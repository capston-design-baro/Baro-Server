"""Make user address and phone nullable

Revision ID: 7f3a2b1c9d4e
Revises: eda74b57f2cd
Create Date: 2026-05-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f3a2b1c9d4e'
down_revision: Union[str, Sequence[str], None] = 'eda74b57f2cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Allow optional address and phone number during registration."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'users' not in inspector.get_table_names():
        return

    columns = {col['name']: col for col in inspector.get_columns('users')}

    if 'address' in columns and not columns['address'].get('nullable', True):
        op.alter_column('users', 'address', existing_type=sa.LargeBinary(), nullable=True)

    if 'phone_number' in columns and not columns['phone_number'].get('nullable', True):
        op.alter_column('users', 'phone_number', existing_type=sa.LargeBinary(), nullable=True)


def downgrade() -> None:
    """Restore required address and phone number constraints."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'users' not in inspector.get_table_names():
        return

    columns = {col['name']: col for col in inspector.get_columns('users')}

    if 'address' in columns and columns['address'].get('nullable', True):
        op.alter_column('users', 'address', existing_type=sa.LargeBinary(), nullable=False)

    if 'phone_number' in columns and columns['phone_number'].get('nullable', True):
        op.alter_column('users', 'phone_number', existing_type=sa.LargeBinary(), nullable=False)
