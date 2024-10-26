import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_station(url, station_name, line_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
    }
    print(f"Accessing URL: {url}")
    
    response = requests.get(url, headers=headers)
    # response.encoding = 'utf-8'
    # response = requests.get(url)
    response.encoding = 'utf-8' 
    
    print(f"Response status: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    stores = []
    # store_container = soup.find('div', class_='cntWhite storelist-container')
    store_container = soup.find('div',class_='cntWhite storelist-container')
    print(store_container)
  
    if store_container:
        for store in store_container.find_all('div', class_='storeList'):
            print(store)
            if 'style' in store.attrs and 'display:none' in store['style']:
                continue
                
            store_data = {}
            dl = store.find('dl')
            if dl:
                dts = dl.find_all('dt')
                dds = dl.find_all('dd')
                
                for dt, dd in zip(dts, dds):
                    if dt.text == '事業者名':
                        store_data['business_name'] = dd.text.strip()
                    elif dt.text == '場所':
                        location = dd.text.strip()
                        if '改札内' in location and '改札外' in location:
                            store_data['location_type'] = 4
                        elif '改札内' in location:
                            store_data['location_type'] = 2
                        elif '改札外' in location:
                            store_data['location_type'] = 3
                        else:
                            store_data['location_type'] = 1
                
                if store_data:
                    stores.append(store_data)
    print({
        "station": station_name,
        "line_name": line_name,
        "stores": stores
    })
    
    return {
        "station": station_name,
        "line_name": line_name,
        "stores": stores
    }

def generate_urls(stations):
    base_url = "https://www.kotsu.city.nagoya.jp/jp/pc/SUBWAY/station_store.html?name="
    return {line: [(f"{base_url}{station}", station) for station in line_stations] for line, line_stations in stations.items()}

def main():
    stations = {
        "東山線": ["高畑", "八田", "岩塚", "中村公園", "中村日赤", "本陣", "亀島", "名古屋", "伏見", "栄",
                   "新栄町", "千種", "今池", "池下", "覚王山", "本山", "東山公園", "星ヶ丘", "一社", "上社",
                   "本郷", "藤が丘"],
        "名城線": ["金山", "東別院", "上前津", "矢場町", "栄", "久屋大通", "名古屋城", "名城公園", "黒川", "志賀本通",
                   "平安通", "大曽根", "ナゴヤドーム前矢田", "砂田橋", "茶屋ヶ坂", "自由ヶ丘", "本山", "名古屋大学", "八事日赤", "八事",
                   "総合リハビリセンター", "瑞穂運動場東", "新瑞橋", "妙音通", "堀田", "熱田神宮伝馬町", "熱田神宮西", "西高蔵"],
        "名港線": ["日比野", "六番町", "東海通", "港区役所", "築地口", "名古屋港"],
        "鶴舞線": ["上小田井", "庄内緑地公園", "庄内通", "浄心", "浅間町", "丸の内", "伏見", "大須観音", "上前津", "鶴舞",
                   "荒畑", "御器所", "川名", "いりなか", "八事", "塩釜口", "植田", "原", "平針", "赤池"],
        "桜通線": ["太閤通", "名古屋", "国際センター", "丸の内", "久屋大通", "高岳", "車道", "今池", "吹上", "御器所",
                   "桜山", "瑞穂区役所", "瑞穂運動場西", "新瑞橋", "桜本町", "鶴里", "野並", "鳴子北", "相生山", "神沢",
                   "徳重"],
        "上飯田線": ["上飯田", "平安通"]
    }
    
    urls = generate_urls(stations)
    all_data = []
    
    for line, line_urls in urls.items():
        for url, station_name in line_urls:
            try:
                station_data = scrape_station(url, station_name, line)
                all_data.append(station_data)
                print(f"Scraped: {station_data['station']} on {line}")
                time.sleep(1)
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
    
    with open('nagoya_subway_stores.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()