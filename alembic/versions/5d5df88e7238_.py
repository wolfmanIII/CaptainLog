"""empty message

Revision ID: 5d5df88e7238
Revises: 8301880f9ae7
Create Date: 2025-05-23 22:07:42.087325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d5df88e7238'
down_revision: Union[str, None] = '8301880f9ae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
