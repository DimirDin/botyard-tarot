import React, { useMemo } from "react";

// Zodiac signs, planets and moon phases — widely supported glyphs.
// U+FE0E forces text presentation so they glow like neon instead of
// rendering as colored emoji on iOS/Android.
const GLYPHS = "☽☿♀♂♃♄♈♉♊♋♌♍♎♏♐♑♒♓✶".split("").map((g) => g + "︎");

interface SymbolSpec {
  glyph: string;
  left: number; // vw
  size: number; // px
  duration: number; // s
  delay: number; // s
  drift: number; // px sideways sway
  violet: boolean;
}

function makeSymbols(count: number): SymbolSpec[] {
  return Array.from({ length: count }, (_, i) => ({
    glyph: GLYPHS[Math.floor(Math.random() * GLYPHS.length)],
    left: 4 + (i / count) * 88 + Math.random() * 6,
    size: 16 + Math.random() * 18,
    duration: 18 + Math.random() * 14,
    delay: -Math.random() * 30, // negative: the sky is already "alive" on load
    drift: (Math.random() - 0.5) * 60,
    violet: Math.random() < 0.5,
  }));
}

interface Props {
  lowPower: boolean;
}

export default function MysticBackground({ lowPower }: Props) {
  const symbols = useMemo(() => makeSymbols(9), []);

  return (
    <div className="mystic-bg">
      {/* base gradient + fine stardust (kept from the original design) */}
      <div className="stardust-bg" />
      {!lowPower && (
        <>
          {/* parallax star layers drifting at different speeds */}
          <div className="star-layer star-layer-far" />
          <div className="star-layer star-layer-near" />
          {/* occasional meteors */}
          <span className="meteor meteor-1" />
          <span className="meteor meteor-2" />
          {/* floating esoteric symbols */}
          {symbols.map((s, i) => (
            <span
              key={i}
              className={`float-symbol ${s.violet ? "violet" : "turquoise"}`}
              style={{
                left: `${s.left}vw`,
                fontSize: s.size,
                animationDuration: `${s.duration}s`,
                animationDelay: `${s.delay}s`,
                ["--sway" as string]: `${s.drift}px`,
              }}
            >
              {s.glyph}
            </span>
          ))}
          {/* mystic smoke rising from the bottom */}
          <div className="smoke smoke-1" />
          <div className="smoke smoke-2" />
          <div className="smoke smoke-3" />
        </>
      )}
    </div>
  );
}
