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
    model = genai.GenerativeModel('gemini-1.5-flash') # 또는 gemini-1.5-pro

    # 데이터 언패킹 (없는 키는 빈 딕셔너리/리스트 처리)
    news = data.get("news", [])
    fred = data.get("fred", {})
    industry = data.get("industry", {})
    arxiv = data.get("arxiv", [])
    faa = data.get("faa", [])

    # 프롬프트 구성
    prompt = f"""
    당신은 UAM(Urban Air Mobility) 산업 전문 애널리스트입니다.
    아래 제공된 데이터를 바탕으로 일일 산업 동향 리포트를 작성해주세요.

    [오늘 날짜] {datetime.now().strftime('%Y-%m-%d')}

    [지침]
    1. **핵심 요약**: 뉴스, 논문, 산업 동향 중 가장 중요한 3가지를 먼저 요약하세요.
    2. **카테고리화**: '주요 뉴스', '기술 연구(Arxiv)', '규제/정책(FAA)' 등으로 나누어 정리하세요.
    3. **인사이트**: 단순 나열이 아니라, 이 소식이 UAM 산업에 미칠 영향을 한 줄 덧붙이세요.
    4. **형식**: Markdown 형식을 사용하여 가독성 있게 작성하세요 (볼드체, 리스트 등 활용).
    5. **제외**: 리포트의 마지막에 '결론'이나 '총평' 같은 의미 없는 요약 섹션은 작성하지 마세요.

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
