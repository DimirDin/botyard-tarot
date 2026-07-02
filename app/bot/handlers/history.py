from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.db.session import async_session
from app.engine.reading_service import list_readings
from app.bot.keyboards import SPREAD_LABELS

router = Router(name="history")


def _format_history(readings) -> str:
    if not readings:
        return "У вас пока нет сохранённых раскладов."
    lines = ["📜 *Ваши последние расклады:*\n"]
    for r in readings:
        label = SPREAD_LABELS.get(r.spread_type, r.spread_type)
        date = r.created_at.strftime("%d.%m.%Y %H:%M") if r.created_at else ""
        theme = r.theme or "—"
        lines.append(f"• {date} — {label} ({theme})")
    return "\n".join(lines)


@router.message(Command("history"))
async def cmd_history(message: Message):
    async with async_session() as session:
        readings = await list_readings(session, message.from_user.id)
    await message.answer(_format_history(readings), parse_mode="Markdown")


@router.callback_query(F.data == "history")
async def cb_history(callback: CallbackQuery):
    await callback.answer()
    async with async_session() as session:
        readings = await list_readings(session, callback.from_user.id)
    await callback.message.answer(_format_history(readings), parse_mode="Markdown")
