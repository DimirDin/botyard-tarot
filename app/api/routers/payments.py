from fastapi import APIRouter
from aiogram import Bot
from aiogram.types import LabeledPrice

from app.config import BOT_TOKEN, CELTIC_CROSS_STARS_PRICE
from app.payments.stars import CELTIC_CROSS_PAYLOAD

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.post("/celtic_cross_invoice_link")
async def celtic_cross_invoice_link():
    """
    Creates a Telegram Stars (XTR) invoice link for the Celtic Cross unlock, so the
    Mini App can call tg.WebApp.openInvoice(link) directly (with the mandatory 80ms
    delay after the user's tap, per platform Mini App rules).
    """
    bot = Bot(token=BOT_TOKEN)
    try:
        link = await bot.create_invoice_link(
            title="Кельтский крест — глубокий расклад",
            description="Расклад на 10 карт с полным разбором позиций и совпадениями карт.",
            payload=CELTIC_CROSS_PAYLOAD,
            currency="XTR",
            prices=[LabeledPrice(label="Кельтский крест", amount=CELTIC_CROSS_STARS_PRICE)],
        )
    finally:
        await bot.session.close()
    return {"invoice_link": link}
