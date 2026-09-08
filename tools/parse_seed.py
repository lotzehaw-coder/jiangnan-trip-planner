import openpyxl, json, re, sys, os, urllib.request
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

# ---- source workbook: the shared iCloud link is the source of truth; the local copy is the fallback ----
ICLOUD_LINK = os.environ.get('ITINERARY_ICLOUD', 'https://www.icloud.com/iclouddrive/0ceZfexaUv-X5Xp7cy54Ztrkw')
def fetch_icloud(link, out='itinerary.xlsx'):
    """Resolve a public iCloud Drive share link to its file and download it. No login needed while the link stays shared."""
    guid = link.rstrip('/').split('/')[-1].split('#')[0]
    H = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request('https://ckdatabasews.icloud.com/database/1/com.apple.cloudkit/production/public/records/resolve',
                                 data=json.dumps({'shortGUIDs': [{'value': guid}]}).encode(), headers=H)
    with urllib.request.urlopen(req, timeout=30) as r: res = json.load(r)['results'][0]
    fields = res['rootRecord']['fields']
    url = fields['fileContent']['value']['downloadURL'].replace('${f}', 'itinerary.xlsx')   # NOT thumb1024 — that is the preview image
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=120) as r: data = r.read()
    if data[:2] != b'PK': raise RuntimeError('download was not an xlsx')
    open(out, 'wb').write(data)
    return len(data), fields.get('size', {}).get('value')
if '--local' not in sys.argv:
    try:
        n, sz = fetch_icloud(ICLOUD_LINK); print(f'workbook: pulled from iCloud ({n} bytes)')
    except Exception as e:
        print(f'workbook: iCloud pull failed ({e}); using local itinerary.xlsx')
else:
    print('workbook: local itinerary.xlsx (--local)')
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
B('seed:t4','2026-11-22','train','G-train to Shanghai Pudong 上海浦东',time='09:30',**{'from':'Suzhou 苏州站','to':'Shanghai Pudong PVG'},tentative=True,note='~1h45 direct, or via Hongqiao + Metro L2 · book the night before')
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

# ---- coordinates: WGS-84 from reference sources, converted to GCJ-02 (what Amap / Apple Maps China expect) ----
import math
_a, _ee = 6378245.0, 0.00669342162296594323
def _tlat(x, y):
    r = -100 + 2*x + 3*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
    r += (20*math.sin(6*x*math.pi) + 20*math.sin(2*x*math.pi)) * 2/3
    r += (20*math.sin(y*math.pi) + 40*math.sin(y/3*math.pi)) * 2/3
    r += (160*math.sin(y/12*math.pi) + 320*math.sin(y*math.pi/30)) * 2/3
    return r
def _tlon(x, y):
    r = 300 + x + 2*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
    r += (20*math.sin(6*x*math.pi) + 20*math.sin(2*x*math.pi)) * 2/3
    r += (20*math.sin(x*math.pi) + 40*math.sin(x/3*math.pi)) * 2/3
    r += (150*math.sin(x/12*math.pi) + 300*math.sin(x/30*math.pi)) * 2/3
    return r
def wgs2gcj(lat, lon):
    dlat, dlon = _tlat(lon-105, lat-35), _tlon(lon-105, lat-35)
    rl = lat/180*math.pi; m = math.sin(rl); m = 1 - _ee*m*m; sm = math.sqrt(m)
    dlat = (dlat*180) / ((_a*(1-_ee)) / (m*sm) * math.pi); dlon = (dlon*180) / (_a/sm*math.cos(rl)*math.pi)
    return round(lat+dlat, 6), round(lon+dlon, 6)
