import type { Question } from "./types";

export interface Level {
  n: number;
  t: string;
  s: string;
}

export interface GlossEntry {
  id: string;
  v: string;
  cat: string;
  kind: string;
  pt: string;
  ex: string;
  note: string;
  base: string;
  base_pt: string;
  /** quantas questões do caderno praticam este item */
  n: number;
}

export interface ModuleMeta {
  id: string;
  href: string;
  /** rótulo curto da aba */
  tab: string;
  tabSub: string;
  eyebrow: string;
  titleA: string;
  titleMark: string;
  intro: string;
  storageKey: string;
  levels: Level[];
  glossaryTitle?: string;
}

export interface ModuleDef extends ModuleMeta {
  questions: Question[];
  theory: Record<number, string>;
  glossary?: GlossEntry[];
}

export const MODULES: ModuleMeta[] = [
  {
    id: "objeto",
    href: "/",
    tab: "Objeto direto e indireto",
    tabSub: "lo, la, le, se lo…",
    eyebrow: "Cuaderno de práctica · español",
    titleA: "Pronombres de",
    titleMark: "objeto",
    intro: "Objeto direto e indireto do básico ao extremo",
    storageKey: "pronombres-objeto-v1",
    levels: [
      { n: 0, t: "Tudo", s: "Todos os níveis" },
      { n: 1, t: "Básico", s: "lo, la, los, las" },
      { n: 2, t: "Elementar", s: "pessoas, OI e “a”" },
      { n: 3, t: "Intermediário", s: "se lo, me lo…" },
      { n: 4, t: "Avançado", s: "posição e acentos" },
      { n: 5, t: "Muito avançado", s: "gustar, leísmo, lo neutro" },
      { n: 6, t: "Extremo", s: "norma e casos-limite" },
    ],
  },
  {
    id: "pronominales",
    href: "/pronominales/",
    tab: "Verbos com pronome",
    tabSub: "me gusta × me levanto",
    eyebrow: "Cuaderno de práctica · español",
    titleA: "Verbos con",
    titleMark: "pronombre",
    intro: "Tipo gustar, pronominais, reflexivos, recíprocos e ênfase, do básico ao extremo",
    storageKey: "verbos-pronominales-v1",
    glossaryTitle: "Lista de verbos",
    levels: [
      { n: 0, t: "Tudo", s: "Todos os níveis" },
      { n: 1, t: "Básico", s: "me gusta × me levanto" },
      { n: 2, t: "Elementar", s: "tipo gustar, rotina" },
      { n: 3, t: "Intermediário", s: "passado e preposições" },
      { n: 4, t: "Avançado", s: "posição e acentos" },
      { n: 5, t: "Muito avançado", s: "sentido, ênfase, caer" },
      { n: 6, t: "Extremo", s: "me gustas, de que" },
    ],
  },
  {
    id: "usos-del-se",
    href: "/usos-del-se/",
    tab: "Usos do se",
    tabSub: "9 usos + se/sé/si/sí",
    eyebrow: "Cuaderno de práctica · español",
    titleA: "Los usos del",
    titleMark: "se",
    intro: "Os nove usos do se, do reflexivo ao passivo, e a diferença entre se, sé, si e sí",
    storageKey: "usos-del-se-v1",
    glossaryTitle: "Usos e verbos",
    levels: [
      { n: 0, t: "Tudo", s: "Todos os níveis" },
      { n: 1, t: "Básico", s: "reflexivo, recíproco, si/sí" },
      { n: 2, t: "Elementar", s: "passivo, impessoal, se lo" },
      { n: 3, t: "Intermediário", s: "mudança espontânea" },
      { n: 4, t: "Avançado", s: "roteiro e classificação" },
      { n: 5, t: "Muito avançado", s: "pessoas e infinitivos" },
      { n: 6, t: "Extremo", s: "perífrase, uno se" },
    ],
  },
];

export const metaById = (id: string) => MODULES.find((m) => m.id === id)!;
