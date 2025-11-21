"""
Swagger 테스트 후 데이터베이스에 실제로 암호화되어 있는지 확인하는 스크립트

사용법:
    python scripts/check_db_encryption.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings

def check_latest_user():
    """가장 최근 생성된 사용자의 암호화 상태 확인"""
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        print("=" * 60)
        print("최근 사용자 데이터 확인")
        print("=" * 60)

        result = session.execute(text("""
            SELECT id, email, name, address, phone_number, created_at
            FROM users
            ORDER BY created_at DESC
            LIMIT 3
        """))

        users = result.fetchall()

        for user in users:
            user_id, email, name, address, phone_number, created_at = user

            # memoryview를 bytes로 변환
            if isinstance(name, memoryview):
                name = bytes(name)
            if isinstance(address, memoryview):
                address = bytes(address)
            if isinstance(phone_number, memoryview):
                phone_number = bytes(phone_number)

            print(f"\nID: {user_id}")
            print(f"Email: {email}")
            print(f"Created: {created_at}")
            print(f"Name (RAW): {name[:80]}..." if len(name) > 80 else f"Name (RAW): {name}")
            print(f"Address (RAW): {address[:80]}..." if len(address) > 80 else f"Address (RAW): {address}")
            print(f"Phone (RAW): {phone_number[:80]}..." if len(phone_number) > 80 else f"Phone (RAW): {phone_number}")

            # Fernet 암호화 데이터는 'gAAAAA'로 시작
            if isinstance(name, bytes) and name.startswith(b'gAAAAA'):
                print("✓ 암호화 확인됨 (Fernet)")
            else:
                print("✗ 암호화되지 않음 또는 평문")

        print("\n" + "=" * 60)

    finally:
        session.close()


def check_latest_complaint():
    """가장 최근 생성된 고소장의 암호화 상태 확인"""
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        print("\n" + "=" * 60)
        print("최근 고소장 데이터 확인")
        print("=" * 60)

        result = session.execute(text("""
            SELECT id,
                   complainant_name, complainant_address, complainant_office_address,
                   complainant_job, complainant_phone, complainant_home_phone, complainant_office_phone,
                   accused_name, accused_address, accused_office_address, accused_job,
                   accused_phone, accused_email, accused_etc,
                   crime_fact, complaint_reason, incident_summary,
                   created_at
            FROM complaints
            ORDER BY created_at DESC
            LIMIT 1
        """))

        complaints = result.fetchall()

        if not complaints:
            print("\n고소장 데이터가 없습니다.")
            return

        for complaint in complaints:
            complaint_id = complaint[0]
            created_at = complaint[18]

            print(f"\nID: {complaint_id}")
            print(f"Created: {created_at}")
            print("\n--- 고소인 정보 (7개 필드) ---")

            complainant_fields = [
                ("complainant_name", complaint[1]),
                ("complainant_address", complaint[2]),
                ("complainant_office_address", complaint[3]),
                ("complainant_job", complaint[4]),
                ("complainant_phone", complaint[5]),
                ("complainant_home_phone", complaint[6]),
                ("complainant_office_phone", complaint[7])
            ]

            for field_name, value in complainant_fields:
                check_field_encryption(field_name, value)

            print("\n--- 피고소인 정보 (7개 필드) ---")

            accused_fields = [
                ("accused_name", complaint[8]),
                ("accused_address", complaint[9]),
                ("accused_office_address", complaint[10]),
                ("accused_job", complaint[11]),
                ("accused_phone", complaint[12]),
                ("accused_email", complaint[13]),
                ("accused_etc", complaint[14])
            ]

            for field_name, value in accused_fields:
                check_field_encryption(field_name, value)

            print("\n--- 사건 정보 (3개 필드) ---")

            case_fields = [
                ("crime_fact (범죄사실)", complaint[15]),
                ("complaint_reason (고소이유)", complaint[16]),
                ("incident_summary (입증내용)", complaint[17])
            ]

            for field_name, value in case_fields:
                check_field_encryption(field_name, value)

        print("\n" + "=" * 60)

    finally:
        session.close()


def check_field_encryption(field_name, value):
    """개별 필드의 암호화 상태 확인"""
    if value is None:
        print(f"{field_name}: NULL")
        return

    # memoryview를 bytes로 변환
    if isinstance(value, memoryview):
        value = bytes(value)

    if isinstance(value, bytes):
        if value.startswith(b'gAAAAA'):
            print(f"{field_name}: ✓ 암호화됨")
        else:
            preview = value[:50] if len(value) > 50 else value
            print(f"{field_name}: ✗ 암호화되지 않음 ({preview}...)")
    else:
        print(f"{field_name}: ✗ 평문 ({value})")


if __name__ == "__main__":
    check_latest_user()
    check_latest_complaint()