COORDS = {  # keyword -> (lat, lon) WGS-84; keys matched longest-first against name, then address
 # Shanghai
 '上海浦东':(31.1443,121.8083),'PVG':(31.1443,121.8083),'启航路900号':(31.1443,121.8083),'虹桥站':(31.1947,121.3199),'虹桥':(31.1947,121.3199),'申贵路1500号':(31.1947,121.3199),
 # Hangzhou
 '杭州东':(30.2905,120.2124),'天城路1号':(30.2905,120.2124),'康莱德':(30.2472,120.2185),'新业路228号':(30.2472,120.2185),'来福士':(30.2480,120.2189),'钱江新城灯光秀':(30.2440,120.2220),'钱江新城':(30.2460,120.2200),'民心路':(30.2440,120.2220),
 '北山街':(30.2590,120.1470),'岳湖':(30.2563,120.1385),'北山路82号':(30.2563,120.1385),'印象西湖':(30.2563,120.1385),'断桥':(30.2588,120.1523),'白堤':(30.2570,120.1450),'西泠印社':(30.2549,120.1418),'孤山路30号':(30.2555,120.1425),'孤山':(30.2549,120.1418),'苏堤':(30.2530,120.1370),'三潭印月':(30.2385,120.1440),'小瀛洲':(30.2385,120.1440),'花港观鱼':(30.2330,120.1380),'杨公堤':(30.2330,120.1380),
 '湖滨路28号':(30.2530,120.1600),'湖滨路':(30.2510,120.1590),'湖滨':(30.2510,120.1590),'雷峰塔':(30.2317,120.1487),'南山路15号':(30.2317,120.1487),'龙井茶村':(30.2210,120.1170),'龙井村':(30.2210,120.1170),'龙井路399号':(30.2260,120.1200),'龙井路':(30.2260,120.1200),
 '河坊街':(30.2402,120.1683),'清河坊':(30.2402,120.1683),'吴山夜市':(30.2500,120.1620),'仁和路':(30.2500,120.1620),'仁和路83号':(30.2500,120.1620),'灵隐寺':(30.2408,120.1010),'法云弄1号':(30.2408,120.1010),'飞来峰':(30.2400,120.1030),'永福寺':(30.2430,120.0960),'法云弄':(30.2430,120.0960),'法喜寺':(30.2260,120.0940),'灵隐路5号':(30.2450,120.1080),'灵隐路':(30.2420,120.1050),'灵隐':(30.2408,120.1010),'满觉陇':(30.2250,120.1330),
 '城隍阁':(30.2440,120.1620),'吴山3号':(30.2440,120.1620),'吴山':(30.2440,120.1620),'胡庆余堂':(30.2415,120.1680),'大井巷95号':(30.2415,120.1680),'大井巷':(30.2415,120.1680),'德寿宫':(30.2455,120.1700),'中河中路':(30.2455,120.1700),'解放路154号':(30.2520,120.1700),'体育场路':(30.2700,120.1650),'曙光路122号':(30.2650,120.1300),'曙光路':(30.2650,120.1300),
 '拱宸桥':(30.3183,120.1360),'桥弄街':(30.3183,120.1360),'小河直街':(30.3130,120.1350),'运河码头':(30.3170,120.1370),'大兜路':(30.3140,120.1400),'丽水路':(30.3100,120.1380),'天目里':(30.2800,120.0870),'天目山路398号':(30.2800,120.0870),'西溪湿地':(30.2660,120.0620),'天目山路518号':(30.2660,120.0620),'海儿巷':(30.2440,120.1650),
 # Nanjing
 '南京南':(31.9690,118.7970),'玉兰路98号':(31.9690,118.7970),'Ritz-Carlton Nanjing':(32.0430,118.7840),'Ritz-Carlton Suzhou':(31.3140,120.6060),'德基广场':(32.0430,118.7840),'德基':(32.0430,118.7840),'中山路18号':(32.0430,118.7840),'中山南路18号':(32.0420,118.7840),'新街口':(32.0410,118.7830),'太平南路248号':(32.0380,118.7900),
 '夫子庙码头':(32.0205,118.7885),'夫子庙':(32.0212,118.7880),'贡院街':(32.0215,118.7890),'江南贡院':(32.0215,118.7895),'金陵路1号':(32.0215,118.7895),'中华门':(32.0100,118.7780),'大报恩寺':(32.0080,118.7830),'雨花路1号':(32.0080,118.7830),'秦淮河':(32.0205,118.7885),'老门东':(32.0140,118.7850),'小西湖':(32.0160,118.7880),'马道街21号':(32.0160,118.7880),'箍桶巷':(32.0140,118.7850),'大顶巷':(32.0230,118.7870),
 '中山陵':(32.0640,118.8500),'石象路7号':(32.0640,118.8500),'美龄宫':(32.0530,118.8430),'音乐台':(32.0610,118.8480),'石象路':(32.0580,118.8340),'明孝陵':(32.0600,118.8380),'紫金山':(32.0620,118.8400),'南京博物院':(32.0400,118.8250),'中山东路321号':(32.0400,118.8250),'中山东路':(32.0410,118.8100),'鸡鸣寺':(32.0600,118.7920),'鸡鸣寺路1号':(32.0600,118.7920),'太平北路':(32.0590,118.7930),'台城':(32.0620,118.7930),'玄武湖':(32.0700,118.7960),'玄武巷1号':(32.0700,118.7960),
 '雕刻时光':(32.0570,118.7790),'鼓楼':(32.0570,118.7790),'狮子桥':(32.0660,118.7780),'湖南路':(32.0660,118.7780),'紫峰大厦':(32.0620,118.7790),'中央路1号':(32.0620,118.7790),'中央路329号':(32.0750,118.7800),'王府大街':(32.0350,118.7790),'汉中路2号':(32.0400,118.7800),'云南北路':(32.0600,118.7750),'南湖':(32.0250,118.7550),'牛首山':(31.9020,118.7620),'宁丹大道':(31.9020,118.7620),'红山森林动物园':(32.0950,118.8110),'和燕路168号':(32.0950,118.8110),'颐和路':(32.0600,118.7730),'先锋书店':(32.0530,118.7690),'广州路173号':(32.0530,118.7690),'栖霞山':(32.1500,118.9500),'栖霞街88号':(32.1500,118.9500),
 # Suzhou
 '苏州站':(31.3290,120.6130),'广济南路369号':(31.3140,120.6060),'广济南路':(31.3140,120.6060),'拙政园':(31.3240,120.6300),'东北街178号':(31.3240,120.6300),'苏州博物馆':(31.3250,120.6290),'东北街204号':(31.3250,120.6290),'狮子林':(31.3220,120.6300),'园林路23号':(31.3220,120.6300),'潘儒巷32号':(31.3175,120.6345),'平江路':(31.3170,120.6350),'双塔市集':(31.3080,120.6330),'吴殿直街2号':(31.3080,120.6330),'山塘街':(31.3220,120.6020),'仁恒仓街':(31.3140,120.6400),'仓街':(31.3140,120.6400),'相门':(31.3140,120.6400),'诚品书店':(31.3120,120.6960),'月廊街8号':(31.3120,120.6960),
 '留园':(31.3175,120.6010),'留园路338号':(31.3175,120.6010),'虎丘':(31.3360,120.5960),'虎丘山门内8号':(31.3360,120.5960),'寒山寺':(31.3120,120.5730),'寒山寺弄24号':(31.3120,120.5730),'松鹤楼':(31.3110,120.6230),'太监弄43号':(31.3110,120.6235),'太监弄':(31.3110,120.6230),'观前街':(31.3115,120.6220),'丝绸博物馆':(31.3170,120.6210),'网师园':(31.2990,120.6320),'阔家头巷11号':(31.2990,120.6320),'十全街':(31.2990,120.6300),'凤凰街':(31.3050,120.6280),'临顿路':(31.3150,120.6290),'嘉馀坊':(31.3100,120.6250),'干将东路':(31.3100,120.6350),
 '金鸡湖':(31.3170,120.7300),'东方之门':(31.3180,120.7320),'星港街199号':(31.3180,120.7320),'苏绣路':(31.3100,120.7250),'同里':(31.1580,120.7200),'周庄':(31.1150,120.8500),'天平山':(31.2830,120.5240),'木渎':(31.2830,120.5240),'苏州中心':(31.3180,120.7320),
}
_keys = sorted(COORDS, key=len, reverse=True)
def locate(*texts):
    for t in texts:
        for k in _keys:
            if k in (t or ''): return wgs2gcj(*COORDS[k])
    return None
