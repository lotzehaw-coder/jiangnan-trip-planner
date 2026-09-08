"""seed.json + template.html -> ../index.html (or ./index.html when run from the scratch folder)."""
import re, os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '..', 'index.html') if os.path.basename(here) == 'tools' else os.path.join(here, 'index.html')
t = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
seed = open(os.path.join(here, 'seed.json'), encoding='utf-8').read()
assert t.count('__SEED__') == 1
html = t.replace('__SEED__', seed.replace('</script', r'<\/script'))
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
print('wrote', os.path.abspath(out), os.path.getsize(out), 'bytes')
