import requests
from bs4 import BeautifulSoup
import json
import re
import time

def scrape_station(url, line_name):
    base_url = "https://railway.jr-central.co.jp"
    full_url = base_url + url
    print(full_url)
    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    station_name_element = soup.find('h2', class_='name current')
    if station_name_element:
        # spanタグを除去し、残りのテキストを取得
        for span in station_name_element.find_all('span'):
            span.extract()
        station_name = station_name_element.text.strip()
        # 最後の "駅" を削除
        if station_name.endswith('駅'):
            station_name = station_name[:-1]
    else:
        station_name = "Unknown Station"
    icon_list = soup.find('ul', class_='icon-list clearfix')
    icons = [li['id'] for li in icon_list.find_all('li')] if icon_list else []
    
    facilities = {
        "車いす対応エレベータ": 1 if "icon-16" in icons else -1,
        "エレベータ": 1 if "icon-16" in icons else -1,
        "エスカレータ": 1 if "icon-24" in icons else -1,
        "車いす対応トイレ": 1 if "icon-11" in icons or "icon-6" in icons or "icon-9" in icons else -1,
        "トイレ": 1 if "icon-11" in icons or "icon-6" in icons or "icon-9" in icons else -1,
        "オストメイト対応トイレ": 1 if "icon-11" in icons else -1,
        "ベビーシート対応トイレ": 1 if "icon-11" in icons or "icon-9" in icons else -1,
        "車いす対応スロープ": 1 if "icon-18" in icons else -1,
        "コインロッカー": 1 if "icon-12" in icons else -1
    }
    
    return {
        "station": station_name,
        "line_name": line_name,
        **facilities
    }

def main():
    content ={
    "JR東海道本線": ['/station-guide/shinkansen/atami/index.html', '/station-guide/shizuoka/kannami/index.html', Ellipsis],
    "飯田線": ['/station-guide/shinkansen/toyohashi/index.html', '/station-guide/tokai/toyokawa/index.html', Ellipsis],
    "中央本線": ['/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/kanayama/index.html', Ellipsis],
    "武豊線": ['/station-guide/tokai/obu/index.html', '/station-guide/tokai/ogawa/index.html', Ellipsis],
    "太多線": ['/station-guide/tokai/tajimi/index.html', '/station-guide/tokai/kani/index.html', Ellipsis],
    "関西本線": ['/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/hatta/index.html', Ellipsis],
    "高山本線": ['/station-guide/tokai/gifu/index.html', '/station-guide/tokai/unuma/index.html', Ellipsis],
    "参宮線": ['/station-guide/tokai/taki/index.html', '/station-guide/tokai/iseshi/index.html'],
    "紀勢本線": ['/station-guide/tokai/kameyama/index.html', '/station-guide/tokai/tsu/index.html', Ellipsis],
    "名松線": ['/station-guide/tokai/matsusaka/index.html']
}
    

    all_data = []
    
    for line_name, urls in content.items():
        for url in urls:
            if url is Ellipsis:
                continue
            try:
                station_data = scrape_station(url, line_name)
                all_data.append(station_data)
                print(f"Scraped: {station_data['station']} on {line_name}")
                time.sleep(1)
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
    
    with open('station_facilities.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
if __name__ == "__main__":
    main()