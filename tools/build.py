"""seed.json (from parse_seed.py) + extras.json (hotels.py) + photos -> ../index.html"""
import re, os, sys, subprocess, json, glob
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '..', 'index.html') if os.path.basename(here) == 'tools' else os.path.join(here, 'index.html')
t = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
seed = json.load(open(os.path.join(here, 'seed.json'), encoding='utf-8'))

# hotels (tools/hotels.py writes extras.json)
xp = os.path.join(here, 'extras.json')
seed['hotelsx'] = json.load(open(xp, encoding='utf-8')) if os.path.exists(xp) else {'stays': [], 'hotels': {}}

# place photos: img/g/<pid>-<n>.jpg, matched to stops by keyword on the page
Q = json.load(open(os.path.join(here, 'gallery_queries.json'), encoding='utf-8'))
cp = os.path.join(here, 'gallery_credits.json'); cred = json.load(open(cp, encoding='utf-8')) if os.path.exists(cp) else {}
pics = {}
for pid, spec in Q.items():
    files = sorted(glob.glob(os.path.join(here, '..', 'img', 'g', f'{pid}-*.jpg')), key=lambda f: int(re.search(r'-(\d+)\.jpg$', f).group(1)))
    if files: pics[pid] = {'cap': spec.get('cap', ''), 'kw': spec.get('kw', []), 'files': ['img/g/' + os.path.basename(f) for f in files]}
seed['pics'] = pics
seed['credits'] = {k: {'page': v.get('page'), 'author': v.get('author'), 'license': v.get('license')} for k, v in sorted(cred.items()) if os.path.exists(os.path.join(here, '..', 'img', 'g', k + '.jpg'))}

assert t.count('__SEED__') == 1
html = t.replace('__SEED__', json.dumps(seed, ensure_ascii=False, separators=(',', ':')).replace('</script', r'<\/script'))
open(out, 'w', encoding='utf-8').write(html)
js = re.search(r'<script>(.*)</script>', html, re.S).group(1)
node = r'C:\Program Files\nodejs\node.exe' if os.name == 'nt' else 'node'
try:
    tmp = os.path.join(here, '_app.js'); open(tmp, 'w', encoding='utf-8').write(js)
    r = subprocess.run([node, '--check', tmp], capture_output=True, text=True); os.remove(tmp)
    if r.returncode: print(r.stderr[:800]); sys.exit(1)
    print('syntax OK |', end=' ')
except FileNotFoundError:
    print('(node not found, syntax not checked) |', end=' ')
print('wrote', os.path.abspath(out), os.path.getsize(out), 'bytes |', len(pics), 'photo sets |', len(seed['hotelsx']['stays']), 'stays')
