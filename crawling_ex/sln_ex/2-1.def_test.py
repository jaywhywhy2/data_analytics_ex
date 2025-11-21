# webdriver_manager 를 활용하여 크롬 드라이버 연결하기
# selenium-4.6.0, chrome-driver 142.0.7444
# selenium-4.38.0, chrome-driver 114.0.5735.90
## [usage : ]
## pip install webdriver-manager 설치 하기
## from webdriver_manager.chrome import ChromeDriverManager
## chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)
###############################################################################
# 1. 필요한 라이브러리 로드
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  

import my_lib.save_lib as save_lib  # save_lib.py 파일을 모듈로 불러오기
#혹은 from my_lib import save_lib


# 2.크롬브라우저 옵션을 정의  
options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("--no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
# options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 1, 2번까지는 기본적인 설정이기 때문에 복붙해서 쓰면 되고, 순서도 상관 없음!

# 3. 크롬 웹드라이브를 통한 크롬 브라우저 객체 생성
# 방법1. webdriver-manager 사용해서 자동으로 다운로드 할 수 있게(현재 설치된 최신버전으로 다운로드 됨)
# ChromeDriver 경로를 지정하는 Service 객체 생성
service = Service(ChromeDriverManager().install())

# 방법2. 자동 다운이 안될때 직접 지정된 경로에서 다운로드 받을 수 있도록 메뉴얼하게 지정해주는 방법.
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# https://googlechromelabs.github.io/chrome-for-testing/
# service = Service("chromedriver_142/chromedriver.exe")

# 크롬 브라우저 객체 생성됨. Chrome은 브라우저 객체 식별자.
chrome = webdriver.Chrome(service=service, options=options) 

# 4. 데이터 수집할 웹 주소
url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

chrome.get(url)  # 웹 페이지 열기
time.sleep(1)  # 페이지 로딩 대기 (필요에 따라 조정)

# 지정한 요소가 브라우저에 로딩될때까지 기다림, 최대 10초
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 5. 데이터 수집 : 할 부분에 대한 검색 액션 수행
try :
    ## 한국 영화만 선택, 해외 체크박스 해제를 액션 지정
    # 셀렉터 지정방법 2가지
    # ul.list_idx li input#repNationNoKor  <<input 박스를 체크하는 방법
    # ul.list_idx li label[for = 'repNationNoKor'] <<레이블링을 해주는 방법
    # find(wait, "셀렉터") : 셀렉터가 될때까지 기다려라
    ele = find(wait, "label[for='repNationNoKor']") #지정 셀렉터 요소가 로딩될때까지 기다리기, 로딩되면 요소를 return
    ele.click() # return 받은 ele을 클릭 액션 수행

    # 조회버튼 로딩되면 클릭하기
    btn = find(wait, ".wrap_btn button.btn_blue")
    btn.click()

    # 조회된 데이터에서 필요한 데이터 수집하기
    # 각 영화 데이터를 list로 추출하기 (tbody tr을 목록으로 추출)
    time.sleep(2) #크롤링한 데이터 요소가 로딩되는 시간까지 기다림.
    items = chrome.find_elements(By.CSS_SELECTOR, "table.tbl_comm tbody tr")
    # items에 지정한 코드를 해석하면 : 해당 주소에서 찾는 건데, table 이름이 tbl_comm인 곳의 tbody 안에 있는 tr 요소들 모두를 찾아라.
    
    print("영화제목|개봉일|매출액|관객수")
    movie_lists = []  # CSV 저장용 2차원 리스트
    print("-"*30)
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        sales = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
        sizes = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text
        # title과 date는 tr 안에서 td가 두번째인 요소의 텍스트를 추출해라 라는 뜻

        if not date :
            date = "-"  # 개봉일 데이터가 없을 경우 -로 처리

        #print(f"{title}|{date}|{sales}|{sizes}")
        movie_lists.append([title, date, sales, sizes])  # 2차원 리스트에 추가

    # 데이터가 로딩될때까지 잠시 대기
    # time.sleep(5)
    print("-"*30)
except Exception as e:
    print("오류",e)

# 파일로 저장하기(.csv)
# 6. 리스트 -> 파일에 저장
#함수 호출부
data_keyword = "movie"
head = ["title","date","sales","size"]
save_lib.save_datas(data_keyword, head, movie_lists)

chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료