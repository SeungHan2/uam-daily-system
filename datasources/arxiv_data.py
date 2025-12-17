# --------------------------------------
# datasources/arxiv_data.py
# --------------------------------------
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

def fetch_arxiv_updates(max_results=5):
    """
    arXiv에서 UAM/eVTOL 관련 최신 논문 검색
    (재시도 로직 및 타임아웃 적용)
    """
    url = f"https://export.arxiv.org/api/query?search_query=all:(UAM+OR+eVTOL+OR+'air+mobility')&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"

    # 재시도(Retry) 전략 설정
    # total=3: 총 3회 재시도
    # backoff_factor=1: 재시도 간격 (1초, 2초, 4초... 대기)
    # status_forcelist: 500번대 서버 에러 시 재시도
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        # timeout을 30초로 설정하여 충분한 대기 시간 확보
        r = http.get(url, timeout=30)
        r.raise_for_status() # 200 OK가 아닐 경우 에러 발생시킴

        soup = BeautifulSoup(r.text, "xml")
        entries = soup.find_all("entry")
        results = []
        
        for e in entries:
            results.append({
                "title": e.title.text.strip(),
                "summary": e.summary.text.strip()[:300] + "...",
                "link": e.id.text.strip(),
            })
            
        print(f"✅ arXiv 논문 {len(results)}건 수집됨")
        return results

    except Exception as e:
        # 에러 발생 시 로그를 출력하고 빈 리스트 반환 (전체 프로그램 중단 방지)
        print(f"⚠️ arXiv 데이터 수집 실패 (건너뜀): {e}")
        return []
