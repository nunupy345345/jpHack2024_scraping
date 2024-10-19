from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_course_links(base_url):
    # Chromeドライバーの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモード（ブラウザが表示されない）
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Chromeドライバーをインストールして起動
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(base_url)

    # リンクを格納するリスト
    station_links = []

    # すべてのリンクを検索
    elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/station_info/line')]")
    print(elements)
    for element in elements:
        href = element.get_attribute('href')
        if href and '/train/station_info/' in href:
            full_url = 'https://www.meitetsu.co.jp' + href
            station_links.append(full_url)

    driver.quit()  # ブラウザを閉じる
    return station_links
def extract_station_info(station_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(station_url)

    station_info = {
        "station": "",
        "convenience": -1,
        "toilet": -1,
        "charge_machine": -1,
        "atm": -1,
        "coin_locker": -1,
        "convenience_kind": {}
    }

    # Extract the station name
    station_name_element = driver.find_element(By.CLASS_NAME, "station_name_class")  # Update with actual class name
    station_info["station"] = station_name_element.text

    # Parse accessibility info (example: 車いす対応エレベータ)
    elements = driver.find_elements(By.CLASS_NAME, "bfTxt")
    for element in elements:
        text = element.text
        status_element = element.find_element(By.XPATH, "following-sibling::span[@class='bfStatus']//img")
        status = status_element.get_attribute("src")

        # Check availability based on status image
        available = 1 if "ico_available" in status else 0

        if "車いす対応エレベータ" in text:
            station_info["convenience"] = available
        elif "エレベータ" in text:
            station_info["convenience_kind"]["エレベータ"] = available
        elif "エスカレータ" in text:
            station_info["convenience_kind"]["エスカレータ"] = available
        elif "車いす対応トイレ" in text:
            station_info["toilet"] = available
        elif "トイレ" in text:
            station_info["convenience_kind"]["トイレ"] = available
        elif "オストメイト対応トイレ" in text:
            station_info["convenience_kind"]["オストメイト対応トイレ"] = available
        elif "ベビーシート対応トイレ" in text:
            station_info["convenience_kind"]["ベビーシート対応トイレ"] = available
        elif "誘導ブロック" in text:
            station_info["convenience_kind"]["誘導ブロック"] = available
        elif "点字運賃表" in text:
            station_info["convenience_kind"]["点字運賃表"] = available
        elif "点字券売機" in text:
            station_info["charge_machine"] = available

    driver.quit()
    return station_info
  
if __name__ == "__main__":
  for i in range(1, 17):
    base_url = "https://www.meitetsu.co.jp/train/station_info/line{i:02d}/index.html"
    station_urls = get_course_links(base_url)
    print(station_urls)
    station_data = []

    for url in station_urls:
        info = extract_station_info(url)
        station_data.append(info)

    # JSONとして出力
    print(json.dumps(station_data, ensure_ascii=False, indent=2))
        # base_url = "https://www.meitetsu.co.jp/train/station_info/index.html"
        # course = get_course_links(base_url)
        # print(course)
        # courses.extend(course)
        # time.sleep(1)
        
        # for i in range(1,9):
        #   url = "https://ocw.u-tokyo.ac.jp/course-search/?start=" + str(i*21)
        #   course = get_course_links(url)
        #   courses.extend(course)
        #   time.sleep(1)
        
        # print(courses)