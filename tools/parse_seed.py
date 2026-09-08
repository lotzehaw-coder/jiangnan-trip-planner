import openpyxl, json, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
w = openpyxl.load_workbook('itinerary.xlsx', data_only=True)
def rows(name):
    for r in w[name].iter_rows(values_only=True):
        yield [('' if c is None else str(c).strip()) for c in r]

DAYS = [('2026-11-15','Hangzhou','Arrive · Shanghai → Hangzhou'),('2026-11-16','Hangzhou','West Lake, tea & foliage'),
        ('2026-11-17','Hangzhou','Lingyin, old town & Grand Canal'),('2026-11-18','Nanjing','Hangzhou → Nanjing · Confucius Temple'),
        ('2026-11-19','Nanjing','Purple Mountain & Xuanwu'),('2026-11-20','Suzhou','Nanjing → Suzhou · gardens & Pingjiang'),
        ('2026-11-21','Suzhou','Gardens, canals & Kunqu'),('2026-11-22','Shanghai','Suzhou → PVG → home')]
days = [{'d':d,'city':c,'label':l} for d,c,l in DAYS]
day_date = {i+1: DAYS[i][0] for i in range(8)}
day_city = {i+1: DAYS[i][1] for i in range(8)}

PREFIX = re.compile(r'^(?:MUST-SEE(?:\s*\+\s*🍁)?|NEW-EXP|NEW swap|TRENDY swap|SEASONAL swap|EVENING ALTERNATIVE|Optional day-trip|Optional stroll|Optional|NEW|MODERN|STREET FOOD|SHOP|TRENDY|🆕|🏨|🍁|📚|🛍)\s*[:—–-]?\s*', re.I)
def clean(s):
    # strip the sheet's shouty tags but keep "Lunch — …" / "Coffee — …" so a meal row still reads as one
    s = s.replace(' + SHOP:', ' + shop at')
    prev = None
    while prev != s:
        prev = s; s = PREFIX.sub('', s).strip()
    return s
def category(act):
    a = act.lower()
    if re.search(r'coffee|café|cafe', a) and not a.startswith(('lunch','dinner')): return 'Café'
    if a.startswith(('lunch','dinner','farewell dinner','street food','dinner + shop')): return 'Food'
    if 'nightcap' in a: return 'Night'
    if a.startswith(('shop','🛍')) or ' shop:' in a: return 'Shop'
    if 'trendy' in a: return 'Trendy'
    if a.startswith('🍁') or 'seasonal' in a: return 'Foliage'
    if re.search(r'→|immigration|sim/esim|transfer to terminal|bag drop|security|relax at gate|station$', a): return 'Travel'
    return 'Sight'
def dur(t, e):
    h1,m1 = map(int, t.split(':')); h2,m2 = map(int, e.split(':')); m = (h2*60+m2)-(h1*60+m1)
    if m <= 0: return ''
    return f'{m//60}h' if m % 60 == 0 else (f'{m}m' if m < 60 else f'{m//60}h{m%60:02d}')

SKIP = re.compile(r'^(Land at|G-train|🏨 Check-in|Breakfast & checkout|Breakfast at|Depart PVG|Arrive Kuala Lumpur|Return to|Rest$|Pack for)', re.I)
items = []; counters = {}
for r in rows('Itinerary'):
    m = re.match(r'Day (\d)\n', r[0])   # data rows are "Day N\n<date>"; the day-header rows are "Day N — …" and must not match
    if not m: continue
    n = int(m.group(1)); t, act, det, log, addr = r[1], r[2], r[3], r[4], r[5]
    if SKIP.match(act): continue
    counters[n] = counters.get(n, 0) + 1
    optional = t in ('Alt','Opt') or act.lower().startswith('optional') or 'optional' in t.lower()
    tm = re.match(r'^(\d{2}:\d{2})(?:\s*[–-]\s*(\d{2}:\d{2}))?$', t)
    start = tm.group(1) if tm else ''; end = (tm.group(2) or '') if tm else ''
    name = clean(act); cat = category(act)
    tags = []
    if optional: tags.append('optional')
    al = act.lower()
    for k in ('lunch','dinner','breakfast'):
        if al.startswith(k) or f' {k}' in al[:20]: tags.append(k); break
    if 'must-see' in al: tags.append('must-see')
    info = ' · '.join(x for x in (det, log) if x and x != '—')
    items.append({'id':f'p:d{n}-{counters[n]:02d}','name':name,'address':'' if addr in ('','—') else addr,'city':day_city[n],'category':cat,
        'info':info,'tags':tags,'suggestedDay':day_date[n],'time':start,'end':end,'duration':dur(start,end) if end else '',
        'day': day_date[n] if tm else '', 'status': 'scheduled' if tm else 'wishlist', 'order':counters[n]})

blocks = []
def B(id, day, type, title, **kw):
    b = {'id':id,'day':day,'type':type,'title':title,'time':'','number':'','from':'','to':'','tentative':False,'note':'','updatedAt':0}
    b.update(kw); blocks.append(b)
