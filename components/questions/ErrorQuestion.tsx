"use client";

import { useState } from "react";
import { esc } from "@/lib/text";
import type { Outcome, QERR } from "@/lib/types";

interface Props {
  q: QERR;
  done: boolean;
  onDone: (o: Outcome) => void;
}

export default function ErrorQuestion({ q, done, onDone }: Props) {
  const [picked, setPicked] = useState<number | null>(null);

  const answer = (i: number) => {
    if (done) return;
    setPicked(i);
    const ok = (i === -1 && q.a.length === 0) || q.a.includes(i);
    const text = q.a.length ? `Correção: <b>${esc(q.fix)}</b>` : ok ? undefined : "A frase estava correta.";
    onDone({ ok, answer: text });
  };

  return (
    <>
      <div className="tokens">
        {q.w.map((w, i) => {
          let cls = "tok";
          if (done && q.a.includes(i)) cls += " bad";
          else if (done && picked === i) cls += " pick";
          return (
            <button key={i} className={cls} disabled={done} onClick={() => answer(i)}>
              {w}
            </button>
          );
        })}
      </div>
      <div style={{ marginTop: 12 }}>
        <button className={`btn${done && picked === -1 && q.a.length ? " pick" : ""}`} disabled={done} onClick={() => answer(-1)}>
          Não há erro
        </button>
      </div>
    </>
  );
}
