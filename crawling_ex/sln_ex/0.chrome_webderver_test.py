from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
import time

# 캐시 삭제
cache_path = os.path.expanduser("~/.wdm")
if os.path.exists(cache_path):
    shutil.rmtree(cache_path)

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# webdriver-manager 사용
service = Service(ChromeDriverManager().install())
# chrome = webdriver.Chrome(service=service, options=options)

# 다운로드한 chromedriver.exe 경로
# https://googlechromelabs.github.io/chrome-for-testing/
# service = Service("chromedriver_142/chromedriver.exe")
chrome = webdriver.Chrome(service=service, options=options)


chrome.get("https://www.kobis.or.kr")

print("-"*30)

time.sleep(5) # 간단한 delay, 파이썬 라이브러리
chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료