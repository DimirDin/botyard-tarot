"""
Shared reading-creation logic used by both the aiogram bot and the FastAPI
mini-app backend, so a reading created from either surface persists and
renders identically.
"""
import json
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db.models import User, Reading
from app.engine.deck import draw_spread
from app.engine.template_engine import assemble_full_reading


async def ensure_user(session: AsyncSession, telegram_id: int) -> User:
    user = await session.get(User, telegram_id)
    if user is None:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.commit()
    return user


async def create_reading(
    session: AsyncSession,
    telegram_id: int,
    spread_type: str,
    theme: Optional[str],
    question: Optional[str],
    is_yes_no_question: bool = False,
) -> Reading:
    await ensure_user(session, telegram_id)

    effective_theme = theme or "general"
    drawn = draw_spread(spread_type)
    assembled, full_text, yes_no = assemble_full_reading(
        drawn, theme=effective_theme, spread_type=spread_type, is_yes_no_question=is_yes_no_question,
    )

    cards_drawn_json = [
        {"card_id": dc.card_id, "upright": dc.upright, "position": dc.position}
        for dc in drawn
    ]

    if yes_no:
        full_text = f"Да/Нет: **{yes_no.capitalize()}**\n\n---\n\n" + full_text

    reading = Reading(
        user_id=telegram_id,
        question=question,
        theme=theme,
        spread_type=spread_type,
        cards_drawn=cards_drawn_json,
        rendered_reading=full_text,
    )
    session.add(reading)
    await session.commit()
    await session.refresh(reading)
    return reading


async def list_readings(session: AsyncSession, telegram_id: int, limit: int = 20):
    result = await session.execute(
        select(Reading)
        .where(Reading.user_id == telegram_id)
        .order_by(Reading.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()
