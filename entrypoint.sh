#!/bin/bash
set -e

echo "=== Starting Baro Backend ==="

# 1. 데이터베이스 마이그레이션
echo "Running database migrations..."
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
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
