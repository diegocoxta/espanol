"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { MODES, TYPES_ORDER } from "@/lib/levels";
import { shuffle } from "@/lib/text";
import { useProgress } from "@/lib/useProgress";
import type { ModuleDef } from "@/lib/modules";
import type { Mode, Question, Store } from "@/lib/types";
import QuestionCard from "./QuestionCard";
import QuestionMap from "./QuestionMap";
import ResetButton from "./ResetButton";
import Glossary from "./Glossary";

const posKey = (s: Pick<Store, "lv" | "type" | "verb">) => `${s.lv}|${s.type}|${s.verb ?? ""}`;
const inLevel = (q: Question, lv: number) => lv === 0 || q.lv === lv;

function buildList(all: Question[], s: Store): Question[] {
  let L = s.verb
    ? all.filter((q) => q.v?.includes(s.verb!) && (s.type === "all" || q.k === s.type))
    : all.filter((q) => inLevel(q, s.lv) && (s.type === "all" || q.k === s.type));
  if (s.mode === "wrong") L = L.filter((q) => s.r[q.id] === 0);
  if (s.mode === "new") L = L.filter((q) => s.r[q.id] === undefined);
  if (s.mode === "rand") L = shuffle(L);
  return L;
}

export default function StudyApp({ mod, nav }: { mod: ModuleDef; nav?: React.ReactNode }) {
  const QUESTIONS = mod.questions;
  const { store, update, ready, resetProgress } = useProgress(mod.storageKey);
  const [list, setList] = useState<Question[]>([]);
  const [idx, setIdx] = useState(0);
  const [resetTick, setResetTick] = useState(0);
  const answeredRef = useRef(false);
  const cardRef = useRef<HTMLElement>(null);

  // Monta a lista só quando muda nível / tipo / modo / verbo (não a cada resposta),
  // para que "Revisar erros" e "Não feitas" não encolham no meio do estudo.
  useEffect(() => {
    if (!ready) return;
    const L = buildList(QUESTIONS, store);
    setList(L);
    let i = 0;
    const saved = store.pos[posKey(store)];
    if (store.mode === "seq" && saved) {
      const j = L.findIndex((q) => q.id === saved);
      if (j >= 0) i = j;
    }
    setIdx(i);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, store.lv, store.type, store.mode, store.verb, resetTick, QUESTIONS]);

  const current = list[Math.min(idx, list.length - 1)];

  useEffect(() => {
    if (!current) return;
    answeredRef.current = false;
    update((s) => ({ ...s, pos: { ...s.pos, [posKey(s)]: current.id } }));
  }, [current, update]);

  const go = useCallback(
    (d: number) => {
      setIdx((i) => {
        const n = i + d;
        return n < 0 || n >= list.length ? i : n;
      });
      cardRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    },
    [list.length],
  );

  const record = useCallback(
    (q: Question, ok: boolean) => {
      answeredRef.current = true;
      update((s) => ({ ...s, r: { ...s.r, [q.id]: ok ? 1 : 0 } }));
    },
    [update],
  );

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement;
      const tag = el.tagName;
      if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA" || e.defaultPrevented) return;
      if (e.key === "Enter" && answeredRef.current && tag !== "BUTTON") {
        e.preventDefault();
        go(1);
      } else if (e.key === "ArrowRight" && !el.closest("nav")) go(1);
      else if (e.key === "ArrowLeft" && !el.closest("nav")) go(-1);
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [go]);

  const setLevel = (lv: number) =>
    update((s) => {
      const hasType = s.type === "all" || QUESTIONS.some((q) => inLevel(q, lv) && q.k === s.type);
      return { ...s, lv, verb: null, type: hasType ? s.type : "all" };
    });
  const setMode = (mode: Mode) => update((s) => ({ ...s, mode }));
  const setType = (type: string) => update((s) => ({ ...s, type }));
  const practiceVerb = (id: string) => {
    update((s) => ({ ...s, verb: id, type: "all" }));
    setTimeout(() => cardRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 30);
  };

  const answeredIds = Object.keys(store.r);
  const okCount = answeredIds.filter((k) => store.r[k] === 1).length;
  const levelStats = useMemo(
    () =>
      mod.levels.map((L) => {
        const qs = QUESTIONS.filter((q) => inLevel(q, L.n));
        return { ...L, total: qs.length, done: qs.filter((q) => store.r[q.id] !== undefined).length };
      }),
    [store.r, QUESTIONS, mod.levels],
  );
  const pool = useMemo(
    () => (store.verb ? QUESTIONS.filter((q) => q.v?.includes(store.verb!)) : QUESTIONS.filter((q) => inLevel(q, store.lv))),
    [QUESTIONS, store.lv, store.verb],
  );
  const typeCounts = useMemo(() => {
    const c: Record<string, number> = {};
    pool.forEach((q) => (c[q.k] = (c[q.k] || 0) + 1));
    return c;
  }, [pool]);
  const types = [...TYPES_ORDER.filter((t) => typeCounts[t]), ...Object.keys(typeCounts).filter((t) => !TYPES_ORDER.includes(t))];
  const lvInfo = mod.levels[store.lv] ?? mod.levels[0];
  const verbEntry = store.verb ? mod.glossary?.find((g) => g.id === store.verb) : undefined;

  let emptyMsg = "Nenhuma questão nesta seleção.";
  if (store.mode === "wrong") emptyMsg = "Nenhum erro para revisar nesta seleção. Bom sinal!";
  if (store.mode === "new") emptyMsg = "Você já fez todas as questões desta seleção.";

  return (
    <div className="wrap">
      {nav}
      <header className="top">
        <div>
          <div className="eyebrow">{mod.eyebrow}</div>
          <h1>
            {mod.titleA} <span className="ob">{mod.titleMark}</span>
          </h1>
          <p className="sub">
            {mod.intro}: {QUESTIONS.length.toLocaleString("pt-BR")} exercícios em seis níveis, com correção na hora e
            explicação de cada resposta.
          </p>
        </div>
        <div className="gstats" aria-live="polite">
          <div className="gstat">
            <b>{ready ? answeredIds.length : "—"}</b>
            <span>feitas</span>
          </div>
          <div className="gstat">
            <b>{ready && answeredIds.length ? Math.round((100 * okCount) / answeredIds.length) + "%" : "—"}</b>
            <span>acertos</span>
          </div>
        </div>
      </header>

      <nav className="rail" aria-label="Níveis">
        <div className="levels">
          {levelStats.map((L) => (
            <button key={L.n} className="lvbtn" aria-pressed={!store.verb && store.lv === L.n} onClick={() => setLevel(L.n)}>
              <span className="n">{L.n === 0 ? "Mistura" : `Nível ${L.n}`}</span>
              <span className="t">{L.t}</span>
              <span className="c">
                {ready ? L.done : 0}/{L.total} · {L.s}
              </span>
              <span className="bar">
                <i style={{ width: `${ready && L.total ? ((100 * L.done) / L.total).toFixed(1) : 0}%` }} />
              </span>
            </button>
          ))}
        </div>
      </nav>

      <div className="toolbar">
        <div className="seg" role="group" aria-label="Modo">
          {MODES.map(({ m, label }) => (
            <button key={m} aria-pressed={store.mode === m} onClick={() => setMode(m)}>
              {label}
            </button>
          ))}
        </div>
        <label className="sel" htmlFor={`typeSel-${mod.id}`}>
          Tipo
          <select id={`typeSel-${mod.id}`} value={typeCounts[store.type] ? store.type : "all"} onChange={(e) => setType(e.target.value)}>
            <option value="all">Todos ({pool.length})</option>
            {types.map((t) => (
              <option key={t} value={t}>
                {t} ({typeCounts[t]})
              </option>
            ))}
          </select>
        </label>
        {store.verb && (
          <span className="chip filt">
            Praticando: <b className="es">{verbEntry?.v ?? store.verb}</b>
            <button aria-label="Remover filtro de verbo" onClick={() => update((s) => ({ ...s, verb: null }))}>
              ✕
            </button>
          </span>
        )}
      </div>

      <details className="sheet">
        <summary>{store.lv === 0 || store.verb ? "Quadro geral" : `Ficha de teoria — Nível ${lvInfo.n}: ${lvInfo.t}`}</summary>
        <div className="theory" dangerouslySetInnerHTML={{ __html: mod.theory[store.verb ? 0 : store.lv] ?? mod.theory[0] }} />
      </details>

      <section className="card" ref={cardRef} aria-live="polite">
        {!ready ? (
          <div className="empty">Carregando seu progresso…</div>
        ) : !current ? (
          <div className="empty">{emptyMsg}</div>
        ) : (
          <QuestionCard
            key={`${current.id}-${resetTick}`}
            q={current}
            levelName={mod.levels[current.lv]?.t ?? ""}
            index={idx}
            total={list.length}
            previous={store.r[current.id]}
            onResult={(ok) => record(current, ok)}
            onPrev={() => go(-1)}
            onNext={() => go(1)}
          />
        )}
      </section>

      {ready && list.length > 0 && <QuestionMap list={list} results={store.r} current={idx} onJump={setIdx} />}

      {mod.glossary && (
        <Glossary
          title={mod.glossaryTitle ?? "Lista"}
          entries={mod.glossary}
          active={store.verb}
          results={store.r}
          questions={QUESTIONS}
          onPractice={practiceVerb}
        />
      )}

      <footer>
        <span>
          Atalhos: <b>1–9</b> escolhem a opção · <b>Enter</b> corrige / avança · <b>← →</b> navegam. O progresso de cada
          caderno fica salvo neste navegador.
        </span>
        <ResetButton
          onConfirm={() => {
            resetProgress();
            setResetTick((t) => t + 1);
          }}
        />
      </footer>
    </div>
  );
}
