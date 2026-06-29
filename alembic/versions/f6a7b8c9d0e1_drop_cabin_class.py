"""drop cabin_class from seats, bookings, flights

Revision ID: f6a7b8c9d0e1
Revises: e4f5g6h7i8j9
Create Date: 2026-06-29 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, None] = "e4f5g6h7i8j9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("seats", "cabin_class")
    op.drop_column("bookings", "cabin_class")
    op.drop_column("flights", "cabin_class")


def downgrade() -> None:
    op.add_column("flights", sa.Column("cabin_class", sa.String(20), nullable=True))
    op.add_column("bookings", sa.Column("cabin_class", sa.String(20), nullable=False, server_default="economy"))
    op.add_column("seats", sa.Column("cabin_class", sa.String(20), nullable=False, server_default="economy"))
