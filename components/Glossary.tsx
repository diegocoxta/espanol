"use client";

import { useMemo, useState } from "react";
import type { GlossEntry } from "@/lib/modules";
import type { Question, Results } from "@/lib/types";
import { deacc } from "@/lib/text";

interface Props {
  title: string;
  entries: GlossEntry[];
  active: string | null;
  results: Results;
  questions: Question[];
  onPractice: (id: string) => void;
}

const key = (s: string) => deacc(s.toLowerCase());

export default function Glossary({ title, entries, active, results, questions, onPractice }: Props) {
  const [q, setQ] = useState("");

  // quantas questões de cada item já foram feitas
  const done = useMemo(() => {
    const d: Record<string, number> = {};
    for (const qq of questions) {
      if (results[qq.id] === undefined || !qq.v) continue;
      for (const v of qq.v) d[v] = (d[v] || 0) + 1;
    }
    return d;
  }, [questions, results]);

  const groups = useMemo(() => {
    const k = key(q.trim());
    const filtered = k
      ? entries.filter((e) => key(`${e.v} ${e.pt} ${e.ex} ${e.base}`).includes(k))
      : entries;
    const map = new Map<string, GlossEntry[]>();
    for (const e of filtered) {
      if (!map.has(e.cat)) map.set(e.cat, []);
      map.get(e.cat)!.push(e);
    }
    return [...map.entries()];
  }, [entries, q]);

  const minN = Math.min(...entries.map((e) => e.n));
  const shown = groups.reduce((a, [, l]) => a + l.length, 0);

  return (
    <details className="sheet gloss">
      <summary>
        {title} <span className="gcount">{entries.length} itens</span>
      </summary>
      <div className="glossbody">
        <p className="gintro">
          Todos os itens do material têm questões próprias (no mínimo {minN}). Toque em <b>Praticar</b> para estudar só
          aquele verbo ou uso, em todos os níveis.
        </p>
        <input
          id="gloss-search"
          type="search"
          className="gsearch"
          placeholder="Buscar verbo, sentido ou exemplo"
          aria-label="Buscar no glossário"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        {resultLine(shown, q)}
        {groups.map(([cat, list]) => (
          <section key={cat} className="gsec">
            <h3>
              {cat} <span>{list.length}</span>
            </h3>
            <ul className="glist">
              {list.map((e) => (
                <li key={e.id} className={active === e.id ? "on" : ""}>
                  <div className="gmain">
                    <div className="gv">
                      <b className="es">{e.v}</b>
                      <span className="gpt">{e.pt}</span>
                      {e.note && <span className="gnote">{e.note}</span>}
                    </div>
                    <div className="gex es">{e.ex}</div>
                    {e.base && (
                      <div className="gbase">
                        sem pronome: <span className="es">{e.base}</span> = {e.base_pt}
                      </div>
                    )}
                  </div>
                  <button className="gbtn" onClick={() => onPractice(e.id)} aria-label={`Praticar ${e.v}`}>
                    Praticar
                    <span>
                      {done[e.id] ?? 0}/{e.n}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </details>
  );
}

function resultLine(shown: number, q: string) {
  if (!q.trim()) return null;
  return <p className="gintro">{shown ? `${shown} resultado${shown > 1 ? "s" : ""}` : "Nada encontrado."}</p>;
}