for it in items:
    p = locate(it['name'], it['address'], it['info'])
    it['lat'], it['lng'] = (p if p else (None, None))
for b in browse:
    p = locate(b['name'], b['address'])
    b['lat'], b['lng'] = (p if p else (None, None))
for b in blocks:
    # a train's useful pin is the station you leave from; a hotel's is the hotel itself
    p = locate(b['from']) if b['type'] == 'train' else locate(b['title'], b['note'], b.get('to',''))
    b['lat'], b['lng'] = (p if p else (None, None))
print('coords: items', sum(1 for i in items if i['lat']), '/', len(items), '| browse', sum(1 for b in browse if b['lat']), '/', len(browse), '| blocks', sum(1 for b in blocks if b['lat']), '/', len(blocks))
print('no coords:', [i['name'][:30] for i in items if not i['lat']])

seed = {'days':days,'blocks':blocks,'items':items,'browse':browse}
json.dump(seed, open('seed.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
sch = [i for i in items if i['status']=='scheduled']; opt = [i for i in items if i['status']!='scheduled']
print('items',len(items),'scheduled',len(sch),'unscheduled',len(opt),'| blocks',len(blocks),'| browse',len(browse),{s:sum(1 for b in browse if b['section']==s) for s in ('dining','meals','explore','events')})
print('categories',Counter(i['category'] for i in items))
for i in items: print(f"{i['id']:9} {i['day'][-2:] or '--'} {i['time'] or '     ':5} {i['duration'] or '':6} {i['category']:8} {'OPT ' if 'optional' in i['tags'] else '    '}{i['name'][:64]}")
print('--- browse sample ---')
for b in browse[:2] + [x for x in browse if x['section']=='meals'][:2] + [x for x in browse if x['section']=='events'][:1]: print(b)
