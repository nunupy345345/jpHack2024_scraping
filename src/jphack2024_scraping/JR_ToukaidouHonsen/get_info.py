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
    "JR東海道本線": ['/station-guide/shinkansen/atami/index.html', '/station-guide/shizuoka/kannami/index.html', '/station-guide/shinkansen/mishima/index.html', '/station-guide/shizuoka/numazu/index.html', '/station-guide/shizuoka/katahama/index.html', '/station-guide/shizuoka/hara/index.html', '/station-guide/shizuoka/yoshiwara/index.html', '/station-guide/shizuoka/fuji/index.html', '/station-guide/shizuoka/fujikawa/index.html', '/station-guide/shizuoka/shin-kambara/index.html', '/station-guide/shizuoka/yui/index.html', '/station-guide/shizuoka/okitsu/index.html', '/station-guide/shizuoka/shimizu/index.html', '/station-guide/shizuoka/kusanagi/index.html', '/station-guide/shizuoka/higashi-shizuoka/index.html', '/station-guide/shinkansen/shizuoka/index.html', '/station-guide/shizuoka/abekawa/index.html', '/station-guide/shizuoka/mochimune/index.html', '/station-guide/shizuoka/yaizu/index.html', '/station-guide/shizuoka/nishi-yaizu/index.html', '/station-guide/shizuoka/fujieda/index.html', '/station-guide/shizuoka/rokugo/index.html', '/station-guide/shizuoka/shimada/index.html', '/station-guide/shizuoka/kanaya/index.html', '/station-guide/shizuoka/kikugawa/index.html', '/station-guide/shinkansen/kakegawa/index.html', '/station-guide/shizuoka/aino/index.html', '/station-guide/shizuoka/fukuroi/index.html', '/station-guide/shizuoka/mikuriya/index.html', '/station-guide/shizuoka/iwata/index.html', '/station-guide/shizuoka/toyodacho/index.html', '/station-guide/shizuoka/tenryugawa/index.html', '/station-guide/shinkansen/hamamatsu/index.html', '/station-guide/shizuoka/takatsuka/index.html', '/station-guide/shizuoka/maisaka/index.html', '/station-guide/shizuoka/araimachi/index.html', '/station-guide/shizuoka/washizu/index.html', '/station-guide/shizuoka/shinjohara/index.html', '/station-guide/tokai/futagawa/index.html', '/station-guide/shinkansen/toyohashi/index.html', '/station-guide/tokai/mikawa-miya/index.html', '/station-guide/tokai/gamagori/index.html', '/station-guide/tokai/koda/index.html', '/station-guide/tokai/aimi/index.html', '/station-guide/tokai/okazaki/index.html', '/station-guide/tokai/nishi-okazaki/index.html', '/station-guide/tokai/anjo/index.html', '/station-guide/shinkansen/mikawa-anjo/index.html', '/station-guide/tokai/higashi-kariya/index.html', '/station-guide/tokai/noda-shimmachi/index.html', '/station-guide/tokai/kariya/index.html', '/station-guide/tokai/aizuma/index.html', '/station-guide/tokai/obu/index.html', '/station-guide/tokai/kyowa/index.html', '/station-guide/tokai/minami-odaka/index.html', '/station-guide/tokai/odaka/index.html', '/station-guide/tokai/kasadera/index.html', '/station-guide/tokai/atsuta/index.html', '/station-guide/tokai/kanayama/index.html', '/station-guide/tokai/otobashi/index.html', '/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/biwajima/index.html', '/station-guide/tokai/kiyosu/index.html', '/station-guide/tokai/inazawa/index.html', '/station-guide/tokai/owari-ichinomiya/index.html', '/station-guide/tokai/kisogawa/index.html', '/station-guide/tokai/gifu/index.html', '/station-guide/tokai/nishi-gifu/index.html', '/station-guide/tokai/hozumi/index.html', '/station-guide/tokai/ogaki/index.html', '/station-guide/tokai/tarui/index.html', '/station-guide/shinkansen/maibara/index.html', Ellipsis],
    "飯田線": ['/station-guide/shinkansen/toyohashi/index.html', '/station-guide/tokai/toyokawa/index.html', '/station-guide/tokai/shinshiro/index.html', '/station-guide/tokai/chubu-tenryu/index.html', '/station-guide/tokai/iida/index.html', '/station-guide/tokai/inashi/index.html', Ellipsis],
    "中央本線": ['/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/kanayama/index.html', '/station-guide/tokai/tsurumai/index.html', '/station-guide/tokai/chikusa/index.html', '/station-guide/tokai/ozone/index.html', '/station-guide/tokai/shin-moriyama/index.html', '/station-guide/tokai/kachigawa/index.html', '/station-guide/tokai/kasugai/index.html', '/station-guide/tokai/jinryo/index.html', '/station-guide/tokai/kozoji/index.html', '/station-guide/tokai/tajimi/index.html', '/station-guide/tokai/tokishi/index.html', '/station-guide/tokai/mizunami/index.html', '/station-guide/tokai/ena/index.html', '/station-guide/tokai/nakatsugawa/index.html', '/station-guide/tokai/kiso-fukushima/index.html', Ellipsis],
    "武豊線": ['/station-guide/tokai/obu/index.html', '/station-guide/tokai/ogawa/index.html', '/station-guide/tokai/higashiura/index.html', '/station-guide/tokai/kamezaki/index.html', '/station-guide/tokai/handa/index.html', '/station-guide/tokai/taketoyo/index.html', Ellipsis],
    "太多線": ['/station-guide/tokai/tajimi/index.html', '/station-guide/tokai/kani/index.html', '/station-guide/tokai/mino-ota/index.html', Ellipsis],
    "関西本線": ['/station-guide/shinkansen/nagoya/index.html', '/station-guide/tokai/hatta/index.html', '/station-guide/tokai/haruta/index.html', '/station-guide/tokai/kanie/index.html', '/station-guide/tokai/kuwana/index.html', '/station-guide/tokai/yokkaichi/index.html', '/station-guide/tokai/kameyama/index.html', Ellipsis],
    "高山本線": ['/station-guide/tokai/gifu/index.html', '/station-guide/tokai/unuma/index.html', '/station-guide/tokai/mino-ota/index.html', '/station-guide/tokai/gero/index.html', '/station-guide/tokai/takayama/index.html', Ellipsis],
    "参宮線": ['/station-guide/tokai/taki/index.html', '/station-guide/tokai/iseshi/index.html'],
    "紀勢本線": ['/station-guide/tokai/kameyama/index.html', '/station-guide/tokai/tsu/index.html', '/station-guide/tokai/matsusaka/index.html', '/station-guide/tokai/taki/index.html', '/station-guide/tokai/kii-nagashima/index.html', '/station-guide/tokai/owase/index.html', '/station-guide/tokai/kumanoshi/index.html', Ellipsis],
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