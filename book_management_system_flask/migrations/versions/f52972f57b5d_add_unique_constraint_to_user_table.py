"""Add unique constraint to user table

Revision ID: f52972f57b5d
Revises: 1677c62ff476
Create Date: 2024-08-30 12:09:35.200894

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "f52972f57b5d"
down_revision: Union[str, None] = "1677c62ff476"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_user_name", ["name"])


def downgrade() -> None:
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint("uq_user_name", type_="unique")
