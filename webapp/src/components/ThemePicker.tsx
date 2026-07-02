import React from "react";

const THEMES = [
  { key: "general", label: "Общий вопрос" },
  { key: "love", label: "Любовь и отношения" },
  { key: "career", label: "Карьера и работа" },
  { key: "finance", label: "Финансы" },
  { key: "health", label: "Здоровье" },
  { key: "spirit", label: "Духовность" },
];

export default function ThemePicker({ onSelect }: { onSelect: (theme: string) => void }) {
  return (
    <div className="content-layer">
      <h2>На какую тему расклад?</h2>
      <div className="picker-grid">
        {THEMES.map((t) => (
          <button key={t.key} className="picker-option" onClick={() => onSelect(t.key)}>
            {t.label}
          </button>
        ))}
      </div>
    </div>
  );
}
