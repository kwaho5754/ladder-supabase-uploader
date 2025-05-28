import requests
import time

# ✅ Supabase 정보
SUPABASE_URL = "https://kfieqgyfuvvrnzawaffr.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtmaWVxZ3lmdXZ2cm56YXdhZmZyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODM3NTY5MSwiZXhwIjoyMDYzOTUxNjkxfQ.nXefrAvDEsBczHI5MEwWVZnCmW3B_B-ISxoftQu4NO8"

# ✅ Supabase에 회차 삽입
def insert_ladder(row):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    payload = {
        "회차": row["round"],
        "start_point": row["start"],
        "line_count": row["line"],
        "odd_even": row["oe"]
    }

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/ladder",
        headers=headers,
        json=payload
    )

    if res.status_code == 201:
        print(f"✅ 회차 {row['round']} 저장됨")
    elif res.status_code == 409:
        print(f"⏭ 회차 {row['round']} 이미 있음 (중복 생략)")
    else:
        print(f"❌ 저장 오류: {res.status_code} - {res.text}")

# ✅ 최신 회차 1줄 가져오기 (필드명 정확히 반영)
def fetch_latest_row():
    url = "https://ntry.com/data/json/games/power_ladder/recent_result.json"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                row = data[0]
                if all(k in row for k in ["date_round", "start_point", "line_count", "odd_even"]):
                    return {
                        "round": int(row["date_round"]),
                        "start": row["start_point"],
                        "line": int(row["line_count"]),
                        "oe": row["odd_even"]
                    }
                else:
                    print("⚠ 일부 필드 누락:", row)
            else:
                print("⚠ JSON 응답 비어 있음")
        else:
            print(f"❌ 요청 실패: {res.status_code}")
    except Exception as e:
        print(f"❌ 요청 예외: {e}")
    return None

# ✅ 5분마다 자동 실행 루프
def run_auto_upload():
    while True:
        row = fetch_latest_row()
        if row:
            insert_ladder(row)
        time.sleep(300)  # 5분 간격

# ✅ 실행 시작
if __name__ == "__main__":
    run_auto_upload()
