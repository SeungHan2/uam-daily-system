# ==========================================
# 📦 common/telegram_bot.py
# ==========================================
import os
import requests
import time
from dotenv import load_dotenv

# 환경변수 로드 (.env에서 TOKEN과 CHAT_ID 가져옴)
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _split_message(text: str, max_length: int = 4000):
    """
    텔레그램 메시지 길이 제한(4096자)을 고려해 분할 전송
    """
    while text:
        yield text[:max_length]
        text = text[max_length:]


def send_telegram_text(text: str, parse_mode: str = "Markdown"):
    """
    텍스트 메시지를 텔레그램으로 전송
    - parse_mode='Markdown' 또는 None 가능
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ TELEGRAM_BOT_TOKEN 또는 CHAT_ID 환경변수가 설정되지 않았습니다.")
        return False

    ok = True
    for chunk in _split_message(text):
        try:
            resp = requests.post(
                f"{TG_API}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": chunk,
                    "parse_mode": parse_mode,
                },
                timeout=10,
            )
            if resp.status_code != 200:
                ok = False
                print(f"⚠️ 텔레그램 전송 실패: {resp.status_code} {resp.text}")
                break
            time.sleep(0.3)
        except Exception as e:
            ok = False
            print(f"⚠️ 텔레그램 전송 중 예외 발생: {e}")
            break

    if ok:
        print("✅ 텔레그램 전송 완료")
    return ok
