# webdriver_manager 를 활용하여 크롬 드라이버 연결하기
## [usage : ]
## pip install webdriver-manager 설치 하기
## from webdriver_manager.chrome import ChromeDriverManager
## chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)
###############################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  
from bs4 import BeautifulSoup as BS
from my_lib import save_lib

options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"])

url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

# ChromeDriver 경로를 지정하는 Service 객체 생성
service = Service(ChromeDriverManager().install())
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# https://googlechromelabs.github.io/chrome-for-testing/
# service = Service("chromedriver_142/chromedriver.exe")
chrome = webdriver.Chrome(service=service, options=options) 
chrome.get(url)
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

try : 
    # 한국것만 선택
    # label for=repNationNoKor 인것 클릭
    label = find(wait, "label[for='repNationNoKor']")
    label.click()

    # .wrap_btn button.btn_blue 클릭
    btn = find(wait, ".wrap_btn button.btn_blue")
    btn.click()

    # 크롬 브라우저의 웹 페이지 소스를 변수에 저장함.
    html = chrome.page_source # 브라우저의 page 소스 저장
except Exception as e:
    print("에러 발생:", e)

# soup 객체로 생성하여 수집
soup = BS(html, 'html.parser') 

items = soup.select(".tbl_comm tbody tr")
time.sleep(1)


movie_lists = []
for item in items:
  title = item.select_one("tbody td.tal a").text.strip()
  open_date = item.select_one("tbody td:nth-child(3)").text.strip()
  reserve_rate = item.select_one("tbody td:nth-child(5)").text.rstrip("%").strip()
  sales_price = item.select_one("tbody td:nth-child(7)").text.replace(",","").strip()
  print(f"{title} | {open_date} | {reserve_rate} | {sales_price}")
  movie_lists.append([title, open_date, reserve_rate, sales_price])

#파일 저장하기
data_keyword = "film"
head = ["title","open_date","reserve_rate","sales_price"]
save_lib.save_datas(data_keyword, head, movie_lists)


print("-"*30)
chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료



#### 다양한 엘리먼트 얻는 방법
# 참고 : https://wikidocs.net/177133