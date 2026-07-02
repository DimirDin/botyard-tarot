import React from "react";

export default function DeckShuffle({ shuffling }: { shuffling: boolean }) {
  return (
    <div className={`deck-stage ${shuffling ? "deck-shuffling" : ""}`}>
      {[0, 1, 2, 3, 4].map((i) => (
        <div key={i} className="deck-card-back" style={{ zIndex: 5 - i, marginLeft: i === 0 ? 0 : -70 }} />
      ))}
    </div>
  );
}
