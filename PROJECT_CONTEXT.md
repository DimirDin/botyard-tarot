# botyard-tarot — AI-Таро (offline tarot bot + Mini App)

Context doc for future sessions on this platform. Mirrors the format used by
sibling bots (botyard-*). Read this before touching the repo.

## Product concept — read this first

This is explicitly **NOT** an LLM-generated tarot bot. There is **zero
external network calls for content generation**. All personalization comes
from a rich, hand-authored, versioned local content database combined with a
deterministic Python template engine (`app/engine/template_engine.py`).
Selling point: instant, works offline, zero API cost, zero latency, and the
same input always produces the same output (verified — see below).

### How a reading is assembled (no AI, just data + templates)

For each drawn card, the engine composes one coherent paragraph in this order:
1. **Base meaning** — `content/cards/<id>.json` → `meanings.<theme>.<upright|reversed>`.
2. **Positional nuance** — `content/position_nuance.json` → text keyed by
   spread type + position index, spliced in as a natural second paragraph.
3. **Combination note** — `content/combinations.json`, if the pair of drawn
   cards has an entry (lookup key: sorted `id_a|id_b`, see
   `content_loader.combination_key`).
4. **Advice line** — `meanings` sibling field `advice.<orientation>`,
   always the last paragraph, prefixed `Совет:`.

Paragraphs are joined with blank lines so it reads as one flowing text, not
four disconnected chunks. See `app/engine/template_engine.py:assemble_card_reading`.

### Spreads

| spread_type    | cards | notes                                                             |
|----------------|-------|--------------------------------------------------------------------|
| `one_card`     | 1     | quick advice; if question is yes/no, also shows `yes_no` field    |
| `three_card`   | 3     | past / present / future                                           |
| `celtic_cross` | 10    | full 10-position reading; **premium**, gated by Telegram Stars    |
| advice of day  | 1     | uses `one_card` spread + `general` theme, no question needed      |

Position semantics live in `content/position_nuance.json` (`three_card`,
`celtic_cross` keys). Deck mechanics (`app/engine/deck.py`): 78 cards, no
repeats per spread, each card independently upright/reversed (~50/50).

### Themes

`general | love | career | finance | health | spirit` — user must pick one
for every spread except "advice of the day" (which always uses `general`).

## Content database — honest coverage status

Source of truth: `scripts/generate_content.py` (regenerate with
`python3 scripts/generate_content.py`, writes `content/cards/*.json`).

- **Wave 1 — COMPLETE for all 78 cards**: `general`, `love`, `career`. Each
  card has hand-authored `essence_up` / `essence_rev` symbolism (see the
  `MAJOR` / `RANKS` tables in the generator) composed through theme-specific
  sentence templates so the three themes read distinctly for the same card,
  not just with the theme name swapped in.
- **Wave 2 — COMPLETE for all 78 cards**: `finance`, `health`, `spirit` are
  generated for every card via the same essence-driven theme templates used
  for love/career (see `finance_text` / `health_text` / `spirit_text` in
  `scripts/generate_content.py`), so they read distinctly per theme while
  staying consistent with each card's core symbolism. No `TODO` stubs remain.
- `yes_no` and `advice` are fully generated for all 78 cards × both
  orientations (156 advice lines, 156 yes/no values), plus a small hand-tuned
  override table for the most narratively-strong majors (Tower, Devil, Moon,
  Sun, Star, World, Death, Hanged Man → non-default yes/no answers).
- `content/position_nuance.json` — complete: 3 entries for `three_card`, 10
  for `celtic_cross`, standard Celtic Cross position semantics (situation,
  obstacle, foundation, past, possible future, near future, self, external
  influence, hopes/fears, outcome).
- `content/combinations.json` — starter library of ~28 hand-written card-pair
  notes for the most evocative/frequent pairs (Tower+Death, Lovers+Devil,
  Star+Sun, etc). Schema documented in the file's own `_schema` key; add more
  pairs any time with zero code changes — the engine looks up
  `sorted([id_a, id_b])` joined by `|`.

**To finish wave 2**: extend `WAVE2_CARDS` in `scripts/generate_content.py`
(or better, replace the templated `finance_text`/`health_text`/`spirit_text`
functions with real per-card hand-authored prose the same way `essence_up`/
`essence_rev` were authored), then rerun the generator.

## Content storage decision

Static card content (`content/*.json`) is **read directly from versioned
JSON at runtime**, not loaded into Postgres. Reasoning: it never needs
relational queries, it's naturally versioned alongside the code that
interprets it, and it keeps deploys simple (no seed-migration step to keep in
sync with content edits). Only `users` and `readings` live in Postgres.
`Reading.rendered_reading` is a **snapshot** of the assembled text at the
time of the reading — if content is edited/expanded later, old history
entries do NOT retroactively change (`app/engine/reading_service.py`).

## Schema (`tarot_schema`, Postgres, Alembic-managed)

