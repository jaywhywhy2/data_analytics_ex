#기본 import사항
from datetime import datetime
import os
import csv

def save_datas(data_keyword, head, movie_lists) :
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H")   # → 2025-11-17-13 형태

    # 폴더 / 파일명 설정
    folder = f"{data_keyword}_datas"
    filename = f"{timestamp}.csv" #날짜별로 파일명으로 저장하는 것
    # "movie_datas/2025-11-17-13.csv"와 같이 저장하도록 join하여 path 설정이 아래와 같음
    filepath = os.path.join(folder, filename)

    # 폴더 자동 생성 (없으면 생성)
    os.makedirs(folder, exist_ok=True)

    # CSV 저장 (2차원 리스트 여야함)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(head)  # 헤더 기록
        # 2차원 리스트인 movie_lists의 각 행을 파일에 기록
        writer.writerows(movie_lists)

    print("CSV 저장 완료:", filepath)