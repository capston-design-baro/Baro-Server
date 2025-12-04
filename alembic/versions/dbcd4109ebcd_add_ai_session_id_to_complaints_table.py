"""Add ai_session_id to complaints table

Revision ID: dbcd4109ebcd
Revises: e4e6f3dd0ddf
Create Date: 2025-10-09 01:33:33.282476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dbcd4109ebcd'
down_revision: Union[str, Sequence[str], None] = 'e4e6f3dd0ddf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if ai_session_id column already exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'complaints' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('complaints')]

        if 'ai_session_id' not in columns:
            # Add ai_session_id column to complaints table
            op.add_column('complaints', sa.Column('ai_session_id', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Check if ai_session_id column exists before dropping
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'complaints' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('complaints')]

        if 'ai_session_id' in columns:
            # Remove ai_session_id column from complaints table
            op.drop_column('complaints', 'ai_session_id')
