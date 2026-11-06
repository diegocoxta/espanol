"use client";

import { useEffect, useState } from "react";
import type { Outcome, QMC } from "@/lib/types";

interface Props {
  q: QMC;
  done: boolean;
  onDone: (o: Outcome, blank?: string) => void;
}

export default function ChoiceQuestion({ q, done, onDone }: Props) {
  const [picked, setPicked] = useState<number | null>(null);
  const long = q.o.some((o) => o.length > 28);

  const choose = (i: number) => {
    if (done) return;
    setPicked(i);
    const ok = i === q.a;
    const right = q.o[q.a];
    onDone({ ok, answer: ok ? undefined : `Resposta: <b>${right}</b>` }, right.startsWith("—") ? "∅" : right);
  };

  // teclas 1–9 escolhem a opção
  useEffect(() => {
    if (done) return;
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") return;
      if (/^[1-9]$/.test(e.key)) {
        const i = Number(e.key) - 1;
        if (i < q.o.length) {
          e.preventDefault();
          choose(i);
        }
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  });

  return (
    <div className={`opts${long ? " long" : ""}`}>
      {q.o.map((o, i) => {
        let cls = "opt";
        if (done) cls += i === q.a ? " ok" : i === picked ? " bad" : " dim";
        return (
          <button key={i} className={cls} disabled={done} onClick={() => choose(i)}>
            <span className="k">{i + 1}</span>
            <span dangerouslySetInnerHTML={{ __html: o }} />
          </button>
        );
      })}
    </div>
  );
}
