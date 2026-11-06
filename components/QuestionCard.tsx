"use client";

import { useEffect, useRef, useState } from "react";
import { sentenceHTML } from "@/lib/text";
import type { Outcome, Question } from "@/lib/types";
import ChoiceQuestion from "./questions/ChoiceQuestion";
import WriteQuestion from "./questions/WriteQuestion";
import ErrorQuestion from "./questions/ErrorQuestion";
import OrderQuestion from "./questions/OrderQuestion";

interface Props {
  q: Question;
  levelName: string;
  index: number;
  total: number;
  previous: 0 | 1 | undefined;
  onResult: (ok: boolean) => void;
  onPrev: () => void;
  onNext: () => void;
}

export default function QuestionCard({ q, levelName, index, total, previous, onResult, onPrev, onNext }: Props) {
  const [outcome, setOutcome] = useState<Outcome | null>(null);
  const [fill, setFill] = useState<{ text: string; ok: boolean } | undefined>();
  const nextRef = useRef<HTMLButtonElement>(null);
  const done = outcome !== null;

  const finish = (o: Outcome, blank?: string) => {
    if (done) return;
    setOutcome(o);
    if (blank !== undefined) setFill({ text: blank, ok: o.ok });
    onResult(o.ok);
  };

  useEffect(() => {
    if (done) nextRef.current?.focus({ preventScroll: true });
  }, [done]);

  const status = previous === 1 ? "✓ acertou antes · " : previous === 0 ? "✗ errou antes · " : "";

  return (
    <>
      <div className="meta">
        <span style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          <span className="chip lv">
            Nível {q.lv} · {levelName}
          </span>
          <span className="chip">{q.k}</span>
        </span>
        <span className="prev">
          {status}
          {index + 1} de {total}
        </span>
      </div>

      <p className="prompt" dangerouslySetInnerHTML={{ __html: q.q }} />
      {q.s && <p className="sentence" dangerouslySetInnerHTML={{ __html: sentenceHTML(q.s, fill) }} />}

      <div>
        {q.t === "mc" && <ChoiceQuestion q={q} done={done} onDone={finish} />}
        {q.t === "in" && <WriteQuestion q={q} done={done} onDone={finish} />}
        {q.t === "err" && <ErrorQuestion q={q} done={done} onDone={finish} />}
        {q.t === "ord" && <OrderQuestion q={q} done={done} onDone={finish} />}
      </div>

      {outcome && (
        <div className={`fb ${outcome.ok ? "ok" : "bad"}`}>
          <div className="h">{outcome.ok ? "Correto!" : "Não foi dessa vez."}</div>
          {outcome.answer && <div className="ans" dangerouslySetInnerHTML={{ __html: outcome.answer }} />}
          <p dangerouslySetInnerHTML={{ __html: q.x }} />
        </div>
      )}

      <div className="nav">
        <div className="grp">
          <button className="btn" onClick={onPrev} disabled={index === 0}>
            ← Anterior
          </button>
          <button
            ref={nextRef}
            className={`btn${done ? " primary" : ""}`}
            onClick={onNext}
            disabled={index === total - 1}
          >
            Próxima →
          </button>
        </div>
        <span className="hint">#{q.id}</span>
      </div>
    </>
  );
}
