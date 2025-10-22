# --------------------------------------
# datasources/arxiv_data.py
# --------------------------------------
import requests
from bs4 import BeautifulSoup

def fetch_arxiv_updates(max_results=5):
    """arXiv에서 UAM/eVTOL 관련 최신 논문 검색"""
    url = f"https://export.arxiv.org/api/query?search_query=all:(UAM+OR+eVTOL+OR+'air+mobility')&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    r = requests.get(url, timeout=10)
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
