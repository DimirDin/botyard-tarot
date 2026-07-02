import React, { useEffect, useState } from "react";
import { fetchHistory, ReadingResponse } from "../api";

export default function HistoryScreen({ telegramId, onBack }: { telegramId: number; onBack: () => void }) {
  const [items, setItems] = useState<ReadingResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory(telegramId)
      .then(setItems)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [telegramId]);

  return (
    <div className="content-layer">
      <h2>📜 История раскладов</h2>
      {loading && <p>Загрузка...</p>}
      {error && <p>Ошибка: {error}</p>}
      {!loading && items.length === 0 && <p>Раскладов пока нет.</p>}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((r) => (
          <div key={r.id} className="reading-block" style={{ animation: "none", opacity: 1, transform: "none" }}>
            <div style={{ fontSize: 12, opacity: 0.6 }}>
              {new Date(r.created_at).toLocaleString("ru-RU")} · {r.spread_type} · {r.theme ?? "—"}
            </div>
            <div style={{ marginTop: 6, whiteSpace: "pre-wrap" }}>{r.rendered_reading.slice(0, 240)}...</div>
          </div>
        ))}
      </div>
      <button className="ghost-btn" onClick={onBack}>← Назад</button>
    </div>
  );
}
