import time
import requests
from supabase import create_client
from datetime import datetime
import os

# Supabase 연결 정보 (Railway 환경변수로 설정 필요)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def run_uploader():
    try:
        # 최신 회차 하나만 가져오기
        url = "https://ntry.com/data/json/games/power_ladder/recent_result.json"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()[0]

        new_row = {
            "reg_date": data["date"],
            "date_round": int(data["round"]),
            "start_point": data["start"],
            "line_count": str(data["line"]),
            "odd_even": data["oe"]
        }

        # 중복 회차 체크
        exist = supabase.table("ladder").select("date_round").eq("date_round", new_row["date_round"]).execute()
        if exist.data:
            print(f"❌ {datetime.now()} - 회차 {new_row['date_round']} 이미 있음")
        else:
            supabase.table("ladder").insert(new_row).execute()
            print(f"✅ {datetime.now()} - 회차 {new_row['date_round']} 저장 완료")

    except Exception as e:
        print(f"❌ {datetime.now()} - 오류 발생: {e}")

if __name__ == "__main__":
    while True:
        run_uploader()
        time.sleep(60)  # ✅ 1분마다 실행
