from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.engine.reading_service import create_reading, list_readings
from app.engine.deck import SPREAD_POSITIONS

router = APIRouter(prefix="/api/readings", tags=["readings"])


class CreateReadingRequest(BaseModel):
    telegram_id: int
    spread_type: str
    theme: Optional[str] = "general"
    question: Optional[str] = None
    is_yes_no_question: bool = False


class ReadingResponse(BaseModel):
    id: int
    spread_type: str
    theme: Optional[str]
    question: Optional[str]
    cards_drawn: list
    rendered_reading: str
    created_at: str

    class Config:
        from_attributes = True


@router.post("", response_model=ReadingResponse)
async def api_create_reading(payload: CreateReadingRequest, session: AsyncSession = Depends(get_session)):
    if payload.spread_type not in SPREAD_POSITIONS:
        raise HTTPException(400, f"Unknown spread_type: {payload.spread_type}")
    reading = await create_reading(
        session,
        telegram_id=payload.telegram_id,
        spread_type=payload.spread_type,
        theme=payload.theme,
        question=payload.question,
        is_yes_no_question=payload.is_yes_no_question,
    )
    return ReadingResponse(
        id=reading.id,
        spread_type=reading.spread_type,
        theme=reading.theme,
        question=reading.question,
        cards_drawn=reading.cards_drawn,
        rendered_reading=reading.rendered_reading,
        created_at=reading.created_at.isoformat() if reading.created_at else "",
    )


@router.get("/{telegram_id}", response_model=List[ReadingResponse])
async def api_list_readings(telegram_id: int, session: AsyncSession = Depends(get_session)):
    readings = await list_readings(session, telegram_id)
    return [
        ReadingResponse(
            id=r.id, spread_type=r.spread_type, theme=r.theme, question=r.question,
            cards_drawn=r.cards_drawn, rendered_reading=r.rendered_reading,
            created_at=r.created_at.isoformat() if r.created_at else "",
        )
        for r in readings
    ]
