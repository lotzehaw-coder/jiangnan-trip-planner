"""Extra photos per place for the carousels -> ../img/g/<id>-<n>.jpg, credits in gallery_credits.json.
Config: gallery_queries.json {id: {"q": [...queries], "pins": ["File:..."], "n": 4, "reject": ["File:..."]}}
Re-run safe: an id is skipped once it has files, unless --force <id>. Rejected titles are never used."""
import requests, json, os, sys, io, re, time, glob
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'img', 'g'); os.makedirs(OUT, exist_ok=True)
API = 'https://commons.wikimedia.org/w/api.php'; S = requests.Session()
S.headers['User-Agent'] = 'jiangnan-trip-planner/1.0 (trip planner; github.com/lotzehaw-coder)'
CFG = json.load(open(os.path.join(HERE, 'gallery_queries.json'), encoding='utf-8'))
MAIN = json.load(open(os.path.join(HERE, 'credits.json'), encoding='utf-8'))
CP = os.path.join(HERE, 'gallery_credits.json'); CRED = json.load(open(CP, encoding='utf-8')) if os.path.exists(CP) else {}
force = '--force' in sys.argv; only = [a for a in sys.argv[1:] if not a.startswith('--')]
BAD = re.compile(r'\bmap\b|logo|diagram|plan\b|flag|coat of arms|seal|icon|svg|locator|chart|ticket|menu|station|metro|platform|concourse|bus route|panoramio', re.I)
def strip(h): return re.sub(r'<[^>]+>', '', h or '').strip()
def api(params):
    for i in range(5):
        r = S.get(API, params=params, timeout=40)
        if r.status_code == 200 and r.text.startswith('{'): return r.json()
        time.sleep(4 + 4*i)
    raise RuntimeError('commons api failed')
PROPS = {'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata|mime', 'iiurlwidth': 800, 'format': 'json', 'action': 'query'}
def search(q):
    r = api(dict(PROPS, generator='search', gsrnamespace=6, gsrsearch=q + ' filetype:bitmap', gsrlimit=20))
    return [(p['title'], p['imageinfo'][0]) for p in sorted((r.get('query') or {}).get('pages', {}).values(), key=lambda p: p.get('index', 99)) if p.get('imageinfo')]
def pinned(t):
    r = api(dict(PROPS, titles=t)); p = list(r['query']['pages'].values())[0]
    return [(p['title'], p['imageinfo'][0])] if p.get('imageinfo') else []
def ok(t, ii):
    w, h = ii.get('width', 0), ii.get('height', 0)
    return ii.get('mime') in ('image/jpeg', 'image/png') and not BAD.search(t) and w >= 900 and h >= 560 and 1.2 <= w/h <= 2.0
used_titles = {c['file'] for c in MAIN.values()}
for pid, spec in CFG.items():
    if only and pid not in only: continue
    have = sorted(glob.glob(os.path.join(OUT, f'{pid}-*.jpg')))
    if have and not force: continue
    for f in have: os.remove(f)
    for k in [k for k in CRED if k.startswith(pid + '-')]: CRED.pop(k)
    want = spec.get('n', 4); rej = set(spec.get('reject', [])); picked = []; seen = set(used_titles) | rej
    try:
        cands = [c for t in spec.get('pins', []) for c in pinned(t)]
        for q in spec.get('q', []):
            if len(cands) >= want * 3: break
            cands += [c for c in search(q) if ok(*c)]; time.sleep(1.2)
        for t, ii in cands:
            if len(picked) >= want: break
            if t in seen: continue
            seen.add(t)
            data = S.get(ii['thumburl'], timeout=60).content
            im = Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((800, 600))
            n = len(picked) + 1; dst = os.path.join(OUT, f'{pid}-{n}.jpg'); im.save(dst, 'JPEG', quality=72, optimize=True, progressive=True)
            md = ii.get('extmetadata', {})
            CRED[f'{pid}-{n}'] = {'file': t, 'page': ii.get('descriptionurl'), 'author': strip(md.get('Artist', {}).get('value'))[:80], 'license': strip(md.get('LicenseShortName', {}).get('value'))}
            picked.append(t); time.sleep(0.6)
        print(f'{pid:16} {len(picked)}/{want}', ' | '.join(x[5:45] for x in picked))
    except Exception as e:
        print('ERR', pid, e)
    json.dump(CRED, open(CP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
