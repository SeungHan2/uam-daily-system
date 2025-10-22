# --------------------------------------
# analyzer/gpt_daily.py
# --------------------------------------
from openai import OpenAI
from common.prompts_daily import DAILY_REPORT_PROMPT_KO

def analyze_daily(inputs: dict, model="gpt-4o"):
    """
    inputs = {
      "news": [...],
      "fred": {...},
      "faa": [...],
      "arxiv": [...]
    }
    """
    client = OpenAI()

    # 입력 텍스트 구성
    text = "=== 뉴스 ===\n"
    for n in inputs["news"]:
        text += f"- {n['title']}\n{n['description']}\n\n"

    text += "=== 거시경제 ===\n" + "\n".join([f"{k}: {v}" for k, v in inputs["fred"].items()]) + "\n\n"

    text += "=== 규제/정책 ===\n"
    for f in inputs["faa"]:
        text += f"- {f['title']}\n{f['summary']}\n\n"

    text += "=== 연구/논문 ===\n"
    for a in inputs["arxiv"]:
        text += f"- {a['title']}\n{a['summary']}\n\n"

    messages = [
        {"role": "system", "content": "당신은 한국어로만 응답하는 UAM 산업 전문 분석가입니다."},
        {"role": "user", "content": DAILY_REPORT_PROMPT_KO + "\n\n" + text}
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4
    )
    result = resp.choices[0].message.content.strip()
    return result
