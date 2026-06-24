"""create passengers table

Revision ID: d4e5f6a7b8c9
Revises: c8d9e0f1a2b3
Create Date: 2026-06-24 11:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = 'c8d9e0f1a2b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'passengers',
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('booking_id', sa.String(36), sa.ForeignKey('bookings.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('mobile_phone', sa.String(20), nullable=False),
        sa.Column('date_of_birth', sa.Date, nullable=False),
        sa.Column('passport_number', sa.String(50), nullable=False),
        sa.Column('nationality', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('passengers')
