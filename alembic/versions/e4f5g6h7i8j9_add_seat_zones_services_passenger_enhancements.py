"""add seat zones, services, passenger enhancements

Revision ID: e4f5g6h7i8j9
Revises: d4e5f6a7b8c9
Create Date: 2026-06-26 10:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e4f5g6h7i8j9"
down_revision: Union[str, None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "seat_zones",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(20), nullable=False, unique=True),
        sa.Column("price_modifier", sa.Float(), nullable=False),
        sa.Column("description", sa.String(255)),
        sa.Column("color_hex", sa.String(7)),
    )

    op.create_table(
        "services",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("max_per_passenger", sa.Integer(), server_default="1"),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
    )

    op.create_table(
        "zone_service_eligibility",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("zone_id", sa.String(36), sa.ForeignKey("seat_zones.id"), nullable=False),
        sa.Column("service_id", sa.String(36), sa.ForeignKey("services.id"), nullable=False),
        sa.Column("age_group", sa.String(10), nullable=False),
        sa.UniqueConstraint("zone_id", "service_id", "age_group", name="uq_zone_service_age"),
    )

    op.create_table(
        "booking_services",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("booking_id", sa.String(36), sa.ForeignKey("bookings.id"), nullable=False),
        sa.Column("passenger_id", sa.String(36), sa.ForeignKey("passengers.id"), nullable=False),
        sa.Column("service_id", sa.String(36), sa.ForeignKey("services.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="1"),
        sa.Column("unit_price", sa.Float(), nullable=False),
    )

    op.add_column("seats", sa.Column("zone_id", sa.String(36), sa.ForeignKey("seat_zones.id")))

    op.add_column("passengers", sa.Column("seat_label", sa.String(10)))
    op.add_column("passengers", sa.Column("age_group", sa.String(10)))
    op.add_column("passengers", sa.Column("address", sa.String(255)))
    op.add_column("passengers", sa.Column("email", sa.String(100)))
    op.add_column("passengers", sa.Column("id_number", sa.String(50)))
    op.add_column("passengers", sa.Column("baggage_level", sa.String(20), server_default="none"))

    op.add_column("bookings", sa.Column("zone_price_total", sa.Float(), server_default="0"))
    op.add_column("bookings", sa.Column("service_total", sa.Float(), server_default="0"))
    op.add_column("bookings", sa.Column("baggage_total", sa.Float(), server_default="0"))


def downgrade() -> None:
    op.drop_table("booking_services")
    op.drop_table("zone_service_eligibility")
    op.drop_table("services")
    op.drop_table("seat_zones")

    op.drop_column("seats", "zone_id")

    op.drop_column("passengers", "baggage_level")
    op.drop_column("passengers", "id_number")
    op.drop_column("passengers", "email")
    op.drop_column("passengers", "address")
    op.drop_column("passengers", "age_group")
    op.drop_column("passengers", "seat_label")

    op.drop_column("bookings", "baggage_total")
    op.drop_column("bookings", "service_total")
    op.drop_column("bookings", "zone_price_total")
