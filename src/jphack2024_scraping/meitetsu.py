import requests
from bs4 import BeautifulSoup
import json
import time

def get_station_links(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=lambda href: href and '/train/station_info/line' in href and 'station' in href)
        
        return ['https://www.meitetsu.co.jp' + link['href'] for link in links if not link['href'].endswith('index.html')]
    except requests.RequestException as e:
        print(f"Error fetching station links from {base_url}: {e}")
        return []

def extract_station_info(station_url):
    try:
        response = requests.get(station_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        station_info = {
            "station": "",
            "convenience": -1,
            "toilet": -1,
            "charge_machine": -1,
            "atm": -1,
            "coin_locker": -1,
            "convenience_kind": {}
        }

        station_name = soup.find('h1', class_='station_name')
        if station_name:
            station_info["station"] = station_name.text.strip()

        facility_items = soup.find_all('div', class_='facilityItem')
        for item in facility_items:
            facility_name = item.find('p', class_='facilityName')
            if facility_name:
                name = facility_name.text.strip()
                status = item.find('img', alt=['利用可能', '利用不可'])
                available = 1 if status and '利用可能' in status['alt'] else 0

                if "車いす対応エレベータ" in name:
                    station_info["convenience"] = available
                elif "エレベータ" in name or "エスカレータ" in name:
                    station_info["convenience_kind"][name] = available
                elif "車いす対応トイレ" in name:
                    station_info["toilet"] = available
                elif "トイレ" in name or "オストメイト対応トイレ" in name or "ベビーシート対応トイレ" in name:
                    station_info["convenience_kind"][name] = available
                elif "誘導ブロック" in name or "点字運賃表" in name:
                    station_info["convenience_kind"][name] = available
                elif "点字券売機" in name:
                    station_info["charge_machine"] = available

        return station_info
    except requests.RequestException as e:
        print(f"Error extracting info from {station_url}: {e}")
        return None

def process_line(line_number):
    base_url = f"https://www.meitetsu.co.jp/train/station_info/line{line_number:02d}/index.html"
    station_urls = get_station_links(base_url)
    print(f"Found {len(station_urls)} stations for line {line_number}")

    # station_data = []
    # for url in station_urls:
    #     info = extract_station_info(url)
    #     if info:
    #         station_data.append(info)
    #     time.sleep(1)  # サーバーへの負荷を軽減するために1秒待機

    return station_urls

if __name__ == "__main__":
    all_station_data = []
    for line in range(1, 17):  # 1から16までの路線を処理
        print(f"Processing line {line}")
        line_data = process_line(line)
        all_station_data.extend(line_data)
        time.sleep(1)  # 路線間で2秒待機
    print(all_station_data)
    # # JSONとして出力
    # with open('meitetsu_station_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(all_station_data, f, ensure_ascii=False, indent=2)

    # print(f"Data for {len(all_station_data)} stations has been saved to meitetsu_station_data.json")