"use client";

import { useEffect, useRef, useState } from "react";
import { deacc, esc, norm } from "@/lib/text";
import type { Outcome, QIN } from "@/lib/types";

interface Props {
  q: QIN;
  done: boolean;
  onDone: (o: Outcome) => void;
}

const KEYS = ["á", "é", "í", "ó", "ú", "ñ", "¿", "¡"];

export default function WriteQuestion({ q, done, onDone }: Props) {
  const [value, setValue] = useState("");
  const [status, setStatus] = useState<"" | "ok" | "bad">("");
  const ref = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (window.matchMedia("(pointer:fine)").matches) ref.current?.focus({ preventScroll: true });
  }, []);

  const check = () => {
    if (done) return;
    const v = norm(value);
    if (!v) {
      ref.current?.focus();
      return;
    }
    const accepted = q.a.map(norm);
    const ok = accepted.includes(v);
    const almost = !ok && accepted.map(deacc).includes(deacc(v));
    setStatus(ok ? "ok" : "bad");

    let answer: string | undefined;
    if (ok) {
      const others = q.a.filter((a) => norm(a) !== v);
      if (others.length) answer = `Também aceito: ${others.map(esc).join(" · ")}`;
    } else {
      const list = q.a.map((a) => `<b>${esc(a)}</b>`).join(" &nbsp;ou&nbsp; ");
      const pre = almost
        ? `<div class="almost">Quase! A estrutura está certa — confira os <b>acentos</b>.</div>`
        : "";
      answer = `${pre}Resposta${q.a.length > 1 ? "s aceitas" : ""}: ${list}`;
    }
    onDone({ ok, answer });
  };

  const insert = (c: string) => {
    const el = ref.current;
    if (!el || done) return;
    const s = el.selectionStart ?? value.length;
    const e = el.selectionEnd ?? s;
    const next = value.slice(0, s) + c + value.slice(e);
    setValue(next);
    requestAnimationFrame(() => {
      el.focus();
      el.setSelectionRange(s + c.length, s + c.length);
    });
  };

  return (
    <>
      <div className="inrow">
        <input
          ref={ref}
          id={`ans-${q.id}`}
          type="text"
          autoComplete="off"
          autoCapitalize="sentences"
          spellCheck={false}
          placeholder="Escreva a frase completa"
          aria-label="Sua resposta"
          className={status}
          value={value}
          readOnly={done}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              check();
            }
          }}
        />
        <button className="btn primary" onClick={check} disabled={done}>
          Corrigir
        </button>
      </div>
      <div className="keys" style={{ marginTop: 10 }}>
        {KEYS.map((c) => (
          <button key={c} type="button" aria-label={`Inserir ${c}`} onClick={() => insert(c)} disabled={done}>
            {c}
          </button>
        ))}
      </div>
    </>
  );
}
