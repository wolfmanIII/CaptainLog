"""empty message

Revision ID: 9d3ded5f2c98
Revises: 5d5df88e7238
Create Date: 2025-05-23 22:26:23.452109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d3ded5f2c98'
down_revision: Union[str, None] = '5d5df88e7238'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
