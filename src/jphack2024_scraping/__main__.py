from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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
    elements = driver.find_elements(By.XPATH, "//svg//g//a[@href]")
    print(elements)
    for element in elements:
        href = element.get_attribute('href')
        if href and '/train/station_info/' in href:
            full_url = 'https://www.meitetsu.co.jp' + href
            station_links.append(full_url)

    driver.quit()  # ブラウザを閉じる
    return station_links

if __name__ == "__main__":
        base_url = "https://www.meitetsu.co.jp/train/station_info/index.html"
        course = get_course_links(base_url)
        print(course)
        # courses.extend(course)
        # time.sleep(1)
        
        # for i in range(1,9):
        #   url = "https://ocw.u-tokyo.ac.jp/course-search/?start=" + str(i*21)
        #   course = get_course_links(url)
        #   courses.extend(course)
        #   time.sleep(1)
        
        # print(courses)