B('seed:mh388','2026-11-15','flight','Fly to Shanghai Pudong',number='MH388',time='09:10',**{'from':'KUL T1','to':'PVG T2'},note='lands 14:30 · Business · A330-300 · confirmed (Trip.com)')
B('seed:t1','2026-11-15','train','G-train to Hangzhou East 杭州东',time='17:00',**{'from':'Shanghai Hongqiao 虹桥','to':'Hangzhou East 杭州东'},tentative=True,note='~1h · not booked yet · sit on the right for river views')
B('seed:h1in','2026-11-15','hotel','Check in — Conrad Hangzhou 康莱德',time='19:10',note='上城区新业路228号 · Qianjiang CBD, connected to Raffles City · ask for a river-view room')
B('seed:h1out','2026-11-18','hotel','Check out — Conrad Hangzhou 康莱德',time='08:00',note='store bags or take to the station')
B('seed:t2','2026-11-18','train','G-train to Nanjing South 南京南',time='10:30',**{'from':'Hangzhou East 杭州东','to':'Nanjing South 南京南'},tentative=True,note='~1h30 · not booked yet')
B('seed:h2in','2026-11-18','hotel','Check in — Ritz-Carlton Nanjing 丽思卡尔顿',time='12:15',note='玄武区中山路18号 · floors 38–62 of Deji Plaza 德基, Xinjiekou · FLAIR bar 62F')
B('seed:h2out','2026-11-20','hotel','Check out — Ritz-Carlton Nanjing 丽思卡尔顿',time='08:00')
B('seed:t3','2026-11-20','train','G-train to Suzhou 苏州',time='10:30',**{'from':'Nanjing South 南京南','to':'Suzhou 苏州'},tentative=True,note='~1h30 · not booked yet')
B('seed:h3in','2026-11-20','hotel','Check in — Ritz-Carlton Suzhou 丽思卡尔顿',time='12:15',note='姑苏区广济南路369号 · Gusu west · <1km Lingering Garden, near Shantang St')
B('seed:h3out','2026-11-22','hotel','Check out — Ritz-Carlton Suzhou 丽思卡尔顿',time='07:30',note='passport + train ticket handy')
B('seed:t4','2026-11-22','train','G-train to Shanghai Pudong 上海浦东',time='09:30',**{'from':'Suzhou 苏州','to':'Shanghai Pudong PVG'},tentative=True,note='~1h45 direct, or via Hongqiao + Metro L2 · book the night before')
B('seed:mh389','2026-11-22','flight','Fly home to Kuala Lumpur',number='MH389',time='16:05',**{'from':'PVG T2','to':'KUL T1'},note='lands 21:50 · Business · A330-300 · confirmed (Trip.com)')

browse = []; bn = 0
def add(section, city, group, name, address, notes, price='', rating='', rank='', cat='', sd=''):
    global bn; bn += 1
    m = re.search(r'\(Day (\d)', name + ' ' + group)
    if not sd and m: sd = day_date[int(m.group(1))]
    browse.append({'id':f'b:{section}:{bn:03d}','section':section,'city':city,'group':group,'rank':rank,'rating':rating,'name':name.strip(),
                   'address':address,'notes':notes,'price':price,'category':cat,'suggestedDay':sd})
CITYHDR = re.compile(r'(HANGZHOU|NANJING|SUZHOU)')
def cityof(s):
    m = CITYHDR.search(s.upper()); return m.group(1).title() if m else ''
icon = lambda s: re.sub(r'^[^\w]+', '', s).strip()

city = ''
for r in rows('Dining & Cafés'):
    c = cityof(r[0])
    if c and not r[1]: city = c; continue
    if not r[1] or r[0] == 'Category' or not city: continue
    add('dining', city, '', r[1], r[2], r[3], price=r[4], cat=icon(r[0]))
group = ''; gcity = ''
for r in rows('Meal Options'):
    if r[0].startswith(('①–','Ratings from','MEAL OPTIONS')) or r[0] == 'Day · Meal': continue
    if not r[2] and r[0]:
        group = r[0]; m = re.match(r'Day (\d)', group); gcity = day_city[int(m.group(1))] if m else gcity; continue
    if not r[2]: continue
    m = re.match(r'Day (\d)', group)
    add('meals', gcity, group, r[2], r[5], r[4], price=r[3], rating=r[1], rank=r[0],
        cat=('Lunch' if 'Lunch' in group else 'Dinner' if 'Dinner' in group else 'Snack'), sd=day_date[int(m.group(1))] if m else '')
city = ''
for r in rows('Shop · Street Food · Explore'):
    c = cityof(r[0])
    if c and not r[1]: city = c; continue
    if not r[1] or r[0] == 'Type' or not city: continue
    add('explore', city, '', r[1], r[2], r[3], cat=icon(r[0]))
city = ''
for r in rows('Events · Seasonal'):
    c = cityof(r[0])
    if c and not r[1]: city = c; continue
    if not r[1] or r[0] == 'Type' or not city: continue
    add('events', city, '', r[1], r[2], r[3], cat=icon(r[0]))

seed = {'days':days,'blocks':blocks,'items':items,'browse':browse}
json.dump(seed, open('seed.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
sch = [i for i in items if i['status']=='scheduled']; opt = [i for i in items if i['status']!='scheduled']
print('items',len(items),'scheduled',len(sch),'unscheduled',len(opt),'| blocks',len(blocks),'| browse',len(browse),{s:sum(1 for b in browse if b['section']==s) for s in ('dining','meals','explore','events')})
print('categories',Counter(i['category'] for i in items))
for i in items: print(f"{i['id']:9} {i['day'][-2:] or '--'} {i['time'] or '     ':5} {i['duration'] or '':6} {i['category']:8} {'OPT ' if 'optional' in i['tags'] else '    '}{i['name'][:64]}")
print('--- browse sample ---')
for b in browse[:2] + [x for x in browse if x['section']=='meals'][:2] + [x for x in browse if x['section']=='events'][:1]: print(b)
