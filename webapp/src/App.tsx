import React, { useEffect, useMemo, useState } from "react";
import MenuScreen from "./components/MenuScreen";
import ThemePicker from "./components/ThemePicker";
import SpreadStage from "./components/SpreadStage";
import HistoryScreen from "./components/HistoryScreen";
import { CardSummary, createReading, fetchCards, getTelegramUserId, ReadingResponse } from "./api";

type Screen = "menu" | "theme" | "reading" | "history" | "paying";

const POSITION_LABELS: Record<string, string[]> = {
  one_card: ["Совет"],
  three_card: ["Прошлое", "Настоящее", "Будущее"],
  celtic_cross: [
    "Текущая ситуация", "Препятствие", "Основа", "Прошлое", "Возможное будущее",
    "Ближайшее будущее", "Вы сами", "Внешнее влияние", "Надежды и страхи", "Итог",
  ],
};

function detectLowPower(): boolean {
  const nav = navigator as any;
  const cores = nav.hardwareConcurrency || 4;
  const mem = nav.deviceMemory || 4;
  const prefersReduced = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  return prefersReduced || cores <= 2 || mem <= 2;
}

export default function App() {
  const [screen, setScreen] = useState<Screen>("menu");
  const [spreadKey, setSpreadKey] = useState<string>("");
  const [cardMap, setCardMap] = useState<Record<string, CardSummary>>({});
  const [reading, setReading] = useState<ReadingResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const lowPower = useMemo(() => detectLowPower(), []);
  const telegramId = useMemo(() => getTelegramUserId() || 0, []);

  useEffect(() => {
    const w = window as any;
    w?.Telegram?.WebApp?.ready?.();
    w?.Telegram?.WebApp?.expand?.();
    fetchCards().then((cards) => {
      const map: Record<string, CardSummary> = {};
      cards.forEach((c) => (map[c.id] = c));
      setCardMap(map);
    });
  }, []);

  async function startInvoiceFlow(theme: string) {
    setScreen("paying");
    try {
      const res = await fetch("/api/payments/celtic_cross_invoice_link", { method: "POST" });
      const { invoice_link } = await res.json();
      const w = window as any;
      // Platform Mini App rule: openInvoice must be called 80ms after the
      // triggering user action, not synchronously.
      setTimeout(() => {
        w?.Telegram?.WebApp?.openInvoice?.(invoice_link, async (status: string) => {
          if (status === "paid") {
            await runReading("celtic_cross", theme);
          } else {
            setScreen("menu");
          }
        });
      }, 80);
    } catch (e) {
      setError(String(e));
      setScreen("menu");
    }
  }

  async function runReading(spread: string, theme: string) {
    setScreen("reading");
    try {
      const r = await createReading({
        telegram_id: telegramId,
        spread_type: spread,
        theme,
        is_yes_no_question: false,
      });
      setReading(r);
    } catch (e) {
      setError(String(e));
    }
  }

  function onSpreadSelect(key: string) {
    setSpreadKey(key);
    if (key === "advice_of_day") {
      runReading("one_card", "general");
      return;
    }
    setScreen("theme");
  }

  function onThemeSelect(theme: string) {
    if (spreadKey === "celtic_cross") {
      startInvoiceFlow(theme);
      return;
    }
    runReading(spreadKey === "advice_of_day" ? "one_card" : spreadKey, theme);
  }

  const effectiveSpread = spreadKey === "advice_of_day" ? "one_card" : spreadKey;

  return (
    <div className={`app-shell ${lowPower ? "low-power" : ""}`}>
      <div className="stardust-bg" />
      {error && <div className="content-layer" style={{ color: "#ff6b6b" }}>{error}</div>}

      {screen === "menu" && (
        <MenuScreen onSelect={onSpreadSelect} onHistory={() => setScreen("history")} />
      )}

      {screen === "theme" && <ThemePicker onSelect={onThemeSelect} />}

      {screen === "paying" && (
        <div className="content-layer">
          <h2>Открываю оплату Telegram Stars...</h2>
        </div>
      )}

      {screen === "reading" && reading && (
        <div className="content-layer">
          <SpreadStage
            cardsDrawn={reading.cards_drawn}
            cardMap={cardMap}
            positionLabels={POSITION_LABELS[reading.spread_type] || []}
            renderedReading={reading.rendered_reading}
            lowPower={lowPower}
          />
          <button className="neon-btn" style={{ marginTop: 20 }} onClick={() => setScreen("menu")}>
            Новый расклад
          </button>
        </div>
      )}

      {screen === "reading" && !reading && (
        <div className="content-layer"><p>Тасую колоду...</p></div>
      )}

      {screen === "history" && (
        <HistoryScreen telegramId={telegramId} onBack={() => setScreen("menu")} />
      )}
    </div>
  );
}
