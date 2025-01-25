"""Initial migration

Revision ID: 12d49107720c
Revises: 
Create Date: 2025-01-25 18:10:41.547248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12d49107720c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("Mobile No", sa.String(13)))
    op.add_column("user", sa.Column("cnic", sa.String(40)))
    op.add_column("user", sa.Column("University", sa.String(40)))
def downgrade() -> None:
    pass