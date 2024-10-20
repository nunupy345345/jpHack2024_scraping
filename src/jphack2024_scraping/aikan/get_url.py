import requests
from bs4 import BeautifulSoup
import urllib.parse

# ウェブページのURLを指定
base_url = "https://www.aikanrailway.co.jp/station/"

# ウェブページの内容を取得
response = requests.get(base_url)
html_content = response.text

# BeautifulSoupを使用してHTMLを解析
soup = BeautifulSoup(html_content, 'html.parser')

# 特定の形式のaタグを検索
urls = []
station_list_table = soup.find('table', class_='station-list mb20-40')
for a_tag in station_list_table.find_all('a', href=True):
    # 相対URLを絶対URLに変換
    full_url = urllib.parse.urljoin(base_url, a_tag['href'])
    urls.append(full_url)

# 結果を表示
for url in urls:
    print(url)
    
# # result
# [https://www.aikanrailway.co.jp/station/okazaki.html,
# https://www.aikanrailway.co.jp/station/mutsuna.html,
# https://www.aikanrailway.co.jp/station/nakaokazaki.html,
# https://www.aikanrailway.co.jp/station/kitaokazaki.html,
# https://www.aikanrailway.co.jp/station/daimon.html,
# https://www.aikanrailway.co.jp/station/kitanomasuzuka.html,
# https://www.aikanrailway.co.jp/station/mikawakamigo.html,
# https://www.aikanrailway.co.jp/station/ekaku.html,
# https://www.aikanrailway.co.jp/station/suenohara.html,
# https://www.aikanrailway.co.jp/station/mikawatoyota.html,
# https://www.aikanrailway.co.jp/station/shinuwagoromo.html,
# https://www.aikanrailway.co.jp/station/shintoyota.html,
# https://www.aikanrailway.co.jp/station/daily_store.html,
# https://www.aikanrailway.co.jp/station/aikanumetsubo.html,
# https://www.aikanrailway.co.jp/station/shigou.html,
# https://www.aikanrailway.co.jp/station/kaizu.html,
# https://www.aikanrailway.co.jp/station/homi.html,
# https://www.aikanrailway.co.jp/station/sasabara.html,
# https://www.aikanrailway.co.jp/station/yakusa.html,
# https://www.aikanrailway.co.jp/station/yamaguchi.html,
# https://www.aikanrailway.co.jp/station/setoguchi.html,
# https://www.aikanrailway.co.jp/station/setoshi.html,
# https://www.aikanrailway.co.jp/station/nakamizuno.html,
# https://www.aikanrailway.co.jp/station/kouzouji.html]