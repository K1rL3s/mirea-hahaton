"""type_to_protocol

Revision ID: 0006
Revises: 0005
Create Date: 2024-11-23 19:38:55.373440

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "open_ports",
        sa.Column("protocol", sa.String(length=36), nullable=False),
    )
    op.drop_column("open_ports", "type")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "open_ports",
        sa.Column("type", sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    )
    op.drop_column("open_ports", "protocol")
    # ### end Alembic commands ###
