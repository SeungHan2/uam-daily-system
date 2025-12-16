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
    아래 제공된 데이터를 바탕으로 투자자와 업계 관계자를 위한 일일 브리핑 리포트를 작성하세요.

    [오늘 날짜] {datetime.now().strftime('%Y-%m-%d')}

    [작성 지침]
    1. **핵심 요약 (Executive Summary)**:
       - 가장 중요한 소식 3가지를 선정하여 짧고 강렬하게 요약하세요.
       - 번호를 매겨서(1., 2., 3.) 작성하세요.

    2. **주요 뉴스 (Industry News)**:
       - 뉴스를 주제별로 그룹화하지 말고, 개별 뉴스 단위로 나열하되 중요도 순으로 정렬하세요.
       - **가독성 최우선**: '제목:', '내용:', '인사이트:' 같은 라벨을 텍스트로 쓰지 마세요.
       - 아래 형식을 엄격히 따르세요:
         * **[뉴스 제목 (한글 번역)]**
           - 📄 **내용**: 핵심 내용 1~2문장 요약
           - 💡 **인사이트**: UAM 산업/주가에 미칠 영향 1문장
       - 기사 원문 제목이 영문이면 적절한 한글로 의역해서 제목으로 쓰세요.

    3. **기타 섹션**:
       - '기술 연구(Arxiv)', '규제/정책(FAA)' 등은 데이터가 없으면 "특이사항 없음"으로 짧게 처리하세요.
       - 데이터가 있다면 뉴스 섹션과 동일한 포맷을 유지하세요.

    4. **스타일**:
       - 전문적이지만 읽기 쉬운 어조를 사용하세요.
       - 불필요한 서론/결론(예: "이 리포트는...")은 생략하세요.

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
