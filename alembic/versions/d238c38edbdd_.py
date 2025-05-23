"""empty message

Revision ID: d238c38edbdd
Revises: 9d3ded5f2c98
Create Date: 2025-05-23 22:27:27.114404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd238c38edbdd'
down_revision: Union[str, None] = '9d3ded5f2c98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
