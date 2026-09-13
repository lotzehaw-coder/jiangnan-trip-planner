"""Hotel choices for the Jiangnan planner -> tools/extras.json (merged into the page by build.py).
Prices: lowest public rate per room per night for 2 adults, before taxes, from hilton.com / marriott.com, checked 13 Sep 2026.
Photos: each hotel's own gallery, hotlinked from the chain's image server (never copied into the repo)."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
MYR = 0.606          # 1 CNY in MYR, 9 Sep 2026
CHECKED = '13 Sep 2026'

def mar(key):   # Marriott image server: R/<CODE>/<name> (older renditions) or S/<name> (Scene7)
    if key.startswith('R/'): return f'https://cache.marriott.com/content/dam/marriott-renditions/{key[2:]}-hor-wide.jpg?output-quality=70&interpolation=progressive-bilinear&downsize=800px:*'
    return f'https://cache.marriott.com/is/image/marriotts7prod/{key[2:]}:Wide-Hor?wid=800&fit=constrain'
def hil(code, key):   # hilton.com image server; key = "<id>/<file>?cw=..&ch=..&xposition=..&yposition=.." as the gallery page crops it
    path, q = key.split('?')
    return f'https://www.hilton.com/im/en/{code}/{path}?impolicy=crop&{q.replace("xposition", "gravity=NorthWest&xposition")}&rw=800&rh=533'
def con(path):  # Conrad pages use Hilton's asset cache instead
    return f'https://assets.hiltonstatic.com/hilton-asset-cache/image/upload/c_fill,w_800,h_533,q_75,f_auto,g_auto/Imagery/{path}'

H = {}
def hotel(id, **kw): H[id] = dict(id=id, **kw)

# ---------------- Hangzhou ----------------
hotel('canopy', short='Canopy', name='Canopy by Hilton Hangzhou West Lake', cn='杭州西湖希尔顿嘉悦里酒店', chain='Hilton', brand='Canopy',
      area='Hubin, 6 min walk to West Lake', address='上城区国货路2号 · No. 2 Guohuo Road', opened='Opened Dec 2020 · 160 rooms',
      pros=['6-minute walk to the lake and the Hubin shopping street', 'Metro Line 1 five minutes away (7 stops to Hangzhou East)', 'Walk to Hefang Street and the Wushan night market'],
      cons=['Boutique hotel: no executive lounge or big pool', 'Lake-view rooms cost more (from ¥1,153)'],
      url='https://www.hilton.com/en/hotels/hghwlpy-canopy-hangzhou-west-lake/',
      photos=[(hil('HGHWLPY', '15097650/outside-building.jpg?cw=4143&ch=2762&xposition=0&yposition=119'), 'The hotel'),
              (hil('HGHWLPY', '15097644/hotel-lobby.jpg?cw=4500&ch=3000&xposition=25&yposition=0'), 'Lobby'),
              (hil('HGHWLPY', '15097572/hghwl-premium-room-1.jpg?cw=4210&ch=2806&xposition=0&yposition=96'), 'Premium king room'),
              (hil('HGHWLPY', '15097558/hghwl-lakeview-room.jpg?cw=4176&ch=2784&xposition=0&yposition=108'), 'Lake-view room'),
              (hil('HGHWLPY', '15097515/hghwl-canopy-loft-room.jpg?cw=4282&ch=2854&xposition=0&yposition=72'), 'Canopy loft'),
              (hil('HGHWLPY', '15097608/hghwl-restaurant-bar-1.jpg?cw=4457&ch=2971&xposition=0&yposition=14'), 'Restaurant & bar')],
      near=['broken', 'hefang'])
hotel('conrad', short='Conrad', name='Conrad Hangzhou', cn='杭州康莱德酒店', chain='Hilton', brand='Conrad',
      area='Qianjiang New City, on the river', address='上城区新业路228号 · Raffles City', opened='Opened 2019 · 306 rooms',
      pros=['Top floors of Raffles City: mall, food court and metro downstairs', 'Qiantang River views and the light show at the door', 'Sky lobby, pool and executive lounge'],
      cons=['~25 min by car to West Lake', 'Most expensive in Hangzhou (river view from ¥1,768)'],
      url='https://www.hilton.com/en/hotels/hghfrci-conrad-hangzhou/',
      photos=[(con('Property%20Photography/Conrad/H/HGHFRCI/Conrad_HANGZHOU_Exterior_Horizontal_JPEG_2.jpg'), 'Raffles City towers'),
              (con('Lifestyle%20Photography/Conrad/H/HGHFRCI/Conrad_HANGZHOU_Lobby_Horizontal_TIFF_1.jpg'), 'Lobby'),
              (con('Lifestyle%20Photography/Conrad/H/HGHFRCI/Conrad_HANGZHOU_SkyLobby_Horizontal_TIFF_3.jpg'), 'Sky lobby'),
              (con('Property%20Photography/Conrad/H/HGHFRCI/HGHFR-King%20Deluxe%20River%20View%20Room.jpg'), 'King deluxe river-view room'),
              (con('Property%20Photography/Conrad/H/HGHFRCI/HGHFR-Conrad%20Suite-Living%20Room.jpg'), 'Conrad suite'),
              (con('Property%20Photography/Conrad/H/HGHFRCI/HGHFR-Swimming%20pool.jpg'), 'Pool')],
      near=['qianjiang'])
hotel('jwhz', short='JW Marriott', name='JW Marriott Hotel Hangzhou', cn='杭州JW万豪酒店', chain='Marriott', brand='JW Marriott',
      area='Wulin, ~2 km north-east of West Lake', address='拱墅区湖墅南路28号 · 28 Hushu South Road', opened='Opened 2010 · 305 rooms',
      pros=['Cheapest of the big five-stars here', 'Executive lounge and indoor pool', '600 m to Wulin Square metro and shopping'],
      cons=['Older rooms than Canopy or Conrad', 'Not walking distance to the lake shore sights'],
      url='https://www.marriott.com/en-us/hotels/hghjw-jw-marriott-hotel-hangzhou/overview/',
      photos=[(mar('R/HGHJW/hghjw-exterior-0026'), 'The hotel'), (mar('R/HGHJW/hghjw-frontdesk-0027'), 'Lobby'), (mar('R/HGHJW/hghjw-guestroom-4439'), 'Guest room'),
              (mar('R/HGHJW/hghjw-suite-0013'), 'Suite'), (mar('R/HGHJW/hghjw-lounge-0029'), 'Executive lounge'), (mar('R/HGHJW/hghjw-pool-0023'), 'Indoor pool')],
      near=['gongchen'])
hotel('azure', short='Azure', name='The Azure Qiantang, a Luxury Collection Hotel', cn='杭州钱塘江畔精选酒店', chain='Marriott', brand='Luxury Collection',
      area='Qiantang riverfront, south of the city centre', address='上城区钱江路 · Qiantang River bank', opened='Opened 2014 · 205 rooms',
      pros=['Every room looks over the Qiantang River', 'Quiet, big rooms and a heated indoor pool', 'Between West Lake and the Six Harmonies Pagoda'],
      cons=['Taxi everywhere; no metro at the door', 'Pricier than JW or Marriott Qianjiang'],
      url='https://www.marriott.com/en-us/hotels/hghlc-the-azure-qiantang-a-luxury-collection-hotel-hangzhou/overview/',
      photos=[(mar('R/HGHLC/hghlc-exterior-9657'), 'The hotel'), (mar('R/HGHLC/hghlc-reception-9667'), 'Reception'), (mar('R/HGHLC/hghlc-queen-premierriverview-room-1135'), 'Premier river-view room'),
              (mar('R/HGHLC/hghlc-suite-livingroom-1132'), 'Suite living room'), (mar('R/HGHLC/hghlc-indoor-heated-9672'), 'Heated indoor pool'), (mar('R/HGHLC/hghlc-panorama-restaurant-9663'), 'Panorama restaurant')],
      near=[])
hotel('mqj', short='Marriott', name='Hangzhou Marriott Hotel Qianjiang', cn='杭州钱江新城万豪酒店', chain='Marriott', brand='Marriott',
      area='Qianjiang New City, on the river', address='上城区钱江新城 · Qianjiang New City', opened='Opened Aug 2016 · 348 rooms',
      pros=['284 of the rooms face the Qiantang River', 'Near the light show, much cheaper than the Conrad', 'Executive lounge, pool and spa'],
      cons=['~25 min by car to West Lake', 'A business hotel feel'],
      url='https://www.marriott.com/en-us/hotels/hghqi-hangzhou-marriott-hotel-qianjiang/overview/',
      photos=[(mar('R/HGHQI/hghqi-exterior-0018'), 'The hotel'), (mar('R/HGHQI/hghqi-desk-0047'), 'Lobby'), (mar('R/HGHQI/hghqi-premier-king-4445'), 'Premier king room'),
              (mar('R/HGHQI/hghqi-suite-0035'), 'Suite'), (mar('R/HGHQI/hghqi-lounge-0051'), 'Executive lounge'), (mar('R/HGHQI/hghqi-pool-0043'), 'Pool')],
      near=['qianjiang'])

# ---------------- Nanjing ----------------
hotel('ritznj', short='Ritz-Carlton', name='The Ritz-Carlton, Nanjing', cn='南京丽思卡尔顿酒店', chain='Marriott', brand='Ritz-Carlton',
      area='Xinjiekou, city centre', address='玄武区中山路18号 · floors 38–62 of Deji Plaza', opened='Opened Jun 2020 · 295 rooms',
      pros=['Right above Deji Plaza and the Xinjiekou metro (Lines 1 & 2)', 'Views over Xuanwu Lake and the city from every room', 'FLAIR rooftop bar on 62F, indoor pool'],
      cons=['The most expensive hotel on the trip', 'Marriott Platinum gets no lounge or breakfast at Ritz-Carlton'],
      url='https://www.ritzcarlton.com/en/hotels/nkgrz-the-ritz-carlton-nanjing/overview/',
      photos=[(mar('R/NKGRZ/nkgrz-aerial-view-4134'), 'City view from the tower'), (mar('R/NKGRZ/nkgrz-arrival-lobby-3145'), 'Arrival lobby'), (mar('R/NKGRZ/nkgrz-deluxe-guest-9275'), 'Deluxe room'),
              (mar('R/NKGRZ/nkgrz-xuanwu-lake-3147'), 'Xuanwu Lake view'), (mar('R/NKGRZ/nkgrz-executive-suite-5172'), 'Executive suite'), (mar('R/NKGRZ/nkgrz-indoor-pool-5178'), 'Indoor pool')],
      near=['xinjiekou'])
hotel('westinnj', short='Westin', name='The Westin Nanjing Xuanwu Lake', cn='南京金茂威斯汀大酒店', chain='Marriott', brand='Westin',
      area='Hunan Road, by Xuanwu Lake', address='鼓楼区中央路201号 · 201 Zhongyang Road', opened='Opened 2011 · 234 rooms',
      pros=['Walk to Xuanwu Lake, Jiming Temple and Shiziqiao food street', 'Club lounge and pool', 'A third of the Ritz price'],
      cons=['~3 km north of Xinjiekou and 6 km from Fuzimiao', 'Older building'],
      url='https://www.marriott.com/en-us/hotels/nkgwi-the-westin-nanjing-xuanwu-lake/overview/',
      photos=[(mar('R/NKGWI/nkgwi-exterior-5004'), 'The hotel'), (mar('R/NKGWI/nkgwi-lobby-1737'), 'Lobby'), (mar('R/NKGWI/nkgwi-king-premier-guestroom-2605'), 'Premier king room'),
              (mar('R/NKGWI/nkgwi-executive-5012'), 'Executive room'), (mar('R/NKGWI/nkgwi-club-lounge-5022'), 'Club lounge'), (mar('R/NKGWI/nkgwi-pool-5018'), 'Pool')],
      near=['xuanwu'])
hotel('hiltonnj', short='Hilton', name='Hilton Nanjing', cn='南京希尔顿酒店', chain='Hilton', brand='Hilton',
      area='Hexi, next to Wanda Plaza', address='建邺区江东中路100号 · 100 Jiangdong Middle Road', opened='Opened Nov 2011 · 355 rooms',
      pros=['Executive rooms with lounge access from ¥856', 'Wanda Plaza mall next door', 'Short walk to the Nanjing Massacre Memorial Hall'],
      cons=['~6 km west of the old-town sights', 'Taxi or metro to everything on the plan'],
      url='https://www.hilton.com/en/hotels/nkgjfhi-hilton-nanjing/',
      photos=[(hil('NKGJFHI', '20252579/dji-0389.jpg?cw=4500&ch=3000&xposition=2&yposition=0'), 'The hotel'), (hil('NKGJFHI', '4830553/lobby-03v2.jpg?cw=2250&ch=1500&xposition=1&yposition=0'), 'Lobby'),
              (hil('NKGJFHI', '4821671/nanjing-guestroom.jpg?cw=3542&ch=2361&xposition=0&yposition=238'), 'Guest room'), (hil('NKGJFHI', '4824758/deluxe-suite-living-room.jpg?cw=2243&ch=1495&xposition=0&yposition=2'), 'Deluxe suite living room'),
              (hil('NKGJFHI', '5293041/nkgjfhi-executivelounge.jpg?cw=4500&ch=3000&xposition=3&yposition=0'), 'Executive lounge'), (hil('NKGJFHI', '4821971/pool.jpg?cw=1500&ch=1000&xposition=0&yposition=640'), 'Pool')],
      near=[])
hotel('hiltonriver', short='Hilton Riverside', name='Hilton Nanjing Riverside', cn='南京世茂滨江希尔顿酒店', chain='Hilton', brand='Hilton',
      area='Yangtze riverside, north-west', address='鼓楼区滨江 · Yangtze riverbank', opened='Opened 2011',
      pros=['Cheapest five-star option (from ¥381)', 'River-view rooms from ¥406, suites from ¥832', 'Gardens and an indoor pool'],
      cons=['~7 km from Fuzimiao and Xinjiekou', 'Far from the evening food streets'],
      url='https://www.hilton.com/en/hotels/nkgnrhi-hilton-nanjing-riverside/',
      photos=[(hil('NKGNRHI', '4822463/hotel-exterior.jpg?cw=3750&ch=2500&xposition=0&yposition=0'), 'The hotel'), (hil('NKGNRHI', '4834261/hotel-exterior-night.jpg?cw=3750&ch=2500&xposition=0&yposition=0'), 'At night'),
              (hil('NKGNRHI', '26819738/king-garden-view-room.png?cw=4500&ch=3000&xposition=176&yposition=0'), 'Garden-view king room'), (hil('NKGNRHI', '4830701/nkgnr-premiersuite.jpg?cw=2880&ch=1920&xposition=0&yposition=0'), 'Premier suite'),
              (hil('NKGNRHI', '4824532/nkgnr-swimmingpool.jpg?cw=2880&ch=1920&xposition=0&yposition=0'), 'Indoor pool'), (hil('NKGNRHI', '4834198/outdoor-garden.jpg?cw=3750&ch=2500&xposition=0&yposition=0'), 'Garden')],
      near=[])
hotel('jingli', short='New Jingli', name='The New Jingli Hotel (SLH)', cn='南京新晶丽酒店', chain='Hilton', brand='SLH · book on hilton.com',
      area='Yuhuatai, south of the old city', address='雨花台区紫荆花路2号 · near Kazimen metro', opened='Opened 2019',
      pros=["Nanjing's first Small Luxury Hotels of the World member", 'Neo-classical European style with an in-house art gallery', 'Same owners as Nanjing Impressions 南京大牌档'],
      cons=['Earns Hilton points, but Hilton elite perks do not apply at SLH hotels', '~5 km to Fuzimiao'],
      url='https://www.hilton.com/en/hotels/nkgnjlx-the-new-jingli-hotel/',
      photos=[(hil('NKGNJLX', '20631301/nkgnjlx-111626483-hotel-front-6631x4282.jpg?cw=4843&ch=3229&xposition=78&yposition=0'), 'Hotel front'),
              (hil('NKGNJLX', '20827918/nkgnjlx-111628465-deluxe-room-6480x4320.jpg?cw=5000&ch=3333&xposition=0&yposition=-1'), 'Deluxe room'),
              (hil('NKGNJLX', '20827921/nkgnjlx-111628602-deluxe-suite-6480x4320.jpg?cw=5000&ch=3333&xposition=0&yposition=-1'), 'Deluxe suite'),
              (hil('NKGNJLX', '20827913/nkgnjlx-119450723-the-new-jingli-suite-4032x3046.jpg?cw=4032&ch=2688&xposition=0&yposition=179'), 'New Jingli suite')],
      near=[])

# ---------------- Suzhou ----------------
hotel('ritzsz', short='Ritz-Carlton', name='The Ritz-Carlton, Suzhou', cn='苏州丽思卡尔顿酒店', chain='Marriott', brand='Ritz-Carlton',
      area='Gusu, west edge of the old town', address='姑苏区广济南路369号 · China Central Place', opened='Opened Mar 2025',
      pros=['Newest hotel on the list', 'Under 1 km to the Lingering Garden, near Shantang Street', 'Club lounge (club rooms), pool'],
      cons=['Marriott Platinum gets no lounge or breakfast at Ritz-Carlton', '~15 min by car to Pingjiang Road'],
      url='https://www.ritzcarlton.com/en/hotels/wuxsz-the-ritz-carlton-suzhou/overview/',
      photos=[(mar('S/rz-wuxsz-hotel-exterior-34977'), 'The hotel'), (mar('S/rz-wuxsz-premier-guest-room-13750-32048'), 'Premier room'), (mar('S/rz-wuxsz-panorama-room-23619'), 'Panorama room'),
              (mar('S/rz-wuxsz-premier-suite-33264-38220'), 'Premier suite'), (mar('S/rz-wuxsz-club-lounge-37192'), 'Club lounge'), (mar('S/rz-wuxsz-swimming-pool-28846'), 'Pool')],
      near=['liuyuan', 'shantang'])
hotel('wsz', short='W Suzhou', name='W Suzhou', cn='苏州W酒店', chain='Marriott', brand='W',
      area='Jinji Lake, Suzhou Industrial Park', address='工业园区苏州中心7号楼 · Suzhou Center', opened='Opened Sep 2017',
      pros=['Lake views over Jinji Lake and the Suzhou Center mall', 'WET pool, lively bar scene', 'Platinum breakfast applies (unlike Ritz-Carlton)'],
      cons=['~10 km east of the old-town gardens (20–30 min by car)', 'Modern business district, not the canal-town feel'],
      url='https://www.marriott.com/en-us/hotels/szvwh-w-suzhou/overview/',
      photos=[(mar('R/SZVWH/szvwh-exterior-8518'), 'The hotel'), (mar('R/SZVWH/szvwh-hotel-entrance-8517'), 'Entrance'), (mar('R/SZVWH/szvwh-wonderful-room-1268'), 'Wonderful room'),
              (mar('R/SZVWH/szvwh-wow-suite-8792'), 'WOW suite'), (mar('R/SZVWH/szvwh-wet-8784'), 'WET pool'), (mar('R/SZVWH/szvwh-living-room-8519'), 'Living Room lounge')],
      near=['jinji'])
hotel('hiltonsz', short='Hilton', name='Hilton Suzhou', cn='苏州希尔顿酒店', chain='Hilton', brand='Hilton',
      area='Jinji Lake, Suzhou Industrial Park', address='工业园区苏州大道东275号 · Nanshi Street metro', opened='Opened May 2016',
      pros=['Executive rooms with lounge access from ¥892', 'Metro at the door (Line 1 to the old town)', 'Pool, suites with kitchens'],
      cons=['~10 km east of the old-town gardens', 'Business-district location'],
      url='https://www.hilton.com/en/hotels/szvtvhi-hilton-suzhou/',
      photos=[(hil('SZVTVHI', '7110522/hotel-exterior.jpg?cw=5000&ch=3333&xposition=0&yposition=193'), 'The hotel'), (hil('SZVTVHI', '2207279/yuxi-lobby.jpg?cw=4984&ch=3323&xposition=7&yposition=0'), 'Yu Xi Chinese restaurant'),
              (hil('SZVTVHI', '6589473/szvtvdi-king-deluxe-room.jpg?cw=4500&ch=3000&xposition=0&yposition=0'), 'King deluxe room'), (hil('SZVTVHI', '6589493/szvtvdi-king-deluxe-suite.jpg?cw=4500&ch=3000&xposition=176&yposition=0'), 'King deluxe suite'),
              (hil('SZVTVHI', '2206369/executive-lounge.jpg?cw=5000&ch=3333&xposition=0&yposition=0'), 'Executive lounge'), (hil('SZVTVHI', '2203540/swimming-pool.jpg?cw=5000&ch=3333&xposition=0&yposition=0'), 'Pool')],
      near=['jinji'])
hotel('szmarriott', short='Marriott', name='Suzhou Marriott Hotel', cn='苏州万豪酒店', chain='Marriott', brand='Marriott',
      area='Ganjiang West Road, west of the old town', address='姑苏区干将西路1296号 · 1296 Ganjiang Rd West', opened='Opened 2009 · renovated 2020 · 293 rooms',
      pros=['Half the Ritz price, ~2 km further west', 'Executive lounge and indoor pool', 'Straight along Ganjiang Road into the old town'],
      cons=['~5 km to Pingjiang Road and the Humble Administrator\'s Garden', 'Older building'],
      url='https://www.marriott.com/en-us/hotels/szvmc-suzhou-marriott-hotel/overview/',
      photos=[(mar('R/SZVMC/szvmc-exterior-7447'), 'The hotel'), (mar('R/SZVMC/szvmc-lobby-7451'), 'Lobby'), (mar('R/SZVMC/szvmc-king-guestroom-7440'), 'King room'),
              (mar('R/SZVMC/szvmc-executive-suite-7455'), 'Executive suite'), (mar('R/SZVMC/szvmc-lounge-7452'), 'Executive lounge'), (mar('R/SZVMC/szvmc-pool-0029'), 'Indoor pool')],
      near=['liuyuan'])

# ---------------- stays: price = lowest public rate for THOSE dates ----------------
STAYS = [
 dict(id='hz1', start='2026-11-15', city='Hangzhou', title='Hangzhou · first two nights', dates='Sun 15 → Tue 17 Nov', nights=2, default='canopy',
      tip="Tze's plan: Canopy by the lake for the West Lake days, then one night at the Conrad.",
      options=[('canopy', 841), ('jwhz', 749), ('mqj', 722), ('azure', 1187), ('conrad', 1641)]),
 dict(id='hz2', start='2026-11-17', city='Hangzhou', title='Hangzhou · last night', dates='Tue 17 → Wed 18 Nov', nights=1, default='conrad',
      tip='Pick the same hotel as the first two nights to skip the hotel move on the 17th.',
      options=[('conrad', 1641), ('mqj', 827), ('azure', 1235), ('jwhz', 802), ('canopy', 841)]),
 dict(id='nj', start='2026-11-18', city='Nanjing', title='Nanjing', dates='Wed 18 → Fri 20 Nov', nights=2, default='ritznj',
      tip='Most of the Nanjing plan is Fuzimiao, Xinjiekou and Purple Mountain, so a central hotel saves the most taxi time.',
      options=[('ritznj', 2090), ('westinnj', 699), ('hiltonnj', 625), ('jingli', 969), ('hiltonriver', 381)]),
 dict(id='sz', start='2026-11-20', city='Suzhou', title='Suzhou', dates='Fri 20 → Sun 22 Nov', nights=2, default='ritzsz',
      tip='The gardens and canal streets are in the old town (Gusu). Jinji Lake hotels are newer-city, 20–30 min away.',
      options=[('ritzsz', 1577), ('szmarriott', 812), ('wsz', 1052), ('hiltonsz', 652)]),
]
out = {'stays': [], 'hotels': {}, 'priceNote': f'Lowest public rate per room per night for 2 adults, before taxes (about 6%), checked on hilton.com / marriott.com on {CHECKED}. RM at 1 CNY = RM{MYR}.', 'myr': MYR}
for s in STAYS:
    opts = []
    for hid, p in s['options']:
        assert hid in H, hid
        opts.append({'id': hid, 'price': p, 'myr': round(p * MYR), 'total': p * s['nights']})
    out['stays'].append(dict(s, options=opts))
for hid, h in H.items():
    out['hotels'][hid] = dict(h, photos=[{'src': u, 'cap': c + (' · © Hilton' if h['chain'] == 'Hilton' else ' · © Marriott')} for u, c in h['photos']])
json.dump(out, open(os.path.join(HERE, 'extras.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('hotels', len(H), '| stays', [(s['id'], len(s['options'])) for s in STAYS])
