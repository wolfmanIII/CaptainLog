"""empty message

Revision ID: 098d9a3ab921
Revises: b7a21f0c2346
Create Date: 2025-05-23 22:51:55.918394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '098d9a3ab921'
down_revision: Union[str, None] = 'b7a21f0c2346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