```sql
tarot_schema.users     (telegram_id PK, is_premium, created_at)
tarot_schema.readings  (id PK, user_id FK -> users, question, theme, spread_type,
                         cards_drawn JSONB, rendered_reading TEXT, created_at)
```

Migrations: `migrations/versions/0001_initial.py` (creates schema + both
tables). Run with `alembic upgrade head` (done automatically by the
`migrate` one-shot service in `docker-compose.yml`).

## Code layout

```
app/
  config.py              env-driven settings
  engine/
    content_loader.py    loads content/*.json (cached)
    deck.py              random draw, no repeats, upright/reversed
    template_engine.py   deterministic assembly (no randomness in here)
    reading_service.py   shared create/list-reading logic (bot + API both use this)
  db/
    models.py            SQLAlchemy models (User, Reading)
    session.py           async engine/session
  bot/
    main.py               aiogram 3 polling entrypoint
    keyboards.py           inline keyboards (spread/theme menus, Mini App button)
    handlers/
      start.py             /start, advice-of-day, spread selection
      reading.py            theme selection -> reading, Stars invoice + payment handlers
      history.py            /history command + callback
  payments/
    stars.py               Telegram Stars (XTR) invoice helper
  api/
    main.py                 FastAPI app; also serves webapp/dist as static files
    routers/
      readings.py           POST /api/readings, GET /api/readings/{telegram_id}
      cards.py               GET /api/cards, GET /api/cards/{id}
      payments.py            POST /api/payments/celtic_cross_invoice_link
content/
  cards/*.json             78 card content files + _index.json
  position_nuance.json
  combinations.json
migrations/                Alembic env + versions
scripts/
  generate_content.py      content DB generator/source-of-truth
  verify_engine.py         determinism + no-crash verification across all 78 cards
tests/test_engine.py        pytest version of the same checks
webapp/                    React 18 + Vite Mini App ("Неоновый мистицизм" design)
```

## Design system — "Неоновый мистицизм" (locked, do not deviate)

- Background `#0F0A1A`, primary neon `#B14EFF` (violet), secondary neon
  `#3DFDFF` (turquoise), text `#EAE6F5`.
- Headings: Space Grotesk. Body: Inter.
- Card glow: violet box-shadow for major arcana, turquoise for minor arcana
  (`webapp/src/styles/global.css` `.tarot-card-front.major/.minor`).
- Animation flow implemented in `webapp/src/components/`:
  `DeckShuffle` (fan motion), `TarotCard` (3D flip + bloom flash),
  `SpreadStage` (orchestrates shuffle → fly-to-position → staggered
  120–150ms reveal → reading text fade/slide-up per card).
  Stardust/parallax background: `.stardust-bg` in `global.css`.
- **`prefers-reduced-motion` and a `.low-power` class both degrade the same
  way**: animations are disabled/shortened, kept purely functional. Low-power
  detection is heuristic (`navigator.hardwareConcurrency`/`deviceMemory`) in
  `App.tsx:detectLowPower`.
- Constraint respected: no `display:contents` combined with CSS animation
  anywhere in this codebase.

## Monetization

Free forever: 1-card, 3-card, advice-of-day. **Premium**: Celtic Cross,
paid via **Telegram Stars only** (currency `XTR`, no other provider).
Two payment entry points, both funneling into the same
`create_invoice_link`/`send_invoice` payload (`celtic_cross_unlock`):
- Bot: `app/bot/handlers/reading.py` calls `send_celtic_cross_invoice`
  directly, handles `pre_checkout_query` + `successful_payment`.
- Mini App: `POST /api/payments/celtic_cross_invoice_link` returns an invoice
  link; `App.tsx:startInvoiceFlow` calls `tg.WebApp.openInvoice(link)` inside
  a `setTimeout(..., 80)` — **the 80ms delay after the triggering tap is a
  hard platform rule**, do not call `openInvoice` synchronously.

## Running locally

```bash
cp .env.example .env   # fill in BOT_TOKEN at minimum
docker compose up -d --build
# webapp on http://127.0.0.1:3008 (Caddy elsewhere maps tarot.botyard.site -> this port)
# bot starts polling automatically
```

Without Docker, for engine-only iteration:
```bash
python3 scripts/verify_engine.py     # sanity across all 78 cards, all themes, all spreads
python3 -m pytest tests/ -q
```

## Deploy

Self-hosted runner + rsync, same pattern as sibling bots — see
`.github/workflows/deploy.yml`. Triggered on push to `main`. This session did
**not** push to the remote; commits are local only, push manually when ready.

## Known simplifications / TODOs for a future session

- Mini App does not yet validate Telegram `initData` HMAC signature server-side
  before creating a reading — `telegram_id` is currently trusted as sent by
  the client. Fine for MVP behind Telegram's own WebView, but should be
  hardened before wider exposure.
- No image assets — `image_ref` is a placeholder slug string only
  (`cards/<id>.png`), Mini App renders text-only card fronts.
- History UI in the Mini App is a simple list (truncated text); no per-card
  breakdown replay for old readings, "good enough" per the spec.
