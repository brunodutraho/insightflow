"""fix subscriptions (safe + defensive)

Revision ID: bdcbd23e9f12
Revises: 1faf351df9a5
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers
revision: str = 'bdcbd23e9f12'
down_revision: Union[str, Sequence[str], None] = '1faf351df9a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    bind = op.get_bind()

    # =========================
    # SUBSCRIPTIONS
    # =========================

    if not column_exists("subscriptions", "started_at"):
        op.add_column("subscriptions", sa.Column("started_at", sa.DateTime(), nullable=True))

    if not column_exists("subscriptions", "updated_at"):
        op.add_column("subscriptions", sa.Column("updated_at", sa.DateTime(), nullable=True))

    if not column_exists("subscriptions", "stripe_subscription_id"):
        op.add_column("subscriptions", sa.Column("stripe_subscription_id", sa.String(), nullable=True))

    if not column_exists("subscriptions", "stripe_customer_id"):
        op.add_column("subscriptions", sa.Column("stripe_customer_id", sa.String(), nullable=True))

    if not column_exists("subscriptions", "discount_percent"):
        op.add_column("subscriptions", sa.Column("discount_percent", sa.Numeric(5, 2), nullable=True))

    if not column_exists("subscriptions", "discount_amount"):
        op.add_column("subscriptions", sa.Column("discount_amount", sa.Numeric(10, 2), nullable=True))

    # =========================
    # EMAIL CODE
    # =========================

    if not column_exists("email_verification_tokens", "code"):
        op.add_column(
            "email_verification_tokens",
            sa.Column("code", sa.String(length=6), nullable=True)
        )

    # =========================
    # PLAN LIMIT
    # =========================

    if not column_exists("plans", "max_requests_per_month"):
        op.add_column(
            "plans",
            sa.Column("max_requests_per_month", sa.Integer(), nullable=True)
        )


def downgrade() -> None:
    # opcional - pode manter simples ou ignorar
    pass