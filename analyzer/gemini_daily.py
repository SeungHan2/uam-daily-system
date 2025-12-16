import os
import google.generativeai as genai
from datetime import datetime

# API 키 설정 (GitHub Secrets에서 GEMINI_API_KEY를 받아와야 함)
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_daily(data):
    """
    수집된 데이터를 바탕으로 Gemini를 이용해 리포트를 생성합니다.
    """
    model = genai.GenerativeModel('gemini-2.5-flash') # 또는 gemini-1.5-pro

    # 데이터 언패킹 (없는 키는 빈 딕셔너리/리스트 처리)
    news = data.get("news", [])
    fred = data.get("fred", {})
    industry = data.get("industry", {})
    arxiv = data.get("arxiv", [])
    faa = data.get("faa", [])

    # 프롬프트 구성
    prompt = f"""
    당신은 UAM(Urban Air Mobility) 산업 전문 애널리스트입니다.
    오늘의 데이터를 바탕으로 투자자와 업계 관계자를 위한 브리핑 리포트를 작성하세요.

    [오늘 날짜] {datetime.now().strftime('%Y-%m-%d')}

    [작성 절대 규칙 (Strict Rules)]
    1. **마크다운 문법(#, *, **)을 절대 사용하지 마세요.** - 예: ### 제목 (X), **강조** (X)
       - 텔레그램에서 깨지지 않는 일반 텍스트와 이모지만 사용해야 합니다.
    2. 대신 아래의 [포맷 가이드]를 철저히 따르세요.

    [포맷 가이드]
    1. 핵심 요약 (Executive Summary)
       - 헤더: "📊 핵심 요약"
       - 내용: 가장 중요한 3가지를 숫자(1, 2, 3)로 요약.

    2. 주요 뉴스 (Industry News)
       - 헤더: "📰 주요 뉴스"
       - 각 뉴스 형식:
         🔹 [뉴스 제목 (한글 의역)]
         ▫️ 내용: 핵심 내용 1~2문장
         💡 인사이트: 산업/주가 영향 1문장
         (줄바꿈 후 다음 뉴스 작성)

    3. 기타 섹션
       - 기술 연구: "🔬 기술/논문 (Arxiv)"
       - 규제 정책: "⚖️ 규제/정책 (FAA)"
       - 데이터가 없으면 "특이사항 없음"으로 표기.

    4. 어조
       - 깔끔하고 전문적인 "해요체" 또는 "습니다체"를 유지하되, 개조식으로 간결하게 작성하세요.

    [데이터 소스]
    === 1. 주요 뉴스 ===
    {str(news)}

    === 2. 산업 리포트 ===
    {str(industry)}

    === 3. 거시경제 지표 (FRED) ===
    {str(fred)}

    === 4. 최신 논문 (Arxiv) ===
    {str(arxiv)}

    === 5. FAA 규제 업데이트 ===
    {str(faa)}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini 리포트 생성 중 오류 발생: {str(e)}"
