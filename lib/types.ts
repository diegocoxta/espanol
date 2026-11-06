export type Mode = "seq" | "rand" | "new" | "wrong";

interface QBase {
  id: number;
  /** nível 1–6 */
  lv: number;
  /** tipo de exercício (Completar, Substituir…) */
  k: string;
  /** enunciado (pode conter HTML simples) */
  q: string;
  /** frase em espanhol; [[x]] = destaque, ___ = lacuna */
  s: string;
  /** explicação em HTML simples */
  x: string;
  /** ids dos verbos/usos do glossário que a questão pratica */
  v?: string[];
}

export interface QMC extends QBase { t: "mc"; o: string[]; a: number }
export interface QIN extends QBase { t: "in"; a: string[] }
export interface QERR extends QBase { t: "err"; w: string[]; a: number[]; fix: string }
export interface QORD extends QBase { t: "ord"; w: string[]; a: string[] }

export type Question = QMC | QIN | QERR | QORD;

/** 1 = acertou, 0 = errou (última tentativa) */
export type Results = Record<string, 0 | 1>;

export interface Store {
  r: Results;
  lv: number;
  mode: Mode;
  type: string;
  /** última questão vista por seleção (nível|tipo|verbo) */
  pos: Record<string, number>;
  /** filtro por verbo/uso do glossário */
  verb: string | null;
}

/** Resultado que cada tipo de questão devolve ao card ao ser respondido. */
export interface Outcome {
  ok: boolean;
  /** linha de resposta/correção em HTML (opcional) */
  answer?: string;
}
