#!/bin/sh
set -e

echo "=== Starting Baro Backend ==="

PORT="${PORT:-8000}"

# 1. 데이터베이스 마이그레이션 (재시도)
echo "Running database migrations..."
for i in 1 2 3 4 5; do
  if alembic upgrade head; then
    echo "Migrations applied."
    break
  fi
  echo "Migration failed, retrying ($i/5) ..."
  sleep 5
done
# 5번 재시도 후에도 실패면 여기서 종료되게 한 번 더 실행
alembic upgrade head

# 2. 경찰서 데이터 확인 및 삽입
echo "Checking police stations data..."
python -c "
from app.database import SessionLocal
from app.models.police_station import PoliceStation

db = SessionLocal()
count = db.query(PoliceStation).count()
db.close()

if count == 0:
    print('Police stations data not found. Inserting...')
    import subprocess
    import sys
    subprocess.run([sys.executable, '-m', 'scripts.seed_police_stations'], check=True)
else:
    print(f'Police stations data already exists ({count} records). Skipping.')
"

# 3. FastAPI 서버 시작
echo \"Starting FastAPI server on port ${PORT}...\"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" --proxy-headers --forwarded-allow-ips="*"
