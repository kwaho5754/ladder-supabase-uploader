# main.py
from flask import Flask
from supabase import create_client
import requests
import os
from datetime import datetime

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

@app.route("/run")
def run_uploader():
    try:
        url = "https://ntry.com/data/json/games/power_ladder/recent_result.json"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()[0]  # 최신 회차 하나만

        new_row = {
            "reg_date": data["date"],
            "date_round": int(data["round"]),
            "start_point": data["start"],
            "line_count": str(data["line"]),
            "odd_even": data["oe"]
        }

        exist = supabase.table("ladder").select("date_round").eq("date_round", new_row["date_round"]).execute()
        if exist.data:
            return f"❌ 회차 {new_row['date_round']} 이미 있음 (중복 생밟)"

        supabase.table("ladder").insert(new_row).execute()
        return f"✅ 회차 {new_row['date_round']} 저장 확인"

    except Exception as e:
        return f"❌ 오류: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
