"""empty message

Revision ID: b7a21f0c2346
Revises: d238c38edbdd
Create Date: 2025-05-23 22:33:25.051281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7a21f0c2346'
down_revision: Union[str, None] = 'd238c38edbdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
