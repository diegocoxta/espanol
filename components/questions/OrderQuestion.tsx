"use client";

import { useEffect, useMemo, useState } from "react";
import { capFirst, esc, norm, seeded, shuffle } from "@/lib/text";
import type { Outcome, QORD } from "@/lib/types";

interface Props {
  q: QORD;
  done: boolean;
  onDone: (o: Outcome) => void;
}

export default function OrderQuestion({ q, done, onDone }: Props) {
  // embaralhamento estável por questão (mesma ordem a cada visita)
  const initial = useMemo(() => {
    let order = shuffle(q.w.map((_, i) => i), seeded(q.id));
    if (order.length > 1 && order.every((v, i) => v === i)) order = order.reverse();
    return order;
  }, [q]);

  const [placed, setPlaced] = useState<number[]>([]);
  const [status, setStatus] = useState<"" | "ok" | "bad">("");
  const bank = initial.filter((i) => !placed.includes(i));
  const complete = bank.length === 0;

  const toggle = (i: number) => {
    if (done) return;
    setPlaced((p) => (p.includes(i) ? p.filter((x) => x !== i) : [...p, i]));
  };

  const check = () => {
    if (done || !complete) return;
    const ok = q.a.includes(norm(placed.map((i) => q.w[i]).join(" ")));
    setStatus(ok ? "ok" : "bad");
    const show = q.a.map((a) => `<b>${esc(capFirst(a))}.</b>`).join(" &nbsp;ou&nbsp; ");
    onDone({ ok, answer: ok ? undefined : `Ordem correta: ${show}` });
  };

  // Enter corrige quando todas as palavras estão colocadas
  useEffect(() => {
    if (done) return;
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement).tagName;
      if (e.key === "Enter" && complete && tag !== "BUTTON" && tag !== "INPUT") {
        e.preventDefault();
        check();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  });

  return (
    <>
      <div className={`ordline ${status}`}>
        {placed.length === 0 && <span className="ordhint">Toque nas palavras abaixo na ordem certa</span>}
        {placed.map((i) => (
          <button key={i} className="w placed" disabled={done} onClick={() => toggle(i)}>
            {q.w[i]}
          </button>
        ))}
      </div>
      <div className="bank" style={{ marginTop: 10 }}>
        {bank.map((i) => (
          <button key={i} className="w" disabled={done} onClick={() => toggle(i)}>
            {q.w[i]}
          </button>
        ))}
      </div>
      <div style={{ display: "flex", gap: 8, marginTop: 12, flexWrap: "wrap" }}>
        <button className="btn primary" onClick={check} disabled={done || !complete}>
          Corrigir
        </button>
        <button className="btn" onClick={() => setPlaced([])} disabled={done || placed.length === 0}>
          Limpar
        </button>
      </div>
    </>
  );
}
