r"""Watch the planner's refresh button and rebuild from the iCloud workbook.

Runs every 2 minutes from Windows Task Scheduler ("Jiangnan planner - refresh listener").
When someone taps "Refresh from workbook", the page posts {req} to the ntfy topic below. This script:
  1. picks up requests newer than the last one handled (state in tools/.refresh_state.json, not in git)
  2. runs parse_seed.py (pulls the latest workbook from the iCloud share link) and build.py
  3. commits and pushes index.html if it changed, then waits for GitHub Pages to serve it
  4. posts {done, req, changed} back to the topic, which the page is watching
Log: C:\Users\User\wa-probe\logs\jiangnan_refresh.log"""
import hashlib, json, os, ssl, subprocess, sys, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
TOPIC = "https://ntfy.sh/jiangnan-refresh-5af214c54c2904f9"
LIVE = 'https://lotzehaw-coder.github.io/jiangnan-trip-planner/'
STATE = os.path.join(HERE, '.refresh_state.json')
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()
def http(url, data=None):
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'jiangnan-refresh-listener'}, method='POST' if data else 'GET')
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r: return r.read()
def post(obj): http(TOPIC, json.dumps(obj).encode())
def log(*a): print(time.strftime('%Y-%m-%d %H:%M:%S'), *a, flush=True)

state = json.load(open(STATE)) if os.path.exists(STATE) else {'last_req': 0}
reqs = []
for line in http(TOPIC + '/json?poll=1&since=all').decode('utf-8').splitlines():
    try:
        m = json.loads(line); d = json.loads(m.get('message', '{}'))
        if m.get('event') == 'message' and 'req' in d and 'done' not in d: reqs.append(d)
    except Exception: pass
new = [d for d in reqs if d['req'] > state['last_req']]
if not new: sys.exit(0)
req = max(d['req'] for d in new); by = next((d.get('by') for d in new if d['req'] == req), '') or 'someone'
log(f'refresh requested by {by}')
state['last_req'] = req; json.dump(state, open(STATE, 'w'))
run = lambda *a: subprocess.run(list(a), cwd=HERE, capture_output=True, text=True, encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
try:
    r = run(sys.executable, 'parse_seed.py')
    if r.returncode: raise RuntimeError('workbook read failed: ' + (r.stderr or r.stdout)[-200:])
    if 'iCloud pull failed' in r.stdout: raise RuntimeError('could not download the workbook from iCloud')
    r = run(sys.executable, 'build.py')
    if r.returncode: raise RuntimeError('build failed: ' + (r.stderr or r.stdout)[-200:])
    git = lambda *a: subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    changed = bool(git('status', '--porcelain', 'index.html').stdout.strip())
    if changed:
        git('add', 'index.html')
        c = git('commit', '-m', f'Refresh from workbook (requested by {by})')
        if c.returncode: raise RuntimeError('commit failed')
        git('pull', '--rebase', '-q')
        p = git('push', '-q')
        if p.returncode: raise RuntimeError('push failed: ' + p.stderr[-200:])
        want = hashlib.sha1(open(os.path.join(ROOT, 'index.html'), 'rb').read()).hexdigest()
        for _ in range(40):                       # wait (up to ~10 min) until GitHub Pages serves the new page
            time.sleep(15)
            try:
                if hashlib.sha1(http(LIVE + '?t=' + str(time.time()))).hexdigest() == want: break
            except Exception: pass
    post({'done': int(time.time() * 1000), 'req': req, 'changed': changed})
    log('done, changed =', changed)
except Exception as e:
    post({'done': int(time.time() * 1000), 'req': req, 'changed': False, 'error': str(e)[:160]})
    log('error:', e)
