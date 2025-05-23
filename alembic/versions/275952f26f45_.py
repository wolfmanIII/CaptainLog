"""empty message

Revision ID: 275952f26f45
Revises: e62a04fe177b
Create Date: 2025-05-23 22:57:39.551212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '275952f26f45'
down_revision: Union[str, None] = 'e62a04fe177b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
