# ===============================================
# main.py — UAM Daily System (Save + Telegram Send)
# ===============================================
import os
from datetime import datetime
from dotenv import load_dotenv

# ✅ (1) GPT를 Gemini로 변경
# from analyzer.gpt_daily import analyze_daily
from analyzer.gemini_daily import analyze_daily # Gemini 분석기 사용으로 변경

from datasources.newsdata_io import fetch_uam_news
from datasources.fred_data import fetch_fred_data
from datasources.arxiv_data import fetch_arxiv_updates
from datasources.faa_feed import fetch_faa_updates
# ✅ (2) 리포트 보강을 위한 새로운 데이터 소스 추가 (예시)
from datasources.industry_reports import fetch_industry_reports 

from common.telegram_bot import send_telegram_text

load_dotenv()
DATA_PATH = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_PATH, exist_ok=True)


def run_daily_report():
    print("🚀 UAM 일일 리포트 생성 중...\n")

    # 1️⃣ 뉴스
    news = fetch_uam_news()

    # 2️⃣ 거시경제 (매일 큰 변화가 없으므로 주 1회(월요일)에만 포함)
    fred_data = {}
    today_weekday = datetime.now().weekday() # 0 = 월요일, 6 = 일요일

    if today_weekday == 0: # 월요일에만 실행 (주간 거시경제 리포트)
        try:
            fred_data = fetch_fred_data()
            print("✅ 거시경제 데이터 불러오기 완료 (월요일 리포트)")
        except Exception as e:
            print("⚠️ FRED API 오류:", e)
    else:
        print("⏭️ 거시경제 데이터 스킵 (월요일이 아님)")

    # 3️⃣ 새로운 소스 추가 (리포트 보강)
    try:
        industry_data = fetch_industry_reports()
        print("✅ 산업 동향 데이터 불러오기 완료")
    except Exception as e:
        industry_data = {}
        print("⚠️ 산업 동향 API 오류:", e)

    # 4️⃣ 논문 / FAA
    faa = fetch_faa_updates()
    arxiv = fetch_arxiv_updates()

    # 5️⃣ Gemini 분석에 전달할 데이터 준비
    print("🧠 Gemini 리포트 생성 중...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    analysis_data = {
        "news": news,
        "fred": fred_data, # 월요일이 아니면 빈 dict이 전달됨
        "industry": industry_data, # 새로 추가된 소스
        "arxiv": arxiv,
    }

    # ✅ (3) FAA/규제 정책은 변경사항이 있을 때만 언급 (fetch_faa_updates()가 변경 없으면 빈 값 반환 가정)
    if faa:
        analysis_data["faa"] = faa
        print("✅ FAA 업데이트 확인 (변경사항 있음)")
    else:
        print("⏭️ FAA 업데이트 스킵 (변경사항 없음)")
        
    
    report = analyze_daily(analysis_data)
    
    # ⚠️ 참고: analyze_daily 함수 내부의 프롬프트 설정을 수정하여
    # ✅ (4) 마지막에 의미 없는 요약 섹션을 생성하지 않도록 변경해야 합니다.

    # 6️⃣ 리포트 저장
    header = f"# UAM 일일 리포트 — {today}\n\n"
    full_text = header + report
    out_path = os.path.join(DATA_PATH, f"uam_daily_report_{today}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ 리포트 저장 완료: {out_path}")

    # 7️⃣ 텔레그램 발송
    print("📤 텔레그램 발송 중...\n")
    ok = send_telegram_text(f"📡 *UAM 일일 리포트 — {today}*\n\n" + report, parse_mode="Markdown")

    if ok:
        print("✅ 텔레그램 발송 완료")
    else:
        print("⚠️ 텔레그램 발송 실패")

    print("\n🎯 프로세스 완료!")


if __name__ == "__main__":
    run_daily_report()
