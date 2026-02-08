"""Initial migration with users table including address

Revision ID: 9cde48243b78
Revises: 
Create Date: 2025-10-06 23:40:42.336489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cde48243b78'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy import inspect

def upgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)

    # users 테이블이 이미 있으면(이전 실패/부분 적용 등) 다시 만들지 않음
    if "users" in inspector.get_table_names():
        return

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("name", sa.LargeBinary(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("address", sa.LargeBinary(), nullable=False),
        sa.Column("phone_number", sa.LargeBinary(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 인덱스도 최초 생성시에만 만들기
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)

    # users가 없으면 내릴 것도 없음
    if "users" not in inspector.get_table_names():
        return

    # 인덱스 존재할 때만 삭제(안전)
    idx_names = {i["name"] for i in inspector.get_indexes("users")}
    if "ix_users_email" in idx_names:
        op.drop_index("ix_users_email", table_name="users")
    if "ix_users_id" in idx_names:
        op.drop_index("ix_users_id", table_name="users")

    op.drop_table("users")