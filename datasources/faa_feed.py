# --------------------------------------
# datasources/faa_feed.py
# --------------------------------------
import feedparser

def fetch_faa_updates():
    """FAA 뉴스 RSS에서 UAM 관련 규제 소식만 수집"""
    feed = feedparser.parse("https://www.faa.gov/news/rss")
    regs = [
        {"title": e.title, "summary": e.summary, "link": e.link}
        for e in feed.entries
        if any(k in e.title for k in ["UAM", "eVTOL", "air taxi", "AAM"])
    ]
    print(f"✅ FAA 관련 소식 {len(regs)}건 수집됨")
    return regs
