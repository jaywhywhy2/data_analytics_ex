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

options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"])

url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

# ChromeDriver 경로를 지정하는 Service 객체 생성
# service = Service(ChromeDriverManager().install())
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# https://googlechromelabs.github.io/chrome-for-testing/
service = Service("chromedriver_142/chromedriver.exe")
chrome = webdriver.Chrome(service=service, options=options) 
chrome.get(url)
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 한국것만 선택
# label for=repNationNoKor 인것 클릭
label = find(wait, "label[for='repNationNoKor']")
label.click()

# .wrap_btn button.btn_blue 클릭
btn = find(wait, ".wrap_btn button.btn_blue")
btn.click()

html = chrome.page_source # 브라우저의 page 소스 저장

soup = BS(html, 'html.parser') 

items = soup.select(".tbl_comm tbody tr")
time.sleep(1)

# 도큐먼트 키 변수 정의
title = "영화제목"
o_date = "개봉일"
r_rate = "예배율"
s_price = "매출가격"

movies_list = []
for item in items:
  movie_doc = {}
  # title = item.select_one(".tbl_comm tbody td.tal a").text.strip()
  # open_date = item.select_one(".tbl_comm tbody td:nth-child(3)").text.strip()
  # reserve_rate = item.select_one(".tbl_comm tbody td:nth-child(5)").text.rstrip("%").strip()
  # sales_price = item.select_one(".tbl_comm tbody td:nth-child(7)").text.replace(",","").strip()
  movie_doc[title] = item.select_one(".tbl_comm tbody td.tal a").text.strip()
  movie_doc[o_date] = item.select_one(".tbl_comm tbody td:nth-child(3)").text.strip()
  movie_doc[r_rate] = item.select_one(".tbl_comm tbody td:nth-child(5)").text.rstrip("%").strip()
  movie_doc[s_price] = item.select_one(".tbl_comm tbody td:nth-child(7)").text.replace(",","").strip()

  movies_list.append(movie_doc)

print(movies_list)
# 몽고 DB 저장하기 위해 도큐먼트 만들기

chrome.quit() # tab 모두 종료

#### 다양한 엘리먼트 얻는 방법
# 참고 : https://wikidocs.net/177133