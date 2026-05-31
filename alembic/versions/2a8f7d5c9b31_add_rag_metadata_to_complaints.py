"""Add RAG metadata to complaints

Revision ID: 2a8f7d5c9b31
Revises: 7f3a2b1c9d4e
Create Date: 2026-05-31 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a8f7d5c9b31'
down_revision: Union[str, Sequence[str], None] = '7f3a2b1c9d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'complaints' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('complaints')]

        if 'rag_keyword' not in columns:
            op.add_column('complaints', sa.Column('rag_keyword', sa.String(), nullable=True))

        if 'rag_cases' not in columns:
            op.add_column('complaints', sa.Column('rag_cases', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'complaints' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('complaints')]

        if 'rag_cases' in columns:
            op.drop_column('complaints', 'rag_cases')

        if 'rag_keyword' in columns:
            op.drop_column('complaints', 'rag_keyword')
