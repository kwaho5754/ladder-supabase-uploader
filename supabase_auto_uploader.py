import requests
import os
from supabase import create_client, Client

# Supabase 환경변수
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")

# Supabase 클라이언트 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# JSON 데이터 주소
json_url = "https://ntry.com/data/json/games/power_ladder/recent_result.json"

try:
    # 전체 288개 중 가장 최신 회차 1개만 가져오기
    response = requests.get(json_url)
    response.raise_for_status()
    data = response.json()
    latest = data[0]  # 최신 회차는 항상 맨 앞

    # 필요한 필드 추출
    reg_date = latest["reg_date"]
    date_round = int(latest["date_round"])
    start_point = latest["start_point"]
    line_count = latest["line_count"]
    odd_even = latest["odd_even"]

    # Supabase에 동일 회차가 이미 존재하는지 확인
    result = supabase.table("ladder").select("date_round").eq("date_round", date_round).execute()

    if len(result.data) == 0:
        # 존재하지 않으면 삽입
        insert_data = {
            "reg_date": reg_date,
            "date_round": date_round,
            "start_point": start_point,
            "line_count": line_count,
            "odd_even": odd_even
        }
        supabase.table("ladder").insert(insert_data).execute()
        print(f"✅ 회차 {date_round} 저장됨")
    else:
        print(f"⏩ 회차 {date_round} 이미 있음 (중복 생략)")

except Exception as e:
    print(f"❌ 예외 발생: {e}")
