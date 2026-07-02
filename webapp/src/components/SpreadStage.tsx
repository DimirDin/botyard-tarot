import React, { useEffect, useMemo, useState } from "react";
import type { CardSummary, DrawnCardEntry } from "../api";
import DeckShuffle from "./DeckShuffle";
import TarotCard from "./TarotCard";

interface Props {
  cardsDrawn: DrawnCardEntry[];
  cardMap: Record<string, CardSummary>;
  positionLabels: string[];
  renderedReading: string;
  lowPower: boolean;
}

const STAGGER_MS = 140;
const SHUFFLE_MS = 1200;

export default function SpreadStage({ cardsDrawn, cardMap, positionLabels, renderedReading, lowPower }: Props) {
  const [shuffling, setShuffling] = useState(true);
  const [showCards, setShowCards] = useState(false);
  const [visibleTextCount, setVisibleTextCount] = useState(0);

  const readingBlocks = useMemo(
    () => renderedReading.split(/\n\n---\n\n/).map((b) => b.trim()),
    [renderedReading]
  );

  useEffect(() => {
    const t = setTimeout(() => {
      setShuffling(false);
      setShowCards(true);
    }, lowPower ? 300 : SHUFFLE_MS);
    return () => clearTimeout(t);
  }, [lowPower]);

  useEffect(() => {
    if (!showCards) return;
    const n = cardsDrawn.length;
    const timers: ReturnType<typeof setTimeout>[] = [];
    for (let i = 0; i < n; i++) {
      const delay = i * (lowPower ? 60 : STAGGER_MS) + 700;
      timers.push(setTimeout(() => setVisibleTextCount((c) => Math.max(c, i + 1)), delay));
    }
    return () => timers.forEach(clearTimeout);
  }, [showCards, cardsDrawn.length, lowPower]);

  return (
    <div>
      {shuffling && <DeckShuffle shuffling={shuffling} />}

      {showCards && (
        <div className="spread-row">
          {cardsDrawn.map((dc, i) => (
            <TarotCard
              key={`${dc.card_id}-${i}`}
              card={cardMap[dc.card_id]}
              upright={dc.upright}
              positionLabel={positionLabels[i]}
              revealDelayMs={i * (lowPower ? 60 : STAGGER_MS) + 300}
              lowPower={lowPower}
            />
          ))}
        </div>
      )}

      <div style={{ marginTop: 20, display: "flex", flexDirection: "column", gap: 12 }}>
        {readingBlocks.slice(0, visibleTextCount).map((block, i) => (
          <div key={i} className="reading-block" style={{ animationDelay: `${i * 80}ms` }}>
            {renderInline(block)}
          </div>
        ))}
      </div>
    </div>
  );
}

function renderInline(text: string) {
  // Minimal markdown-ish rendering: **bold** headers and "Совет:" line highlight
  const lines = text.split("\n");
  return lines.map((line, idx) => {
    const isHeader = line.startsWith("**") && line.endsWith("**");
    const isAdvice = line.startsWith("Совет:");
    if (isHeader) {
      return <h3 key={idx}>{line.replace(/\*\*/g, "")}</h3>;
    }
    if (isAdvice) {
      return <p key={idx} className="advice-line">{line}</p>;
    }
    return <p key={idx}>{line}</p>;
  });
}
