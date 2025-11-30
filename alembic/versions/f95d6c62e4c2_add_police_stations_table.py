"""add_police_stations_table

Revision ID: f95d6c62e4c2
Revises: f56e0a1e53f6
Create Date: 2025-11-30 21:33:21.706054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f95d6c62e4c2'
down_revision: Union[str, Sequence[str], None] = 'f56e0a1e53f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'police_stations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('province', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('district', sa.String(), nullable=True),
        sa.Column('station_name', sa.String(), nullable=False),
        sa.Column('jurisdiction', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_police_stations_province'), 'police_stations', ['province'], unique=False)
    op.create_index(op.f('ix_police_stations_city'), 'police_stations', ['city'], unique=False)
    op.create_index(op.f('ix_police_stations_district'), 'police_stations', ['district'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_police_stations_district'), table_name='police_stations')
    op.drop_index(op.f('ix_police_stations_city'), table_name='police_stations')
    op.drop_index(op.f('ix_police_stations_province'), table_name='police_stations')
    op.drop_table('police_stations')
