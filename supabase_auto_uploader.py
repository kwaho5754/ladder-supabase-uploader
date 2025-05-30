import time
import requests
from supabase import create_client
from datetime import datetime
import os

# ✅ Supabase 연결 설정
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def run_uploader():
    try:
        # ✅ 최신 회차 JSON 불러오기
        url = "https://ntry.com/data/json/games/power_ladder/recent_result.json"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()[0]

        # ✅ 저장할 row 생성
        new_row = {
            "reg_date": data["reg_date"],
            "date_round": int(data["date_round"]),
            "start_point": data["start_point"],
            "line_count": str(data["line_count"]),
            "odd_even": data["odd_even"]
        }

        # ✅ 중복 검사: reg_date + date_round 기준
        exist = (
            supabase.table("ladder")
            .select("*")
            .eq("reg_date", new_row["reg_date"])
            .eq("date_round", new_row["date_round"])
            .execute()
        )

        if exist.data:
            print(f"❌ {datetime.now()} - {new_row['reg_date']} 회차 {new_row['date_round']} 이미 있음")
        else:
            supabase.table("ladder").insert(new_row).execute()
            print(f"✅ {datetime.now()} - {new_row['reg_date']} 회차 {new_row['date_round']} 저장 완료")

    except Exception as e:
        print(f"❌ {datetime.now()} - 오류 발생: {e}")

# ✅ 60초마다 자동 실행
if __name__ == "__main__":
    while True:
        run_uploader()
        time.sleep(60)
