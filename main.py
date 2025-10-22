# ===============================================
# main.py — UAM Daily System (Save + Telegram Send)
# ===============================================
import os
from datetime import datetime
from dotenv import load_dotenv

# ✅ 변경된 부분
from analyzer.gpt_daily import analyze_daily  

from datasources.newsdata_io import fetch_uam_news
from datasources.fred_data import fetch_fred_data
from datasources.arxiv_data import fetch_arxiv_updates
from datasources.faa_feed import fetch_faa_updates
from common.telegram_bot import send_telegram_text

load_dotenv()
DATA_PATH = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_PATH, exist_ok=True)


def run_daily_report():
    print("🚀 UAM 일일 리포트 생성 중...\n")

    # 1️⃣ 뉴스
    news = fetch_uam_news()

    # 2️⃣ 거시경제
    try:
        fred_data = fetch_fred_data()
        print("✅ 거시경제 데이터 불러오기 완료")
    except Exception as e:
        fred_data = {}
        print("⚠️ FRED API 오류:", e)

    # 3️⃣ FAA / 논문
    faa = fetch_faa_updates()
    arxiv = fetch_arxiv_updates()

    # 4️⃣ GPT 분석
    print("🧠 GPT 리포트 생성 중...")
    today = datetime.now().strftime("%Y-%m-%d")
    report = analyze_daily({
        "news": news,
        "fred": fred_data,
        "faa": faa,
        "arxiv": arxiv,
    })

    # 5️⃣ 리포트 저장
    header = f"# UAM 일일 리포트 — {today}\n\n"
    full_text = header + report
    out_path = os.path.join(DATA_PATH, f"uam_daily_report_{today}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ 리포트 저장 완료: {out_path}")

    # 6️⃣ 텔레그램 발송
    print("📤 텔레그램 발송 중...\n")
    ok = send_telegram_text(f"📡 *UAM 일일 리포트 — {today}*\n\n" + report, parse_mode="Markdown")

    if ok:
        print("✅ 텔레그램 발송 완료")
    else:
        print("⚠️ 텔레그램 발송 실패")

    print("\n🎯 프로세스 완료!")


if __name__ == "__main__":
    run_daily_report()
