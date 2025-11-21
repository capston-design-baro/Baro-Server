"""
암호화된 데이터를 검증하는 스크립트

사용법:
    python scripts/verify_encryption.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.services.encryption_service import encryption_service

def verify_users(session):
    """Users 테이블의 암호화 검증"""
    print("Users 테이블 암호화 검증 중...")

    result = session.execute(text("SELECT id, name, address, phone_number FROM users LIMIT 5"))
    users = result.fetchall()

    for user in users:
        user_id, name, address, phone_number = user

        # memoryview를 bytes로 변환
        if isinstance(name, memoryview):
            name = bytes(name)
        if isinstance(address, memoryview):
            address = bytes(address)
        if isinstance(phone_number, memoryview):
            phone_number = bytes(phone_number)

        print(f"\n사용자 ID {user_id}:")
        print(f"  - name (암호화됨): {name[:50]}..." if len(name) > 50 else f"  - name (암호화됨): {name}")

        try:
            # 복호화 테스트
            decrypted_name = encryption_service.decrypt_field(name)
            decrypted_address = encryption_service.decrypt_field(address)
            decrypted_phone = encryption_service.decrypt_field(phone_number)

            print(f"  - name (복호화): {decrypted_name}")
            print(f"  - address (복호화): {decrypted_address}")
            print(f"  - phone_number (복호화): {decrypted_phone}")
            print("  ✓ 암호화/복호화 성공")
        except Exception as e:
            print(f"  ✗ 복호화 실패: {str(e)}")

    print("\nUsers 테이블 검증 완료\n")


def verify_complaints(session):
    """Complaints 테이블의 암호화 검증"""
    print("Complaints 테이블 암호화 검증 중...")

    result = session.execute(text("""
        SELECT id, complainant_name, accused_name, crime_fact
        FROM complaints
        LIMIT 5
    """))
    complaints = result.fetchall()

    if not complaints:
        print("  검증할 고소장 데이터가 없습니다.\n")
        return

    for complaint in complaints:
        complaint_id, complainant_name, accused_name, crime_fact = complaint

        # memoryview를 bytes로 변환
        if isinstance(complainant_name, memoryview):
            complainant_name = bytes(complainant_name)
        if isinstance(accused_name, memoryview):
            accused_name = bytes(accused_name)
        if isinstance(crime_fact, memoryview):
            crime_fact = bytes(crime_fact)

        print(f"\n고소장 ID {complaint_id}:")

        try:
            # 복호화 테스트
            if complainant_name:
                dec_complainant = encryption_service.decrypt_field(complainant_name)
                print(f"  - 고소인 이름 (복호화): {dec_complainant}")

            if accused_name:
                dec_accused = encryption_service.decrypt_field(accused_name)
                print(f"  - 피고소인 이름 (복호화): {dec_accused}")

            if crime_fact:
                dec_crime = encryption_service.decrypt_field(crime_fact)
                print(f"  - 범죄사실 (복호화): {dec_crime[:50]}...")

            print("  ✓ 암호화/복호화 성공")
        except Exception as e:
            print(f"  ✗ 복호화 실패: {str(e)}")

    print("\nComplaints 테이블 검증 완료\n")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("암호화 검증 스크립트")
    print("=" * 60)
    print()

    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        verify_users(session)
        verify_complaints(session)

        print("=" * 60)
        print("모든 검증 완료!")
        print("=" * 60)
    except Exception as e:
        print(f"\n검증 중 오류 발생: {str(e)}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
