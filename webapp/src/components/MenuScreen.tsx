import React from "react";

export const SPREADS = [
  { key: "advice_of_day", label: "Совет дня", desc: "1 карта, без темы" },
  { key: "one_card", label: "1 карта", desc: "быстрый совет" },
  { key: "three_card", label: "3 карты", desc: "прошлое · настоящее · будущее" },
  { key: "celtic_cross", label: "Кельтский крест ⭐", desc: "10 карт, премиум-разбор" },
];

interface Props {
  onSelect: (spreadKey: string) => void;
  onHistory: () => void;
}

export default function MenuScreen({ onSelect, onHistory }: Props) {
  return (
    <div className="content-layer">
      <h1>🔮 AI-Таро</h1>
      <p>Оффлайн-расклады на локальной базе значений — без обращений к внешним нейросетям.</p>
      <div className="picker-grid">
        {SPREADS.map((s) => (
          <button key={s.key} className="picker-option" onClick={() => onSelect(s.key)}>
            <strong>{s.label}</strong>
            <div style={{ opacity: 0.7, fontSize: 13 }}>{s.desc}</div>
          </button>
        ))}
      </div>
      <button className="ghost-btn" onClick={onHistory}>📜 История раскладов</button>
    </div>
  );
}
