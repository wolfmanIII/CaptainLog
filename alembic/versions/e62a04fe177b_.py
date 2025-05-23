"""empty message

Revision ID: e62a04fe177b
Revises: 1e32aa745b37
Create Date: 2025-05-23 22:56:39.521119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e62a04fe177b'
down_revision: Union[str, None] = '1e32aa745b37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
