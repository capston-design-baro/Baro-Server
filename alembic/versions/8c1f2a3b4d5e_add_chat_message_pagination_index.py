"""Add chat message pagination index

Revision ID: 8c1f2a3b4d5e
Revises: 2a8f7d5c9b31
Create Date: 2026-07-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c1f2a3b4d5e'
down_revision: Union[str, Sequence[str], None] = '2a8f7d5c9b31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


INDEX_NAME = "ix_chat_messages_complaint_id_id"


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'chat_messages' not in inspector.get_table_names():
        return

    indexes = [index['name'] for index in inspector.get_indexes('chat_messages')]
    if INDEX_NAME not in indexes:
        op.create_index(
            INDEX_NAME,
            'chat_messages',
            ['complaint_id', 'id'],
            unique=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'chat_messages' not in inspector.get_table_names():
        return

    indexes = [index['name'] for index in inspector.get_indexes('chat_messages')]
    if INDEX_NAME in indexes:
        op.drop_index(INDEX_NAME, table_name='chat_messages')
