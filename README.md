# taroT (botyard-tarot)

Offline Telegram tarot bot + Mini App. No LLM calls — readings are assembled
from a local structured content database via a deterministic template engine.

See `PROJECT_CONTEXT.md` for full architecture, content coverage status, and
design system details.

## Quick start

```bash
cp .env.example .env
# edit .env: set BOT_TOKEN at minimum
docker compose up -d --build
```

- Mini App / API: http://127.0.0.1:3008
- Bot: starts polling automatically once `BOT_TOKEN` is set

## Verify the engine without Docker

```bash
pip install -r requirements.txt
python3 scripts/verify_engine.py
python3 -m pytest tests/ -q
```

## Regenerate the content database

```bash
python3 scripts/generate_content.py
```
