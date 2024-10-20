import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_station(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 駅名の取得方法を修正
    station_title = soup.find('div', id='station-title')
    if station_title:
        station_name_element = station_title.find('span', class_='notranslate')
        if station_name_element:
            station_name = station_name_element.text.strip()
        else:
            station_name = "Unknown Station"
    else:
        station_name = "Unknown Station"
    
    facilities = {
        "エレベーター": -1,
        "改札内トイレ": -1,
        "トイレ": -1,
        "改札内トイレ(多目的)": -1,
        "自動券売機・ICカードチャージ(営業時間内稼働)": -1,
        "駅員無配置": -1,
        "コインロッカー": -1
    }
    
    table = soup.find('table', class_='table-border')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if th and td:
                facility = th.text.strip()
                icon = td.find('i')
                if icon:
                    if 'fa-circle' in icon['class']:
                        value = 1
                    elif 'fa-minus' in icon['class']:
                        value = -1
                    else:
                        value = -1
                    
                    if facility == "駅係員配置":
                        facilities["駅員無配置"] = -value
                    elif facility in facilities:
                        facilities[facility] = value
                    elif facility == "自動券売機・ICカードチャージ(営業時間内稼働)":
                        facilities["自動券売機・ICカードチャージ(営業時間内稼働)"] = value
    print(facilities)
    return {
        "station": station_name,
        "line_name": "愛環",
        **facilities
    }

def main():
    urls = [
        "https://www.aikanrailway.co.jp/station/okazaki.html",
        "https://www.aikanrailway.co.jp/station/mutsuna.html",
        "https://www.aikanrailway.co.jp/station/nakaokazaki.html",
        "https://www.aikanrailway.co.jp/station/kitaokazaki.html",
        "https://www.aikanrailway.co.jp/station/daimon.html",
        "https://www.aikanrailway.co.jp/station/kitanomasuzuka.html",
        "https://www.aikanrailway.co.jp/station/mikawakamigo.html",
        "https://www.aikanrailway.co.jp/station/ekaku.html",
        "https://www.aikanrailway.co.jp/station/suenohara.html",
        "https://www.aikanrailway.co.jp/station/mikawatoyota.html",
        "https://www.aikanrailway.co.jp/station/shinuwagoromo.html",
        "https://www.aikanrailway.co.jp/station/shintoyota.html",
        "https://www.aikanrailway.co.jp/station/aikanumetsubo.html",
        "https://www.aikanrailway.co.jp/station/shigou.html",
        "https://www.aikanrailway.co.jp/station/kaizu.html",
        "https://www.aikanrailway.co.jp/station/homi.html",
        "https://www.aikanrailway.co.jp/station/sasabara.html",
        "https://www.aikanrailway.co.jp/station/yakusa.html",
        "https://www.aikanrailway.co.jp/station/yamaguchi.html",
        "https://www.aikanrailway.co.jp/station/setoguchi.html",
        "https://www.aikanrailway.co.jp/station/setoshi.html",
        "https://www.aikanrailway.co.jp/station/nakamizuno.html",
        "https://www.aikanrailway.co.jp/station/kouzouji.html"
    ]

    all_data = []
    
    for url in urls:
        try:
            station_data = scrape_station(url)
            all_data.append(station_data)
            print(f"Scraped: {station_data['station']}")
            time.sleep(1)  # 1秒待機してサーバーに負荷をかけないようにする
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
    
    with open('station_facilities.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()