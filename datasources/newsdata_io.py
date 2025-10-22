# --------------------------------------
# datasources/newsdata_io.py
# --------------------------------------
import os, requests, json, time
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_uam_news(limit_per_keyword=5):
    """여러 키워드별로 나눠서 요청 (NewsData.io의 422 방지)"""
    base_url = "https://newsdata.io/api/1/news"
    keywords = ["UAM", "eVTOL", "AAM", "air taxi", "urban air mobility", "Joby", "Archer", "EHang"]
    all_results = []

    for kw in keywords:
        params = {
            "apikey": API_KEY,
            "q": kw,
            "language": "en",
            "size": limit_per_keyword
        }
        try:
            r = requests.get(base_url, params=params, timeout=10)
            if r.status_code == 422:
                print(f"⚠️ '{kw}' 쿼리에서 422 오류 발생 — 건너뜀")
                continue
            r.raise_for_status()
            data = r.json()
            results = [
                {"title": it.get("title", ""), "description": it.get("description", ""), "source": kw}
                for it in data.get("results", [])
                if it.get("title") and it.get("description")
            ]
            print(f"✅ '{kw}' 관련 뉴스 {len(results)}건 수집")
            all_results.extend(results)
            time.sleep(0.5)  # API rate limit 보호
        except Exception as e:
            print(f"⚠️ '{kw}' 요청 중 오류 발생:", e)
            continue

    # 중복 제거 (제목 기준)
    unique = []
    seen = set()
    for n in all_results:
        if n["title"] not in seen:
            seen.add(n["title"])
            unique.append(n)

    print(f"📦 총 {len(unique)}건의 UAM 관련 뉴스 통합 수집 완료")
    return unique
