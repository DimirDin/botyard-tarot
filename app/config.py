import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "tarot")
DB_USER = os.getenv("DB_USER", "tarot")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tarot")
DB_SCHEMA = os.getenv("DB_SCHEMA", "tarot_schema")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://tarot.botyard.site")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "3008"))

CELTIC_CROSS_STARS_PRICE = int(os.getenv("CELTIC_CROSS_STARS_PRICE", "25"))
