"use client";

import type { Question, Results } from "@/lib/types";

interface Props {
  list: Question[];
  results: Results;
  current: number;
  onJump: (i: number) => void;
}

export default function QuestionMap({ list, results, current, onJump }: Props) {
  const ok = list.filter((q) => results[q.id] === 1).length;
  const bad = list.filter((q) => results[q.id] === 0).length;

  return (
    <details className="map">
      <summary>
        Mapa das questões{" "}
        <span>
          {list.length} nesta seleção · {ok} certas · {bad} erradas
        </span>
      </summary>
      <div className="legend">
        <span><i className="sw ok" />acertou</span>
        <span><i className="sw bad" />errou</span>
        <span><i className="sw none" />não feita</span>
      </div>
      <div className="dots">
        {list.map((q, i) => {
          const r = results[q.id];
          const cls = `dot${r === 1 ? " ok" : r === 0 ? " bad" : ""}${i === current ? " cur" : ""}`;
          const label = `Questão ${i + 1} (#${q.id}) · ${q.k}`;
          return <button key={q.id} className={cls} title={label} aria-label={label} onClick={() => onJump(i)} />;
        })}
      </div>
    </details>
  );
}
