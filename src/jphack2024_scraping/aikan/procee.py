import json

# JSONデータを読み込む
data = json.loads('''
                  [
  {
    "station": "岡崎",
    "line_name": "愛環",
    "エレベーター": 1,
    "改札内トイレ": 1,
    "トイレ": -1,
    "改札内トイレ(多目的)": 1,
    "自動券売機・ICカードチャージ(営業時間内稼働)": 1,
    "駅員無配置": -1,
    "コインロッカー": -1
  },
  {
    "station": "六名",
    "line_name": "愛環",
    "エレベーター": -1,
    "改札内トイレ": -1,
    "トイレ": -1,
    "改札内トイレ(多目的)": -1,
    "自動券売機・ICカードチャージ(営業時間内稼働)": -1,
    "駅員無配置": 1,
    "コインロッカー": -1
  },
]
                  ''')
# 各駅のデータを処理
for station in data:
    # "駅員無配置"を"駅員配置"に変更し、値を反転
    if "駅員無配置" in station:
        station["駅員配置"] = -station["駅員無配置"]
        del station["駅員無配置"]
    if "改札内トイレ" in station:
      if station["改札内トイレ"] == 1:
        station["トイレ"] = 2
      else:
        station["トイレ"] = -1
      del station["改札内トイレ"]
    
    
    # # すべての数値を反転（-1 → 1, 1 → -1）
    # for key, value in station.items():
    #     if isinstance(value, int):
    #         station[key] = -value
with open('processed_toilet_station_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
# 結果を表示
print(json.dumps(data, ensure_ascii=False, indent=2))