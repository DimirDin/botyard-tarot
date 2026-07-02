import React, { useEffect, useState } from "react";
import type { CardSummary } from "../api";

interface Props {
  card: CardSummary | undefined;
  upright: boolean;
  positionLabel?: string;
  revealDelayMs: number;
  lowPower: boolean;
}

export default function TarotCard({ card, upright, positionLabel, revealDelayMs, lowPower }: Props) {
  const [flying, setFlying] = useState(true);
  const [revealed, setRevealed] = useState(false);
  const [bloom, setBloom] = useState(false);

  useEffect(() => {
    const flyTimer = setTimeout(() => setFlying(false), 50);
    const revealTimer = setTimeout(() => {
      setRevealed(true);
      setBloom(true);
    }, revealDelayMs);
    return () => {
      clearTimeout(flyTimer);
      clearTimeout(revealTimer);
    };
  }, [revealDelayMs]);

  const arcanaClass = card?.arcana === "major" ? "major" : "minor";

  return (
    <div>
      <div className={`tarot-card ${flying ? "flying" : ""} ${revealed ? "revealed" : ""} ${bloom && !lowPower ? "bloom" : ""}`}>
        <div className="tarot-card-inner">
          <div className="tarot-card-face tarot-card-back">✦</div>
          <div className={`tarot-card-face tarot-card-front ${arcanaClass} ${!upright ? "reversed" : ""}`}>
            <div>{card?.name_ru ?? "…"}</div>
          </div>
        </div>
      </div>
      {positionLabel && <div className="position-label">{positionLabel}{!upright ? " · перевёрнута" : ""}</div>}
    </div>
  );
}
