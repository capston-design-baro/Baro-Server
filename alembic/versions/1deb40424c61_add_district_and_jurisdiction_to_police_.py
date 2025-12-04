"""add_district_and_jurisdiction_to_police_station

Revision ID: 1deb40424c61
Revises: f95d6c62e4c2
Create Date: 2025-11-30 22:13:16.240865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1deb40424c61'
down_revision: Union[str, Sequence[str], None] = 'f95d6c62e4c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'police_stations' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('police_stations')]
        indexes = [idx['name'] for idx in inspector.get_indexes('police_stations')]

        # Add district and jurisdiction columns if they don't exist
        # Note: These columns are already created in f95d6c62e4c2, so this might be redundant
        if 'district' not in columns:
            op.add_column('police_stations', sa.Column('district', sa.String(), nullable=True))
        if 'jurisdiction' not in columns:
            op.add_column('police_stations', sa.Column('jurisdiction', sa.Text(), nullable=True))

        # Create index if it doesn't exist
        if 'ix_police_stations_district' not in indexes:
            op.create_index(op.f('ix_police_stations_district'), 'police_stations', ['district'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'police_stations' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('police_stations')]
        indexes = [idx['name'] for idx in inspector.get_indexes('police_stations')]

        # Remove district and jurisdiction columns if they exist
        if 'ix_police_stations_district' in indexes:
            op.drop_index(op.f('ix_police_stations_district'), table_name='police_stations')
        if 'jurisdiction' in columns:
            op.drop_column('police_stations', 'jurisdiction')
        if 'district' in columns:
            op.drop_column('police_stations', 'district')
