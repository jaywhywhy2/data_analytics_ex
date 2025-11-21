import requests
from bs4 import BeautifulSoup as BS

url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

res = requests.get(url)
soup = BS(res.text, "html.parser")

print(soup.select_one("tbody"))

# 동적 랜더링으로 데이터를 가져올 수 없음

#### 다양한 엘리먼트 얻는 방법
# 참고 : https://wikidocs.net/177133