"""Make crime_type nullable

Revision ID: e4e6f3dd0ddf
Revises: 9cde48243b78
Create Date: 2025-10-09 00:04:50.243821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e4e6f3dd0ddf'
down_revision: Union[str, Sequence[str], None] = '9cde48243b78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Make crime_type nullable."""
    # Check if complaints table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'complaints' in inspector.get_table_names():
        # Check if crime_type column exists and is not nullable
        columns = {col['name']: col for col in inspector.get_columns('complaints')}

        if 'crime_type' in columns and not columns['crime_type']['nullable']:
            # Make crime_type nullable
            op.alter_column('complaints', 'crime_type',
                          existing_type=sa.VARCHAR(),
                          nullable=True)


def downgrade() -> None:
    """Downgrade schema: Make crime_type NOT nullable."""
    # Check if complaints table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'complaints' in inspector.get_table_names():
        columns = {col['name']: col for col in inspector.get_columns('complaints')}

        if 'crime_type' in columns and columns['crime_type']['nullable']:
            # Make crime_type NOT nullable (only if all values are not null)
            op.execute("UPDATE complaints SET crime_type = 'unknown' WHERE crime_type IS NULL")
            op.alter_column('complaints', 'crime_type',
                          existing_type=sa.VARCHAR(),
                          nullable=False)
