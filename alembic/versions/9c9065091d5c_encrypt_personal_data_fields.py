"""encrypt_personal_data_fields

Revision ID: 9c9065091d5c
Revises: 4a5a2a26a7ac
Create Date: 2025-11-22 00:04:34.777192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c9065091d5c'
down_revision: Union[str, Sequence[str], None] = '4a5a2a26a7ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: 개인정보 필드를 LargeBinary로 변경"""

    # Users 테이블 - 개인정보 필드 암호화
    # PostgreSQL에서는 USING 절을 사용하여 타입 변환
    op.execute('ALTER TABLE users ALTER COLUMN name TYPE BYTEA USING name::text::bytea')
    op.execute('ALTER TABLE users ALTER COLUMN address TYPE BYTEA USING address::text::bytea')
    op.execute('ALTER TABLE users ALTER COLUMN phone_number TYPE BYTEA USING phone_number::text::bytea')

    # Complaints 테이블 - 고소인 정보 암호화
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_name TYPE BYTEA USING complainant_name::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_address TYPE BYTEA USING complainant_address::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_office_address TYPE BYTEA USING complainant_office_address::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_job TYPE BYTEA USING complainant_job::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_phone TYPE BYTEA USING complainant_phone::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_home_phone TYPE BYTEA USING complainant_home_phone::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_office_phone TYPE BYTEA USING complainant_office_phone::text::bytea')

    # Complaints 테이블 - 피고소인 정보 암호화
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_name TYPE BYTEA USING accused_name::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_address TYPE BYTEA USING accused_address::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_office_address TYPE BYTEA USING accused_office_address::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_job TYPE BYTEA USING accused_job::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_phone TYPE BYTEA USING accused_phone::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_email TYPE BYTEA USING accused_email::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_etc TYPE BYTEA USING accused_etc::text::bytea')

    # Complaints 테이블 - 사건 정보 암호화
    op.execute('ALTER TABLE complaints ALTER COLUMN crime_fact TYPE BYTEA USING crime_fact::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN complaint_reason TYPE BYTEA USING complaint_reason::text::bytea')
    op.execute('ALTER TABLE complaints ALTER COLUMN incident_summary TYPE BYTEA USING incident_summary::text::bytea')


def downgrade() -> None:
    """Downgrade schema: LargeBinary를 다시 원래 타입으로 변경"""

    # Users 테이블
    op.execute('ALTER TABLE users ALTER COLUMN name TYPE VARCHAR USING encode(name, \'escape\')')
    op.execute('ALTER TABLE users ALTER COLUMN address TYPE VARCHAR USING encode(address, \'escape\')')
    op.execute('ALTER TABLE users ALTER COLUMN phone_number TYPE VARCHAR USING encode(phone_number, \'escape\')')

    # Complaints 테이블 - 고소인 정보
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_name TYPE VARCHAR USING encode(complainant_name, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_address TYPE TEXT USING encode(complainant_address, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_office_address TYPE TEXT USING encode(complainant_office_address, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_job TYPE VARCHAR USING encode(complainant_job, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_phone TYPE VARCHAR USING encode(complainant_phone, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_home_phone TYPE VARCHAR USING encode(complainant_home_phone, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complainant_office_phone TYPE VARCHAR USING encode(complainant_office_phone, \'escape\')')

    # Complaints 테이블 - 피고소인 정보
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_name TYPE VARCHAR USING encode(accused_name, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_address TYPE TEXT USING encode(accused_address, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_office_address TYPE TEXT USING encode(accused_office_address, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_job TYPE VARCHAR USING encode(accused_job, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_phone TYPE VARCHAR USING encode(accused_phone, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_email TYPE VARCHAR USING encode(accused_email, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN accused_etc TYPE TEXT USING encode(accused_etc, \'escape\')')

    # Complaints 테이블 - 사건 정보
    op.execute('ALTER TABLE complaints ALTER COLUMN crime_fact TYPE TEXT USING encode(crime_fact, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN complaint_reason TYPE TEXT USING encode(complaint_reason, \'escape\')')
    op.execute('ALTER TABLE complaints ALTER COLUMN incident_summary TYPE TEXT USING encode(incident_summary, \'escape\')')
