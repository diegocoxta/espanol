/** Normaliza para comparar respostas: minúsculas, sem pontuação, espaços simples. Mantém acentos. */
export const norm = (s: string) =>
  s.toLowerCase().replace(/[—–¿?¡!.,;:"«»“”()]/g, " ").replace(/\s+/g, " ").trim();

/** Remove acentos — usado só para avisar "quase, confira os acentos". */
export const deacc = (s: string) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

const ESC: Record<string, string> = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };
export const esc = (s: string) => String(s).replace(/[&<>"]/g, (c) => ESC[c]);

export function seeded(n: number) {
  let x = n * 9301 + 49297;
  return () => (x = (x * 9301 + 49297) % 233280) / 233280;
}

export function shuffle<T>(arr: T[], rnd: () => number = Math.random): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Converte a frase do banco em HTML: [[x]] vira <mark>, ___ vira a lacuna (preenchida após responder). */
export function sentenceHTML(s: string, fill?: { text: string; ok: boolean }) {
  const blank = fill
    ? `<span class="blank ${fill.ok ? "ok" : "bad"}">${esc(fill.text)}</span>`
    : `<span class="blank">&nbsp;</span>`;
  return s.replace(/\[\[(.+?)\]\]/g, "<mark>$1</mark>").replace(/___/g, blank);
}

export const capFirst = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);
