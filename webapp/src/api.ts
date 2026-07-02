export interface CardSummary {
  id: string;
  name_ru: string;
  name_en: string;
  arcana: "major" | "minor";
  suit: string | null;
  image_ref: string;
}

export interface DrawnCardEntry {
  card_id: string;
  upright: boolean;
  position: number;
}

export interface ReadingResponse {
  id: number;
  spread_type: string;
  theme: string | null;
  question: string | null;
  cards_drawn: DrawnCardEntry[];
  rendered_reading: string;
  created_at: string;
}

const BASE = ""; // same-origin: FastAPI serves both API and static bundle

export async function fetchCards(): Promise<CardSummary[]> {
  const res = await fetch(`${BASE}/api/cards`);
  if (!res.ok) throw new Error("Failed to load cards");
  return res.json();
}

export async function createReading(params: {
  telegram_id: number;
  spread_type: string;
  theme: string;
  question?: string;
  is_yes_no_question?: boolean;
}): Promise<ReadingResponse> {
  const res = await fetch(`${BASE}/api/readings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error("Failed to create reading");
  return res.json();
}

export async function fetchHistory(telegramId: number): Promise<ReadingResponse[]> {
  const res = await fetch(`${BASE}/api/readings/${telegramId}`);
  if (!res.ok) throw new Error("Failed to load history");
  return res.json();
}

export function getTelegramUserId(): number {
  const w = window as any;
  const tgId = w?.Telegram?.WebApp?.initDataUnsafe?.user?.id;
  return tgId ?? 0;
}
