import datetime
from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.config import DB_SCHEMA


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": DB_SCHEMA}

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_premium: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    readings: Mapped[list["Reading"]] = relationship(back_populates="user")


class Reading(Base):
    __tablename__ = "readings"
    __table_args__ = {"schema": DB_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{DB_SCHEMA}.users.telegram_id"))
    question: Mapped[str] = mapped_column(Text, nullable=True)
    theme: Mapped[str] = mapped_column(String(32), nullable=True)
    spread_type: Mapped[str] = mapped_column(String(32))
    cards_drawn: Mapped[dict] = mapped_column(JSONB)
    rendered_reading: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="readings")
