"""empty message

Revision ID: 1e32aa745b37
Revises: 098d9a3ab921
Create Date: 2025-05-23 22:55:43.724481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e32aa745b37'
down_revision: Union[str, None] = '098d9a3ab921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
