import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def crawl_nara_jangteo(keyword, start_date, end_date):
    # 검색어와 기간을 URL에 포함시켜서 검색 결과 페이지에 접속
    url = f"https://www.g2b.go.kr/index.jsp/main/search/searchGeneral.do?searchType=1&keyword={keyword}&fromBidDt={start_date}&toBidDt={end_date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 검색 결과를 추출하여 데이터프레임으로 저장
    results = []
    items = soup.select('.tbl_wrap tbody tr')
    for item in items:
        title = item.select_one('.tl a').text.strip()
        date = item.select_one('.bdate').text.strip()
        results.append({'Title': title, 'Date': date})
    df = pd.DataFrame(results)

    # 데이터프레임을 파일로 저장
    df.to_csv('search_results.txt', index=False, sep='\t')  # txt 파일로 저장
    df.to_excel('search_results.xls', index=False)  # xls 파일로 저장

# 크롤러 실행
crawl_nara_jangteo("검색어", "시작일", "종료일")
