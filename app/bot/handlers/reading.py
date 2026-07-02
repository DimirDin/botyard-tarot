from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery
from aiogram.fsm.context import FSMContext

from app.bot.keyboards import webapp_button_kb
from app.db.session import async_session
from app.engine.reading_service import create_reading
from app.payments.stars import send_celtic_cross_invoice, CELTIC_CROSS_PAYLOAD

router = Router(name="reading")


@router.callback_query(F.data.startswith("theme:"))
async def choose_theme(callback: CallbackQuery, state: FSMContext, bot: Bot):
    _, spread_type, theme = callback.data.split(":", 2)
    await callback.answer()

    if spread_type == "celtic_cross":
        await state.update_data(pending_spread_type=spread_type, pending_theme=theme)
        await callback.message.answer(
            "Кельтский крест — это глубокий расклад на 10 карт с разбором позиций и "
            "совпадений между картами. Разовая разблокировка через Telegram Stars."
        )
        await send_celtic_cross_invoice(bot, callback.from_user.id)
        return

    await callback.message.answer("Раскладываю карты... 🌌")
    async with async_session() as session:
        reading = await create_reading(
            session, callback.from_user.id, spread_type=spread_type, theme=theme,
            question=None, is_yes_no_question=False,
        )
    await callback.message.answer(reading.rendered_reading, parse_mode="Markdown", reply_markup=webapp_button_kb())


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    if pre_checkout_query.invoice_payload == CELTIC_CROSS_PAYLOAD:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Неизвестный товар")


@router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    theme = data.get("pending_theme", "general")

    await message.answer("Оплата прошла успешно! Раскладываю Кельтский крест... 🌌✨")
    async with async_session() as session:
        reading = await create_reading(
            session, message.from_user.id, spread_type="celtic_cross", theme=theme,
            question=None, is_yes_no_question=False,
        )
    await message.answer(reading.rendered_reading, parse_mode="Markdown", reply_markup=webapp_button_kb())
    await state.update_data(pending_spread_type=None, pending_theme=None)
