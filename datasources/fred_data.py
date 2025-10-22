# datasources/fred_data.py
from fredapi import Fred
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_fred_data():
    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key=api_key)
    try:
        oil = fred.get_series_latest_release("DCOILWTICO")
        rate = fred.get_series_latest_release("FEDFUNDS")
        nasdaq = fred.get_series_latest_release("NASDAQCOM")

        def latest_value(series):
            try:
                return round(float(series.iloc[-1]), 2)
            except Exception:
                return None

        return {
            "유가(WTI)": latest_value(oil),
            "연방금리": latest_value(rate),
            "나스닥지수": latest_value(nasdaq),
        }
    except Exception as e:
        print("⚠️ FRED API 오류:", e)
        return {}
