"""
Telegram Stars (XTR) invoice for the Celtic Cross / premium deep reading.
No other payment provider is used per product spec.
"""
from aiogram import Bot
from aiogram.types import LabeledPrice

from app.config import CELTIC_CROSS_STARS_PRICE

CELTIC_CROSS_PAYLOAD = "celtic_cross_unlock"


async def send_celtic_cross_invoice(bot: Bot, chat_id: int):
    await bot.send_invoice(
        chat_id=chat_id,
        title="Кельтский крест — глубокий расклад",
        description=(
            "Расклад на 10 карт с полным разбором позиций и совпадениями карт. "
            "Разовая разблокировка одного полного расклада."
        ),
        payload=CELTIC_CROSS_PAYLOAD,
        currency="XTR",
        prices=[LabeledPrice(label="Кельтский крест", amount=CELTIC_CROSS_STARS_PRICE)],
        provider_token="",  # not used for Telegram Stars (XTR)
    )
