from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.bot.keyboards import main_menu_kb, theme_kb
from app.db.session import async_session
from app.engine.reading_service import ensure_user

router = Router(name="start")

WELCOME = (
    "🔮 *taroT*\n\n"
    "Оффлайн-бот для расклада Таро: без обращений к внешним API, всё "
    "работает мгновенно на локальной базе значений карт.\n\n"
    "Выберите расклад:"
)


class ReadingFlow(StatesGroup):
    waiting_for_question = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    async with async_session() as session:
        await ensure_user(session, message.from_user.id)
    await state.clear()
    await message.answer(WELCOME, reply_markup=main_menu_kb(), parse_mode="Markdown")


@router.callback_query(F.data == "spread:advice_of_day")
async def advice_of_day(callback: CallbackQuery, state: FSMContext):
    from app.engine.reading_service import create_reading

    await callback.answer("Тяну карту дня...")
    async with async_session() as session:
        reading = await create_reading(
            session, callback.from_user.id, spread_type="one_card", theme="general",
            question=None, is_yes_no_question=False,
        )
    await callback.message.answer(f"✨ *Совет дня*\n\n{reading.rendered_reading}", parse_mode="Markdown")


@router.callback_query(F.data.startswith("spread:"))
async def choose_spread(callback: CallbackQuery, state: FSMContext):
    spread_type = callback.data.split(":", 1)[1]
    if spread_type == "advice_of_day":
        return  # handled above
    await state.update_data(spread_type=spread_type)
    await callback.answer()
    await callback.message.answer(
        "На какую тему хотите расклад?", reply_markup=theme_kb(spread_type)
    )
