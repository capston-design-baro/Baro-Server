"""
기존 평문 데이터를 암호화하는 마이그레이션 스크립트

사용법:
    python scripts/migrate_encrypt_data.py
"""

import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.services.encryption_service import encryption_service

def migrate_users(session):
    """Users 테이블의 평문 데이터를 암호화"""
    print("Users 테이블 마이그레이션 시작...")

    # 평문 데이터 조회 (String 타입으로 저장된 데이터)
    result = session.execute(text("""
        SELECT id, name, address, phone_number
        FROM users
    """))

    users = result.fetchall()
    total = len(users)
    print(f"총 {total}개의 사용자 레코드 발견")

    for idx, user in enumerate(users, 1):
        user_id, name, address, phone_number = user

        # memoryview를 bytes로 변환 (PostgreSQL BYTEA 타입)
        if isinstance(name, memoryview):
            name = bytes(name)
        if isinstance(address, memoryview):
            address = bytes(address)
        if isinstance(phone_number, memoryview):
            phone_number = bytes(phone_number)

        # 이미 암호화된 데이터인지 확인 (Fernet 암호화 데이터는 gAAAAA로 시작)
        if isinstance(name, bytes) and name.startswith(b'gAAAAA'):
            print(f"사용자 ID {user_id}: 이미 암호화됨 (건너뛰기)")
            continue

        # bytes 타입이지만 암호화되지 않은 데이터 (스키마 변경 후 평문이 bytes로 변환됨)
        if isinstance(name, bytes):
            # bytes를 문자열로 디코딩
            name = name.decode('utf-8')
            address = address.decode('utf-8') if address else None
            phone_number = phone_number.decode('utf-8') if phone_number else None

        try:
            # 평문 데이터를 암호화
            encrypted_name = encryption_service.encrypt_field(name)
            encrypted_address = encryption_service.encrypt_field(address)
            encrypted_phone = encryption_service.encrypt_field(phone_number)

            # 업데이트
            session.execute(text("""
                UPDATE users
                SET name = :name, address = :address, phone_number = :phone_number
                WHERE id = :id
            """), {
                "id": user_id,
                "name": encrypted_name,
                "address": encrypted_address,
                "phone_number": encrypted_phone
            })

            print(f"[{idx}/{total}] 사용자 ID {user_id} 암호화 완료")

        except Exception as e:
            print(f"사용자 ID {user_id} 암호화 실패: {str(e)}")
            raise

    session.commit()
    print(f"Users 테이블 마이그레이션 완료\n")


def migrate_complaints(session):
    """Complaints 테이블의 평문 데이터를 암호화"""
    print("Complaints 테이블 마이그레이션 시작...")

    # 평문 데이터 조회
    result = session.execute(text("""
        SELECT id, complainant_name, complainant_address, complainant_office_address,
               complainant_job, complainant_phone, complainant_home_phone, complainant_office_phone,
               accused_name, accused_address, accused_office_address, accused_job,
               accused_phone, accused_email, accused_etc,
               crime_fact, complaint_reason, incident_summary
        FROM complaints
    """))

    complaints = result.fetchall()
    total = len(complaints)
    print(f"총 {total}개의 고소장 레코드 발견")

    for idx, complaint in enumerate(complaints, 1):
        complaint_id = complaint[0]

        # memoryview를 bytes로 변환
        complaint = list(complaint)
        for i in range(1, len(complaint)):
            if isinstance(complaint[i], memoryview):
                complaint[i] = bytes(complaint[i])

        # 첫 번째 필드가 이미 암호화되어 있는지 확인 (Fernet 암호화는 gAAAAA로 시작)
        if isinstance(complaint[1], bytes) and complaint[1].startswith(b'gAAAAA'):
            print(f"고소장 ID {complaint_id}: 이미 암호화됨 (건너뛰기)")
            continue

        try:
            # 각 필드를 암호화 (None 값은 그대로 유지)
            encrypted_data = {}

            fields = [
                'complainant_name', 'complainant_address', 'complainant_office_address',
                'complainant_job', 'complainant_phone', 'complainant_home_phone',
                'complainant_office_phone', 'accused_name', 'accused_address',
                'accused_office_address', 'accused_job', 'accused_phone',
                'accused_email', 'accused_etc', 'crime_fact', 'complaint_reason',
                'incident_summary'
            ]

            for i, field_name in enumerate(fields, 1):
                value = complaint[i]
                if value is not None:
                    # bytes 타입이면 문자열로 디코딩 (스키마 변경 후 평문이 bytes로 변환됨)
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    encrypted_data[field_name] = encryption_service.encrypt_field(value)
                else:
                    encrypted_data[field_name] = None

            # 업데이트
            session.execute(text("""
                UPDATE complaints
                SET complainant_name = :complainant_name,
                    complainant_address = :complainant_address,
                    complainant_office_address = :complainant_office_address,
                    complainant_job = :complainant_job,
                    complainant_phone = :complainant_phone,
                    complainant_home_phone = :complainant_home_phone,
                    complainant_office_phone = :complainant_office_phone,
                    accused_name = :accused_name,
                    accused_address = :accused_address,
                    accused_office_address = :accused_office_address,
                    accused_job = :accused_job,
                    accused_phone = :accused_phone,
                    accused_email = :accused_email,
                    accused_etc = :accused_etc,
                    crime_fact = :crime_fact,
                    complaint_reason = :complaint_reason,
                    incident_summary = :incident_summary
                WHERE id = :id
            """), {**encrypted_data, "id": complaint_id})

            print(f"[{idx}/{total}] 고소장 ID {complaint_id} 암호화 완료")

        except Exception as e:
            print(f"고소장 ID {complaint_id} 암호화 실패: {str(e)}")
            raise

    session.commit()
    print(f"Complaints 테이블 마이그레이션 완료\n")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("개인정보 암호화 마이그레이션 스크립트")
    print("=" * 60)
    print()

    # 데이터베이스 연결
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 1. Users 테이블 마이그레이션
        migrate_users(session)

        # 2. Complaints 테이블 마이그레이션
        migrate_complaints(session)

        print("=" * 60)
        print("모든 데이터 암호화 마이그레이션 완료!")
        print("=" * 60)

    except Exception as e:
        print(f"\n마이그레이션 중 오류 발생: {str(e)}")
        session.rollback()
        sys.exit(1)

    finally:
        session.close()


if __name__ == "__main__":
    main()
