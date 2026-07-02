import React, { useEffect, useMemo, useState } from "react";
import type { CardSummary } from "../api";

interface DustSpec {
  dx: number;
  dy: number;
  size: number;
  delay: number;
  color: string;
}

function makeDust(count: number, major: boolean): DustSpec[] {
  const violet = "rgba(177, 78, 255, 0.9)";
  const turquoise = "rgba(61, 253, 255, 0.9)";
  return Array.from({ length: count }, (_, i) => {
    const angle = (i / count) * Math.PI * 2 + Math.random() * 0.6;
    const dist = 55 + Math.random() * 45;
    return {
      dx: Math.cos(angle) * dist,
      dy: Math.sin(angle) * dist,
      size: 3 + Math.random() * 3,
      delay: Math.random() * 0.25,
      // major arcana skews violet, minor skews turquoise — matches card glow
      color: Math.random() < (major ? 0.7 : 0.3) ? violet : turquoise,
    };
  });
}

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
  const [imgOk, setImgOk] = useState(true);

  const dust = useMemo(
    () => (lowPower ? [] : makeDust(16, card?.arcana === "major")),
    [lowPower, card?.arcana],
  );

  useEffect(() => {
    const flyTimer = setTimeout(() => setFlying(false), 50);
    const revealTimer = setTimeout(() => setRevealed(true), revealDelayMs);
    return () => {
      clearTimeout(flyTimer);
      clearTimeout(revealTimer);
    };
  }, [revealDelayMs]);

  const arcanaClass = card?.arcana === "major" ? "major" : "minor";

  return (
    <div>
      <div className={`tarot-card ${flying ? "flying" : ""} ${revealed ? "revealed" : ""}`}>
        {revealed &&
          dust.map((p, i) => (
            <span
              key={i}
              className="dust-particle"
              style={{
                width: p.size,
                height: p.size,
                background: p.color,
                boxShadow: `0 0 6px ${p.color}`,
                animationDelay: `${p.delay}s`,
                ["--dx" as string]: `${p.dx}px`,
                ["--dy" as string]: `${p.dy}px`,
              }}
            />
          ))}
        <div className="tarot-card-inner">
          <div className="tarot-card-face tarot-card-back">✦</div>
          <div className={`tarot-card-face tarot-card-front ${arcanaClass} ${!upright ? "reversed" : ""} ${imgOk && card ? "has-image" : ""}`}>
            {imgOk && card ? (
              <>
                <img
                  className="tarot-card-art"
                  src={`/cards/${card.id}.webp`}
                  alt={card.name_ru}
                  draggable={false}
                  onError={() => setImgOk(false)}
                />
                <div className="tarot-card-caption">{card.name_ru}</div>
              </>
            ) : (
              <div>{card?.name_ru ?? "…"}</div>
            )}
          </div>
        </div>
      </div>
      {positionLabel && <div className="position-label">{positionLabel}{!upright ? " · перевёрнута" : ""}</div>}
    </div>
  );
}
