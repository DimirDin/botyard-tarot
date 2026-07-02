"""initial schema: tarot_schema.users, tarot_schema.readings

Revision ID: 0001
Revises:
Create Date: 2026-07-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "tarot_schema"


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    op.create_table(
        "users",
        sa.Column("telegram_id", sa.BigInteger(), primary_key=True),
        sa.Column("is_premium", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        schema=SCHEMA,
    )

    op.create_table(
        "readings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey(f"{SCHEMA}.users.telegram_id"), nullable=False),
        sa.Column("question", sa.Text(), nullable=True),
        sa.Column("theme", sa.String(32), nullable=True),
        sa.Column("spread_type", sa.String(32), nullable=False),
        sa.Column("cards_drawn", postgresql.JSONB(), nullable=False),
        sa.Column("rendered_reading", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        schema=SCHEMA,
    )
    op.create_index("ix_readings_user_id", "readings", ["user_id"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_index("ix_readings_user_id", table_name="readings", schema=SCHEMA)
    op.drop_table("readings", schema=SCHEMA)
    op.drop_table("users", schema=SCHEMA)
    op.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE")
