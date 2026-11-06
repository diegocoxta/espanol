# -*- coding: utf-8 -*-
"""Helpers comuns para montar questões no formato da app (ver lib/types.ts)."""
import json
import random
import re

NAMES = {'María', 'Ana', 'Juan', 'Pedro', 'Lucía', 'Diego', 'Lima', 'Madrid', 'Perú', 'Buenos', 'Aires', 'WhatsApp', 'Navidad', 'Cervantes'}


def cap(s):
    for i, c in enumerate(s):
        if c.isalpha():
            return s[:i] + c.upper() + s[i + 1:]
    return s


def low(s):
    w = s.split(' ')
    if w[0] in NAMES:
        return s
    return w[0][0].lower() + w[0][1:] + ('' if len(w) == 1 else ' ' + ' '.join(w[1:]))


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[—–¿?¡!.,;:"«»“”()]', ' ', s.lower())).strip()


class Bank:
    def __init__(self, seed):
        self.R = random.Random(seed)
        self.items = []
        self._seen = set()

    def _add(self, d):
        key = (d['t'], d['q'], d['s'], json.dumps(d.get('w'), ensure_ascii=False), json.dumps(d.get('o'), ensure_ascii=False))
        if key in self._seen:
            return None
        self._seen.add(key)
        self.items.append(d)
        return d

    def base(self, lv, k, t, q, s, v, x, gen, **kw):
        d = dict(lv=lv, k=k, t=t, q=q, s=s, x=x, v=list(v) if isinstance(v, (list, tuple)) else [v], gen=gen)
        d.update(kw)
        return self._add(d)

    def mc(self, lv, k, q, s, opts, correct, x, v, gen, shuffle=True):
        opts = list(dict.fromkeys(opts))
        if correct not in opts:
            raise ValueError((q, s, opts, correct))
        if len(opts) < 2:
            return None
        if shuffle:
            self.R.shuffle(opts)
        return self.base(lv, k, 'mc', q, s, v, x, gen, o=opts, a=opts.index(correct))

    def inp(self, lv, k, q, s, answers, x, v, gen):
        return self.base(lv, k, 'in', q, s, v, x, gen, a=list(dict.fromkeys(answers)))

    def err(self, lv, sentence, bad, fix, x, v, gen, q='Clique na palavra com erro — ou em “Não há erro”.'):
        w = sentence.split(' ')
        if isinstance(bad, int):
            bad = [bad] if bad >= 0 else []
        assert all(0 <= b < len(w) for b in bad), (sentence, bad)
        return self.base(lv, 'Encontrar o erro', 'err', q, '', v, x, gen, w=w, a=bad, fix=fix)

    def ordq(self, lv, q, sentence, alts, x, v, gen):
        toks = sentence.rstrip('.?!').replace('¿', '').replace('¡', '').split(' ')
        toks = [t if t in NAMES else t.lower() for t in toks]
        answers = [norm(a) for a in [sentence] + list(alts)]
        return self.base(lv, 'Ordenar', 'ord', q, '', v, x, gen, w=toks, a=list(dict.fromkeys(answers)))


def select(items, entry_ids, minc, targets, cap_per_entry, seed, always_gens=('hand',), prio=(), gen_cap=0.3):
    """Seleciona questões garantindo cobertura mínima por verbo e completando cada nível até a meta."""
    R = random.Random(seed)
    chosen, cnt = [], {e: 0 for e in entry_ids}
    used = set()

    def take(i):
        used.add(i)
        chosen.append(items[i])
        for v in items[i]['v']:
            cnt[v] = cnt.get(v, 0) + 1

    for i, it in enumerate(items):
        if it['gen'] in always_gens:
            take(i)
    by_entry = {e: [] for e in entry_ids}
    for i, it in enumerate(items):
        for v in it['v']:
            by_entry.setdefault(v, []).append(i)
    order = list(entry_ids)
    R.shuffle(order)
    for e in order:
        pool = [i for i in by_entry.get(e, []) if i not in used]
        R.shuffle(pool)
        gens_used = set(items[i]['gen'] for i in by_entry.get(e, []) if i in used)
        for group in prio:  # garante um item de cada grupo prioritário (ex.: vocabulário, gramática central)
            if any(items[i]['gen'] in group for i in by_entry.get(e, []) if i in used):
                continue
            cands = [i for i in pool if items[i]['gen'] in group]
            if cands:
                i = cands[0]
                pool.remove(i)
                take(i)
                gens_used.add(items[i]['gen'])
        pool.sort(key=lambda i: items[i]['gen'] in gens_used)  # gerador ainda não usado primeiro
        while cnt.get(e, 0) < minc and pool:
            i = pool.pop(0)
            if i in used:
                continue
            take(i)
            gens_used.add(items[i]['gen'])
            pool.sort(key=lambda j: items[j]['gen'] in gens_used)
    for lv, tgt in sorted(targets.items()):
        have = sum(1 for it in chosen if it['lv'] == lv)
        pool = [i for i, it in enumerate(items) if it['lv'] == lv and i not in used]
        R.shuffle(pool)
        per_gen = {}
        for it in chosen:
            if it['lv'] == lv:
                per_gen[it['gen']] = per_gen.get(it['gen'], 0) + 1
        for i in pool:
            if have >= tgt:
                break
            g = items[i]['gen']
            if any(cnt.get(v, 0) >= cap_per_entry for v in items[i]['v']) or per_gen.get(g, 0) >= gen_cap * tgt:
                continue
            take(i)
            per_gen[g] = per_gen.get(g, 0) + 1
            have += 1
    return chosen, cnt


def finalize(chosen, seed):
    R = random.Random(seed)
    out = []
    for lv in sorted(set(q['lv'] for q in chosen)):
        L = [q for q in chosen if q['lv'] == lv]
        R.shuffle(L)
        out += L
    for i, q in enumerate(out):
        q['id'] = i + 1
        q.pop('gen', None)
    return out
