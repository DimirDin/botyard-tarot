from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from app.config import WEBAPP_URL

THEME_LABELS = {
    "general": "Общий вопрос",
    "love": "Любовь и отношения",
    "career": "Карьера и работа",
    "finance": "Финансы",
    "health": "Здоровье",
    "spirit": "Духовность",
}

SPREAD_LABELS = {
    "one_card": "1 карта — быстрый совет",
    "three_card": "3 карты — прошлое/настоящее/будущее",
    "celtic_cross": "Кельтский крест (10 карт) ⭐ премиум",
    "advice_of_day": "Совет дня",
}


def main_menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=SPREAD_LABELS["advice_of_day"], callback_data="spread:advice_of_day")],
        [InlineKeyboardButton(text=SPREAD_LABELS["one_card"], callback_data="spread:one_card")],
        [InlineKeyboardButton(text=SPREAD_LABELS["three_card"], callback_data="spread:three_card")],
        [InlineKeyboardButton(text=SPREAD_LABELS["celtic_cross"], callback_data="spread:celtic_cross")],
        [InlineKeyboardButton(text="🌌 Открыть приложение", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="📜 История раскладов", callback_data="history")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def theme_kb(spread_type: str) -> InlineKeyboardMarkup:
    rows = []
    for key, label in THEME_LABELS.items():
        rows.append([InlineKeyboardButton(text=label, callback_data=f"theme:{spread_type}:{key}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def webapp_button_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌌 Смотреть анимацию в приложении", web_app=WebAppInfo(url=WEBAPP_URL))],
    ])
