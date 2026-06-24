"""change selected_seat to String(255) for multi-seat CSV

Revision ID: c8d9e0f1a2b3
Revises: b7b936239bd5
Create Date: 2026-06-24 10:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c8d9e0f1a2b3'
down_revision: Union[str, None] = 'b7b936239bd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'bookings',
        'selected_seat',
        type_=sa.String(255),
        existing_type=sa.String(10),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'bookings',
        'selected_seat',
        type_=sa.String(10),
        existing_type=sa.String(255),
        nullable=True,
    )
