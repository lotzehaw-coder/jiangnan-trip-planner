"""Train options for the Jiangnan planner -> merged into tools/extras.json (run after hotels.py).
Fuxing Hao 复兴号 G-trains only (Tze, 13 Sep: "I'm only interested in the Fuxinghao and not the older trains").
Source: 12306 (kyfw.12306.cn leftTicket/queryG + queryTicketPrice), sampled 13 Sep 2026 for the same weekday in late
September (Sun 27 / Wed 23 / Fri 25 Sep), because November tickets are not on sale yet. China's high-speed fares now float
by train and time of day, so November prices can differ a little. Fuxing = dw_flag field [1] == '1' (12306's own badge logic)."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

def T(code, dep, arr, dur, first, biz, second, note=''):
    return {'code': code, 'dep': dep, 'arr': arr, 'dur': dur, 'first': first, 'biz': biz, 'second': second, 'note': note}

LEGS = [
 {'id': 't1', 'block': 'seed:t1', 'date': '2026-11-15', 'from': 'Shanghai Hongqiao 上海虹桥', 'to': 'Hangzhou East 杭州东', 'sale': 'Sun 1 Nov',
  'before': {'what': 'Airport Link 市域机场线 PVG T1/T2 → Hongqiao T2', 'each': 26, 'note': '~40 min, ¥26; lands 14:30, so aim for a train after ~16:30'},
  'suggest': 'G231', 'trains': [
   T('G253', '16:00', '16:45', '45m', 140, 275, 87, 'tight after a 14:30 landing'), T('G1583', '16:32', '17:24', '52m', 140, 306, 87),
   T('G1343', '16:37', '17:36', '59m', 140, 275, 87), T('G231', '17:13', '17:58', '45m', 140, 306, 87, 'non-stop feel, 45 min'),
   T('G261', '17:17', '18:02', '45m', 140, 306, 87), T('G1349', '17:38', '18:37', '59m', 140, 275, 87),
   T('G7367', '17:47', '18:52', '1h05', 126, 275, 78), T('G7371', '18:08', '19:05', '57m', 140, 306, 87)]},
 {'id': 't2', 'block': 'seed:t2', 'date': '2026-11-18', 'from': 'Hangzhou East 杭州东', 'to': 'Nanjing South 南京南', 'sale': 'Wed 4 Nov',
  'suggest': 'G7650', 'trains': [
   T('G590', '09:13', '10:42', '1h29', 225, 493, 141), T('G7674', '10:15', '11:36', '1h21', 225, 493, 141),
   T('G7650', '10:25', '11:42', '1h17', 225, 493, 141, 'closest to the 10:30 plan'), T('G7796', '10:42', '12:17', '1h35', 225, 493, 141),
   T('G822', '11:24', '12:26', '1h02', 225, 493, 141, 'fastest'), T('G824', '11:39', '13:13', '1h34', 225, 493, 141)]},
 {'id': 't3', 'block': 'seed:t3', 'date': '2026-11-20', 'from': 'Nanjing South 南京南', 'to': 'Suzhou 苏州', 'sale': 'Fri 6 Nov',
  'suggest': 'G7221', 'trains': [
   T('G7225', '08:45', '09:52', '1h07', 200, 437, 125, 'fastest'), T('G7591', '09:42', '11:17', '1h35', 180, 393, 113),
   T('G7221', '09:59', '11:40', '1h41', 180, 393, 113, 'arrives in time for the 12:15 check-in'), T('G2365', '10:47', '12:23', '1h36', 200, 398, 125, 'check-in slips to ~13:00')]},
 {'id': 't4', 'block': 'seed:t4', 'date': '2026-11-22', 'from': 'Suzhou 苏州 / Suzhou North 苏州北', 'to': 'Shanghai Hongqiao 上海虹桥', 'sale': 'Sun 8 Nov',
  'after': {'what': 'Airport Link 市域机场线 Hongqiao T2 → PVG T1/T2', 'each': 26, 'note': '~40 min, ¥26; MH389 leaves 16:05, be at PVG by ~13:00'},
  'suggest': 'G7461', 'trains': [
   T('G7461', '09:19', '09:51', '32m', 74, 162, 46, '苏州站, 10 min from the Ritz'), T('G7507', '09:39', '10:09', '30m', 63, 117, 37, '苏州北, ~25 min drive'),
   T('G7431', '10:29', '10:59', '30m', 70, 145, 42, '苏州北'), T('G2661', '10:49', '11:12', '23m', 70, 145, 42, '苏州北'),
   T('G7591', '11:19', '11:54', '35m', 67, 146, 41, '苏州站, latest sensible')]},
]
p = os.path.join(HERE, 'extras.json'); X = json.load(open(p, encoding='utf-8'))
X['trains'] = {'legs': LEGS, 'note': "Fuxing Hao 复兴号 G-trains only. Fares from 12306 for the same weekday in late September (13 Sep check); high-speed fares float by train and time, so November can differ slightly. Tickets open 15 days ahead counting the travel day, at 12306 or Trip.com; passports needed."}
json.dump(X, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for L in LEGS:
    s = next(t for t in L['trains'] if t['code'] == L['suggest'])
    print(L['id'], L['from'][:12], '->', L['to'][:12], s['code'], s['dep'], 'first', s['first'], 'biz', s['biz'])
