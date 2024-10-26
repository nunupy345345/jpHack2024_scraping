import json

# JSONファイルを読み込む
with open('../meitetsu/processed_station_data.json', 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

with open('../aikan/processed_station_data.json', 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

with open('../JR_ToukaidouHonsen/station_facilities.json', 'r', encoding='utf-8') as f3:
    data3 = json.load(f3)

with open('../tikatetsu/nagoya_subway_facilities.json', 'r', encoding='utf-8') as f4:
    data4 = json.load(f4)

# すべてのデータを結合
all_data = data1 + data2 + data3 + data4

# 駅ごとにデータを統合
stations = {}
for item in all_data:
    station = item['station']
    if station not in stations:
        stations[station] = item
        stations[station]['line_name'] = [item['line_name']]
    else:
        # 路線名を追加
        if item['line_name'] not in stations[station]['line_name']:
            stations[station]['line_name'].append(item['line_name'])
        
        # その他の要素を更新
        for key, value in item.items():
            if key != 'station' and key != 'line_name':
                if key not in stations[station]:
                    stations[station][key] = value
                elif value == 1:
                    stations[station][key] = 1

# トイレの処理
for station in stations.values():
    if '改札内トイレ' in station:
        if station['改札内トイレ'] == 1:
            station['トイレ'] = 2
        del station['改札内トイレ']
    
    if '改札内トイレ(多目的)' in station:
        if station['改札内トイレ(多目的)'] == 1:
            station['多目的トイレ'] = 2
        del station['改札内トイレ(多目的)']

# 0を追加
all_keys = set()
for station in stations.values():
    all_keys.update(station.keys())

for station in stations.values():
    for key in all_keys:
        if key not in station and key != 'station' and key != 'line_name':
            station[key] = 0

# 結果を新しいJSONファイルに書き込む
result = list(stations.values())
with open('combined_station_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("処理が完了しました。結果はcombined_station_data.jsonに保存されました。")