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
    # Add district and jurisdiction columns to police_stations
    op.add_column('police_stations', sa.Column('district', sa.String(), nullable=True))
    op.add_column('police_stations', sa.Column('jurisdiction', sa.Text(), nullable=True))
    op.create_index(op.f('ix_police_stations_district'), 'police_stations', ['district'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove district and jurisdiction columns from police_stations
    op.drop_index(op.f('ix_police_stations_district'), table_name='police_stations')
    op.drop_column('police_stations', 'jurisdiction')
    op.drop_column('police_stations', 'district')
