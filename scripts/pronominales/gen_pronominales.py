# -*- coding: utf-8 -*-
"""Gera data/pronominales.json (questões) e data/pronominales-verbos.json (glossário com cobertura).

Uso: python3 scripts/pronominales/gen_pronominales.py data
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from conj import conj, attach, strip, place, stress_idx, ACC  # noqa: E402
from catalog import GUSTAR, PRON, ALL  # noqa: E402
from qlib import Bank, cap, low, select, finalize  # noqa: E402

B = Bank(20261105)
R = B.R
BYID = {e['id']: e for e in ALL}
REF = ['me', 'te', 'se', 'nos', 'os', 'se']
ESTAR = 'estoy estás está estamos estáis están'.split()
AUX = [('ir a', 'voy a|vas a|va a|vamos a|vais a|van a'), ('querer', 'quiero|quieres|quiere|queremos|queréis|quieren'),
       ('tener que', 'tengo que|tienes que|tiene que|tenemos que|tenéis que|tienen que'), ('poder', 'puedo|puedes|puede|podemos|podéis|pueden'),
       ('deber', 'debo|debes|debe|debemos|debéis|deben'), ('acabar de', 'acabo de|acabas de|acaba de|acabamos de|acabáis de|acaban de')]
AUX = [(a, f.split('|')) for a, f in AUX]

SUBJ = [("Yo", 0, True), ("Tú", 1, True), ("Mi padre", 2, False), ("María", 2, False), ("Nosotros", 3, True), ("Vosotros", 4, True),
        ("Mis hijos", 5, False), ("Ustedes", 5, True), ("Usted", 2, True), ("Los niños", 5, False), ("Ana", 2, False),
        ("Mis amigos", 5, False), ("Mi hermana", 2, False), ("Juan", 2, False)]
SUBJ_MSG = [("Yo", 0, True), ("Tú", 1, True), ("Mi padre", 2, False), ("Juan", 2, False), ("Mi hermano", 2, False)]
SUBJ_PL = [("Nosotros", 3, True), ("Vosotros", 4, True), ("Juan y Ana", 5, False), ("Mis padres", 5, False), ("Ustedes", 5, True),
           ("Los dos hermanos", 5, False), ("Tú y yo", 3, False)]
ADULT = {'emborracharse', 'divorciarse', 'casarse', 'afeitarse', 'rasurarse', 'maquillarse', 'depilarse', 'jactarse', 'fugarse',
         'vanagloriarse', 'cabrearse', 'pintarse', 'fumarse (ênfase)', 'apropiarse', 'adueñarse', 'apoderarse'}
HABIT = ('los domingos', 'cada', 'todos los', 'a menudo', 'entre semana', 'con frecuencia', 'en invierno', 'en verano', 'en otoño', 'fácilmente', 'con facilidad')
PASTW = ('pasad', 'ayer', 'anoche', 'en 2020', 'hace años')
TM = ['Ayer', 'El sábado', 'Anoche', 'La semana pasada', 'Esa tarde']
NO_DROP = {'darse cuenta', 'enfermarse', 'casarse', 'calmarse', 'entristecerse', 'mirarse', 'desayunarse', 'cuidarse'}
PREPS = ['de', 'a', 'en', 'por', 'con', 'contra', 'para']
CJ = {}


def cj(verb, cls=''):
    k = (verb, cls)
    if k not in CJ:
        CJ[k] = conj(verb, cls)
    return CJ[k]


def subjects(e):
    f = e['flags']
    if 'pl' in f.split():
        L = SUBJ_PL
    elif 'masc' in f:
        L = SUBJ_MSG
    else:
        L = SUBJ
    if e['name'] in ADULT:
        L = [s for s in L if s[0] not in ('Los niños', 'Mis hijos')]
    return L


def usable(e):
    return e['tails'] and 'special' not in e['flags'] and 'sensitive' not in e['flags'] and e['grp'] != 'enf'


def inf_of(e):
    return e['verb'] + 'se'


def disp(e):
    """nome do verbo para enunciados"""
    return e['name'].split(' (')[0]


def sent(s):
    s = cap(s)
    return s if s.endswith(('.', '!', '?', '...')) else s + '.'


def pres_tails(e):
    return [t for t in e['tails'] if not any(w in t for w in PASTW)] or e['tails']


def pret_tails(e):
    return [t for t in e['tails'] if not any(w in t for w in HABIT)]



CLUSTERS = [
    'gustar encantar chiflar flipar enloquecer|volver loco apasionar fascinar agradar complacer atraer seducir entusiasmar tentar apetecer antojarse provocar|dar ganas',
    'desagradar disgustar molestar fastidiar irritar enfadar enojar cabrear indignar hartar cansar|dar rabia|sacar de quicio|tener harto repugnar asquear|dar asco ofender',
    'asustar espantar aterrar horrorizar|dar miedo inquietar preocupar angustiar agobiar estresar desesperar perturbar|poner nervioso obsesionar',
    'entristecer apenar deprimir|doler (emocional) decepcionar defraudar frustrar|dar pena|dar lástima|poner triste / contento pesar',
    'alegrar divertir emocionar ilusionar animar motivar entusiasmar|hacer ilusión|hacer feliz|hacer gracia|dar risa entretener conmover enternecer inspirar|caer en gracia',
    'impresionar maravillar asombrar sorprender chocar escandalizar extrañar|llamar la atención intrigar|dar curiosidad',
    'tranquilizar relajar reconfortar satisfacer complacer halagar enorgullecer',
    'importar interesar|dar igual|dar lo mismo|dar exactamente igual|traer sin cuidado|tener sin cuidado incumbir corresponder pertenecer tocar afectar',
    'faltar|hacer falta urgir bastar alcanzar sobrar|quedar (restar) convenir servir beneficiar perjudicar',
    'pasar suceder|ocurrir (ideia)', '|dar vergüenza|dar pena avergonzar humillar', '|sonar (familiar)|sonar bien / mal parecer',
    '|caer bien / mal|caer gordo|caer en gracia|sentar bien / mal (atitude)',
    'obstinarse empecinarse', 'mudarse trasladarse', 'aburrirse cansarse hartarse', 'asustarse espantarse', 'sorprenderse asombrarse',
    'entristecerse deprimirse', 'enfermarse resfriarse', 'equivocarse confundirse', 'calmarse tranquilizarse relajarse',
    'subirse montarse', 'tirarse lanzarse', 'escaparse fugarse', 'fijarse percatarse|darse cuenta', 'enojarse enfadarse cabrearse molestarse',
    'agobiarse estresarse desesperarse inquietarse preocuparse', 'alegrarse emocionarse ilusionarse animarse entusiasmarse',
]
STOP = {'ficar', 'fazer', 'deixar', 'dar', 'com', 'para', 'algo', 'bem', 'mal', 'sem', 'Lat', 'coloq', 'Espanha', 'ênfase'}


def _names(row):
    out = set()
    # nomes compostos vêm separados por '|'; nomes simples, por espaço
    for chunk in row.split('|'):
        chunk = chunk.strip()
        if not chunk:
            continue
        out.add(chunk)
        out.update(chunk.split(' '))
    return out


CL_SETS = [_names(r) for r in CLUSTERS]


def _tok(pt):
    import re as _re
    return {w.lower() for w in _re.split(r"[^\wÀ-ÿ-]+", pt) if len(w) > 3 and w not in STOP}


def same_cluster(a, b):
    a, b = a.split(' (')[0], b.split(' (')[0]
    return any(a in S and b in S for S in CL_SETS)


def distractors(e, pool, n=3):
    bad_t = _tok(e['pt'])
    ok = []
    for o in pool:
        if o['id'] == e['id'] or o['pt'] == e['pt'] or (_tok(o['pt']) & bad_t) or same_cluster(o['name'], e['name']) or 'sensitive' in o.get('flags', ''):
            continue
        if o['pt'] in [x['pt'] for x in ok]:
            continue
        ok.append(o)
    R.shuffle(ok)
    return [o['pt'] for o in ok[:n]]


ACC_NOTE = 'Ao juntar o pronome, a palavra passa a ter a tônica na antepenúltima sílaba → leva acento.'

# ============================================================== PRONOMINAIS
for e in PRON:
    if not usable(e):
        continue
    c = cj(e['verb'], e['cls'])
    v = e['id']
    grp, tier = e['grp'], e['tier']
    nm = disp(e)
    S = subjects(e)
    PT = pres_tails(e)
    QT = pret_tails(e)
    basic = (grp == 'rot' and tier == 1)

    # PA — escolher o pronome (presente)
    for s, i, isp in S:
        for t in PT:
            lv = 1 if basic else (3 if tier == 3 else 2)
            x = f"Sujeito ‘{s}’ → <b>{REF[i]}</b> {c['pres'][i]}. Nos verbos pronominais o pronome acompanha a pessoa (me, te, se, nos, os, se)."
            if grp == 'rec':
                x += ' Aqui o sentido é recíproco (um ao outro), por isso só aparece no plural.'
            B.mc(lv, 'Completar', 'Complete com o pronome.', f"{s} ___ {c['pres'][i]} {t}.", REF[:5], REF[i], x, v, 'PA', shuffle=False)

    # PB — conjugar no presente (mudança de raiz)
    reg_stem = e['verb'][:-2]
    for s, i, isp in S:
        for t in PT:
            corr = c['pres'][i]
            opts = [corr, c['pres'][(i + 1) % 6], c['pres'][(i + 3) % 6]]
            if e['cls']:
                alt = cj(e['verb'])['pres'][i]
                if alt == corr and corr.startswith(reg_stem):
                    alt = c['pres'][5][:-2] + corr[len(reg_stem):]
                opts.append(alt)
            opts = [o for o in dict.fromkeys(opts)]
            if len(opts) < 3:
                continue
            note = f" Repare na mudança de raiz ({c['pres'][0]}, {c['pres'][3]})." if e['cls'] else ''
            B.mc(3 if tier == 3 else 2, 'Conjugar', f'Complete com <i>{nm}</i> no presente.', f"{s} {REF[i]} ___ {t}.", opts, corr,
                 f"{s} → <b>{REF[i]} {corr}</b>: o verbo concorda com a pessoa, e o pronome também.{note}", v, 'PB')

    # PC — pretérito
    for s, i, isp in S:
        for t in QT:
            tm = R.choice(TM)
            corr = c['pret'][i]
            opts = [corr, c['pres'][i], c['pret'][(i + 2) % 6]]
            alt = cj(e['verb'])['pret'][i]
            if alt != corr:
                opts.append(alt)
            B.mc(3, 'Conjugar', f'Complete com <i>{nm}</i> no pretérito indefinido.', f"{tm} {low(s)} {REF[i]} ___ {t}.", opts, corr,
                 f"Pretérito de {nm}, pessoa ‘{low(s)}’: <b>{REF[i]} {corr}</b>." + (f" Atenção à raiz: {c['pret'][2]}, {c['pret'][5]}." if c['pret'][2][:3] != e['verb'][:3] or e['cls'] in ('i', 'ie-i', 'ue-u') else ''), v, 'PC')

    # PE — preposição de regência
    if e['prep']:
        for s, i, isp in S:
            for t in e['tails']:
                w = t.split(' ')
                j = 0 if w[0] == e['prep'] else (1 if len(w) > 1 and w[0] == 'cuenta' and w[1] == e['prep'] else -1)
                if j < 0:
                    continue
                rest = ' '.join(w[:j] + ['___'] + w[j + 1:])
                opts = [e['prep']] + R.sample([p for p in PREPS if p != e['prep']], 3)
                B.mc(3, 'Completar', 'Complete com a preposição.', f"{s} {REF[i]} {c['pres'][i]} {rest}.", opts, e['prep'],
                     f"<b>{nm} {e['prep']}</b> algo: a preposição faz parte da regência do verbo.", v, 'PE')

    # PF — encontrar o erro (pronome faltando / pronome errado)
    drop_ok = grp in ('so', 'emo', 'rot', 'mov') and 'nodrop' not in e['flags'] and 'od' not in e['flags'] and nm not in NO_DROP
    for s, i, isp in S:
        for t in PT:
            n = len(s.split(' '))
            verb = c['pres'][i]
            kind = R.choice((['drop', 'drop'] if drop_ok else []) + (['wrong'] if i in (0, 1, 3, 4) else []) + ['ok'])
            good = f"{s} {REF[i]} {verb} {t}."
            if kind == 'drop':
                B.err(3, f"{s} {verb} {t}.", [n], good,
                      f"Falta o pronome: <b>{nm}</b> é pronominal, e o pronome é obrigatório → {REF[i]} {verb}.", v, 'PF')
            elif kind == 'wrong':
                wr = 'se'
                B.err(3, f"{s} {wr} {verb} {t}.", [n], good,
                      f"O pronome concorda com o sujeito ‘{s}’: <b>{REF[i]}</b> {verb}. <i>Se</i> só combina com 3ª pessoa (él, ella, usted, ellos, ustedes).", v, 'PF')
            else:
                B.err(3, good, -1, good, f"Correto: ‘{s}’ → {REF[i]} {verb}.", v, 'PF')

    # PG — imperativo afirmativo (tú / usted)
    if e['aff'] is not None and grp != 'rec':
        tail = (' ' + e['aff']) if e['aff'] else ''
        f_tu = attach(c['tu'], 'te')
        B.inp(4, 'Imperativo', 'Dê a ordem para <b>tú</b> (imperativo afirmativo).', f"(tú) {inf_of(e)}{tail}", [cap(f_tu) + tail + '.'],
              f"Imperativo afirmativo: pronome <b>depois</b>, colado ao verbo → <b>{cap(f_tu)}</b>." + (' ' + ACC_NOTE if f_tu != strip(f_tu) else ' (Sem acento: a palavra continua paroxítona.)'), v, 'PG')
        f_ud = attach(c['ud'], 'se')
        B.inp(4, 'Imperativo', 'Dê a ordem para <b>usted</b> (imperativo afirmativo).', f"(usted) {inf_of(e)}{tail}", [cap(f_ud) + tail + '.'],
              f"Com <i>usted</i> usa-se o subjuntivo ({c['ud']}) + <b>se</b> colado: <b>{cap(f_ud)}</b>.", v, 'PG')
        # ortografia
        wrong_sep = f"{c['tu']} te"
        noacc = strip(f_tu)
        cand = [f_tu, noacc, wrong_sep]
        j = max(k for k, ch in enumerate(noacc) if ch in 'aeiou')
        bad_acc = noacc[:j] + ACC[noacc[j]] + noacc[j + 1:]
        if bad_acc not in cand:
            cand.append(bad_acc)
        B.mc(4, 'Ortografia', 'Qual é a grafia correta do imperativo (tú)?', f"{inf_of(e)} → ¡___{tail}!", cand, f_tu,
             f"<b>{f_tu}</b>: o pronome vai colado ao imperativo afirmativo." + (' ' + ACC_NOTE if f_tu != noacc else ' Sem acento: a palavra continua paroxítona terminada em vogal.'), v, 'PK')
        # nosotros / vosotros
        f_nos = attach(c['nos'], 'nos', 'nos')
        w1 = place(strip(c['nos']) + 'nos', stress_idx(c['nos']))
        B.mc(6 if tier >= 2 else 4, 'Ortografia', 'Imperativo de <b>nosotros</b>: qual é a forma correta?', f"{inf_of(e)} → ¡___{tail}!",
             [f_nos, w1, strip(f_nos), c['nos'] + ' nos'], f_nos,
             f"<i>{c['nos']}</i> + nos: o <b>-s final cai</b> antes de <i>nos</i> e a forma leva acento → <b>{f_nos}</b>.", v, 'PK')
        if e['verb'] != 'ir':
            f_vos = attach(c['vos'], 'os', 'vos')
            B.mc(6, 'Ortografia', 'Imperativo de <b>vosotros</b> (norma culta): qual é a forma correta?', f"{inf_of(e)} → ¡___{tail}!",
                 [f_vos, strip(c['vos'][:-1]) + 'dos', c['vos'][:-1] + 'ros', c['vos'] + ' os'], f_vos,
                 f"<i>{c['vos']}</i> + os: o <b>-d cai</b> → <b>{f_vos}</b>. A forma com -r (<i>{c['vos'][:-1]}ros</i>) é muito comum na fala, mas a norma culta prefere <i>{f_vos}</i>." + (' O acento marca o hiato.' if 'í' in f_vos else ''), v, 'PK')

    # PH — imperativo negativo
    if e['neg'] is not None and grp != 'rec':
        tail = (' ' + e['neg']) if e['neg'] else ''
        B.inp(4, 'Imperativo', 'Dê a ordem <b>negativa</b> para <b>tú</b>.', f"(tú, negativo) {inf_of(e)}{tail}", [f"No te {c['subj'][1]}{tail}."],
              f"No imperativo negativo o pronome vai <b>antes</b>, e o verbo vai no subjuntivo: <b>No te {c['subj'][1]}</b>.", v, 'PH')
        if e['aff'] is not None:
            ta = (' ' + e['aff']) if e['aff'] else ''
            B.inp(4, 'Transformar', 'Passe para o negativo (mantendo o complemento).', f"{cap(attach(c['tu'], 'te'))}{ta}.",
                  [f"No te {c['subj'][1]}{ta}."], f"Afirmativo: pronome depois e colado. Negativo: <b>No te {c['subj'][1]}</b> (pronome antes, subjuntivo).", v, 'PH')

    # PI / PJ — perífrase e gerúndio
    for s, i, isp in S:
        for t in PT:
            a, forms = R.choice(AUX)
            before = f"{s} {REF[i]} {forms[i]} {e['verb']} {t}."
            after = f"{s} {forms[i]} {attach(e['verb'], REF[i])} {t}."
            src, dst = (before, after) if R.random() < .5 else (after, before)
            ans = [dst]
            if isp and not s.startswith('Us'):
                ans.append(cap(dst.split(' ', 1)[1]))
            B.inp(4, 'Posição', 'Reescreva colocando o pronome na <b>outra</b> posição possível.', src, ans,
                  f"Com perífrase há duas posições: antes do verbo conjugado (<i>{REF[i]} {forms[i]} {e['verb']}</i>) ou colado ao infinitivo (<i>{forms[i]} {attach(e['verb'], REF[i])}</i>). Infinitivo + 1 pronome não leva acento.", v, 'PI')
            g1 = f"{s} {REF[i]} {ESTAR[i]} {c['ger']} {t}."
            g2 = f"{s} {ESTAR[i]} {attach(c['ger'], REF[i])} {t}."
            src, dst = (g1, g2) if R.random() < .6 else (g2, g1)
            ans = [dst]
            if isp and not s.startswith('Us'):
                ans.append(cap(dst.split(' ', 1)[1]))
            B.inp(4, 'Posição', 'Reescreva colocando o pronome na <b>outra</b> posição possível.', src, ans,
                  f"Com <i>estar</i> + gerúndio: <i>{REF[i]} {ESTAR[i]} {c['ger']}</i> = <i>{ESTAR[i]} <b>{attach(c['ger'], REF[i])}</b></i>. Gerúndio + pronome sempre leva acento.", v, 'PJ')

    # PT1 — teste rápido: passar para tú (nível 1, rotina)
    if grp in ('rot', 'emo', 'mov') and tier == 1:
        for t in PT:
            B.inp(1 if grp == 'rot' else 2, 'Transformar', 'Teste rápido: reescreva a frase para <b>tú</b>.', f"Me {c['pres'][0]} {t}.",
                  [f"Te {c['pres'][1]} {t}.", f"Tú te {c['pres'][1]} {t}."],
                  f"Ao trocar a pessoa, <b>o verbo também muda</b> (me {c['pres'][0]} → te {c['pres'][1]}): é verbo pronominal, não tipo gustar.", v, 'PT1')

# ---- sentido (significado) para todos os pronominais (inclui especiais)
for grp in set(e['grp'] for e in PRON):
    G = [e for e in PRON if e['grp'] == grp]
    for e in G:
        ds = distractors(e, G)
        if len(ds) < 3:
            ds += [d for d in distractors(e, PRON, 8) if d not in ds][:3 - len(ds)]
        lv = 3 if (e['tier'] == 3 or grp == 'sen') else 2
        note = ' (uso narrativo)' if 'sensitive' in e['flags'] else ''
        B.mc(lv, 'Vocabulário', f"Na frase, <b>{disp(e)}</b> significa:", sent(e['ex']) + note,
             [e['pt']] + ds, e['pt'], f"<b>{disp(e)}</b> = {e['pt']}. Exemplo: <i>{e['ex']}</i>.", e['id'], 'PD')
        if e['base']:
            ob = list(dict.fromkeys(o['base_pt'] for o in G if o['base'] and o['base_pt'] != e['base_pt']))
            B.mc(3, 'Vocabulário', f"<b>Sem</b> o pronome, <b>{e['base']}</b> significa:", sent(e['base_ex']), [e['base_pt']] + R.sample(ob, 3), e['base_pt'],
                 f"<b>{e['base']}</b> = {e['base_pt']}; <b>{disp(e)}</b> = {e['pt']}. O pronome muda o sentido.", e['id'], 'PD2')

# ---- ênfase
DOBJ = {
    'comer': [("la pizza", 'la'), ("el pastel", 'lo'), ("las galletas", 'las')], 'beber': [("la cerveza", 'la'), ("el zumo", 'lo'), ("los refrescos", 'los')],
    'tomar': [("el café", 'lo'), ("la sopa", 'la'), ("las pastillas", 'las')], 'leer': [("el libro", 'lo'), ("la novela", 'la'), ("los apuntes", 'los')],
    'aprender': [("la canción", 'la'), ("los verbos", 'los'), ("el poema", 'lo')], 'saber': [("la letra", 'la'), ("los nombres", 'los')],
    'fumar': [("el puro", 'lo'), ("los cigarrillos", 'los')], 'gastar': [("el sueldo", 'lo'), ("la herencia", 'la')], 'ganar': [("el premio", 'lo'), ("la beca", 'la')],
    'ver': [("la serie", 'la'), ("el partido", 'lo')], 'tragar': [("la mentira", 'la'), ("el chicle", 'lo')],
    'poner': [("el abrigo", 'lo'), ("la chaqueta", 'la'), ("los guantes", 'los'), ("las botas", 'las')], 'quitar': [("el abrigo", 'lo'), ("los zapatos", 'los'), ("las gafas", 'las')],
    'lavar': [("las manos", 'las'), ("la cara", 'la'), ("el pelo", 'lo')], 'cepillar': [("los dientes", 'los'), ("el pelo", 'lo')],
    'probar': [("el vestido", 'lo'), ("la camisa", 'la'), ("los zapatos", 'los')], 'secar': [("el pelo", 'lo'), ("las manos", 'las')],
    'pintar': [("las uñas", 'las'), ("los labios", 'los')], 'cortar': [("el pelo", 'lo'), ("las uñas", 'las')], 'calzar': [("las botas", 'las')],
    'llevar': [("el abrigo", 'lo'), ("el dinero", 'lo')], 'conocer': [("la ciudad", 'la'), ("el barrio", 'lo')],
}
VID = {'poner': 'p:ponerse', 'quitar': 'p:quitarse', 'lavar': 'p:lavarse', 'cepillar': 'p:cepillarse', 'probar': 'p:probarse', 'secar': 'p:secarse',
       'pintar': 'p:pintarse', 'cortar': 'p:cortarse', 'calzar': 'p:calzarse', 'llevar': 'p:llevarse'}
for e in PRON:
    if e['grp'] == 'enf':
        VID.setdefault(e['verb'], e['id'])
VID['conocer'] = 'p:conocerse (ênfase)'
VID['ver'] = 'p:verse (ênfase)'
CLS = {'probar': 'ue'}
DOUBLE_S = [("Yo", 0), ("Tú", 1), ("Mi hermano", 2), ("Nosotros", 3), ("Mis primos", 5)]

for e in PRON:
    if e['grp'] != 'enf':
        continue
    c = cj(e['verb'], e['cls'])
    v = e['id']
    nm = disp(e)
    if e['verb'] in ('esperar', 'subir'):
        f = attach(c['tu'], 'te')
        jobs = [(e['verb'], t) for t in e['tails']] if e['verb'] == 'esperar' else [('subir', 'al coche'), ('subir', 'a la moto'), ('bajar', 'del autobús'), ('bajar', 'aquí')]
        for vb, t in jobs:
            fv = attach(cj(vb)['tu'], 'te')
            B.inp(5, 'Imperativo', 'Dê a ordem para <b>tú</b> com o pronome de ênfase.', f"(tú) {vb}se {t}", [cap(fv) + ' ' + t + '.'],
                  f"<b>{cap(fv)}</b>: o pronome deixa a ordem mais próxima e enfática (‘espera aí’, ‘sobe aí’).", v, 'EN1')
        B.mc(5, 'Ênfase', 'Qual a diferença?', f"‘{cap(c['tu'])} {e['tails'][0]}.’ × ‘{cap(f)} {e['tails'][0]}.’",
             ['O sentido é o mesmo; com o pronome soa mais enfático e coloquial', 'Com pronome a ação é recíproca', 'Sem pronome a frase está errada', 'Com pronome a ação foi sem querer'],
             'O sentido é o mesmo; com o pronome soa mais enfático e coloquial', 'Pronome de ênfase: pode sair sem a frase ficar errada, mas ela perde força.', v, 'EN1')
        continue
    S2 = [("Yo", 0), ("Tú", 1), ("Mi hermano", 2), ("Nosotros", 3), ("Mis primos", 5)]
    for s, i in (S2 if e['verb'] not in ('saber', 'conocer') else []):
        for q in e['tails']:
            B.mc(5, 'Ênfase', 'Complete com a forma que dá a ideia de “tudo, até o fim”.', f"{s} ___ {q}.",
                 [f"{REF[i]} {c['pret'][i]}", c['pret'][i], f"{REF[(i + 1) % 5]} {c['pret'][i]}", f"{REF[i]} {c['pret'][(i + 2) % 6]}"], f"{REF[i]} {c['pret'][i]}",
                 f"<b>{REF[i]} {c['pret'][i]}</b> {q}: o pronome de ênfase concorda com o sujeito e pede objeto definido/quantificado. Sem ele (<i>{c['pret'][i]} {q}</i>) a frase continua correta, só perde força.", v, 'EN2')
            for b in e['bare']:
                strange = f"{s} {REF[i]} {c['pret'][i]} {b}."
                B.mc(5, 'Ênfase', 'Qual frase soa <b>estranha</b> para um nativo?', '',
                     [strange, f"{s} {REF[i]} {c['pret'][i]} {q}.", f"{s} {c['pret'][i]} {b}.", f"{s} {c['pret'][i]} {q}."], strange,
                     f"O <i>se</i> de ênfase pede objeto <b>definido ou quantificado</b> ({q}). Com um objeto genérico (‘{b}’) ele soa estranho; sem o pronome, as duas versões funcionam.", v, 'EN3')
                break
    if e['verb'] in ('saber', 'conocer'):
        for s, i in S2:
            for q in e['tails']:
                B.mc(5, 'Conjugar', f'Complete com <i>{nm}</i> no presente.', f"{s} {REF[i]} ___ {q}.", list(dict.fromkeys([c['pres'][i], c['pres'][(i + 1) % 6], cj(e['verb'])['pret'][i], c['pres'][0] if i else c['pres'][2]])),
                     c['pres'][i], f"<b>{REF[i]} {c['pres'][i]}</b> {q} = sei/conhece de cor, por inteiro.", v, 'EN4')

# dupla de pronomes reflexivo + OD (nível 6)
for verb, objs in DOBJ.items():
    v = VID.get(verb)
    if not v:
        continue
    c = cj(verb, CLS.get(verb, ''))
    for s, i in DOUBLE_S:
        for np, od in objs:
            B.inp(6, 'Substituir', 'Troque o objeto destacado pelo pronome.', f"{s} {REF[i]} {c['pret'][i]} [[{np}]].", [f"{s} {REF[i]} {od} {c['pret'][i]}."] + ([f"{cap(REF[i])} {od} {c['pret'][i]}."] if s in ('Yo', 'Tú', 'Nosotros') else []),
                  f"Reflexivo/ênfase + OD: ordem fixa <b>{REF[i]} {od}</b> (o pronome reflexivo vem primeiro).", v, 'D1')
    for np, od in objs:
        f2 = attach(c['tu'], ['te', od])
        B.inp(6, 'Substituir', 'Imperativo: troque o objeto destacado pelo pronome.', f"{cap(attach(c['tu'], 'te'))} [[{np}]].", [cap(f2) + '.'],
              f"Dois pronomes colados ao imperativo (te + {od}) → <b>{cap(f2)}</b>, com acento.", v, 'D2')
        B.inp(6, 'Substituir', 'Troque o objeto destacado pelo pronome.', f"No te {c['subj'][1]} [[{np}]].", [f"No te {od} {c['subj'][1]}."],
              f"Negativo: os dois pronomes vão antes, nesta ordem → <b>No te {od} {c['subj'][1]}</b>.", v, 'D3')
        i = R.choice([0, 1, 3])
        s = {0: 'Yo', 1: 'Tú', 3: 'Nosotros'}[i]
        B.inp(6, 'Substituir', 'Troque o objeto destacado pelo pronome (qualquer posição correta).', f"{s} {ESTAR[i]} {attach(c['ger'], REF[i])} [[{np}]].",
              [f"{s} {REF[i]} {od} {ESTAR[i]} {c['ger']}.", f"{s} {ESTAR[i]} {attach(c['ger'], [REF[i], od])}."],
              f"<i>{REF[i]} {od} {ESTAR[i]} {c['ger']}</i> ou <i>{ESTAR[i]} <b>{attach(c['ger'], [REF[i], od])}</b></i> — os pronomes andam juntos.", v, 'D4')

# ============================================================== TIPO GUSTAR
EXP = [("A mí", "me"), ("A ti", "te"), ("A Juan", "le"), ("A mi madre", "le"), ("A usted", "le"), ("A nosotros", "nos"), ("A vosotros", "os"),
       ("A mis padres", "les"), ("A ustedes", "les"), ("A los niños", "les"), ("A ella", "le"), ("A ellos", "les")]
EXP12 = [("A mí", "me"), ("A ti", "te"), ("A nosotros", "nos"), ("A vosotros", "os")]
ADJ_PL = {'loco': 'locos', 'feliz': 'felices', 'harto': 'hartos', 'nervioso': 'nerviosos', 'triste': 'tristes', 'contento': 'contentos'}
LABEL_ADJ = {'parecer', 'resultar (fácil/difícil)', 'quedar grande / pequeño', 'quedar lejos / cerca'}
PT_TIME = ['ayer', 'el año pasado', 'aquella vez', 'en el viaje']


def gextra(e, pr=None):
    ex = e['extra']
    if ex in ('bien', 'mal') and ' / ' in e['name']:
        ex = R.choice(['bien', 'mal'])
    if e['name'] == 'poner triste / contento':
        ex = R.choice(['triste', 'contento'])
    if 'adj' in e['flags'] and pr in ('nos', 'os'):
        ex = ADJ_PL.get(ex, ex)
    return ex


def gparts(e, exp, pr, verb, extra, thing):
    parts = ([exp] if exp else []) + (['se', pr] if 'se' in e['flags'].split() else [pr]) + [verb] + ([extra] if extra else []) + [thing]
    return parts


def gs(parts):
    return cap(' '.join(parts)) + '.'


def label(e, thing):
    return ' '.join(thing.split(' ')[1:]) if e['name'] in LABEL_ADJ else thing


def is_inf(thing):
    w = thing.split(' ')[0]
    return w.endswith(('ar', 'er', 'ir')) and w not in ('el', 'la') and len(w) > 3


for e in GUSTAR:
    if e.get('custom'):
        continue
    c = cj(e['head'], e['cls'])
    v = e['id']
    nm = e['name']
    tier = e['tier']
    lvb = {1: 1, 2: 2, 3: 3}[tier]
    fl = e['flags'].split()
    exps = EXP12 if 'tr' in fl else EXP
    things = [(t, 'S') for t in e['S']] + [(t, 'P') for t in e['P']]
    se = 'se' in fl
    for exp, pr in exps:
        for thing, num in things:
            form = c['pres'][2] if num == 'S' else c['pres'][5]
            ex = gextra(e, pr)
            lab = label(e, thing)
            infnote = ' Infinitivo como sujeito = singular.' if num == 'S' and is_inf(lab) else ''
            # GB concordância presente
            P = gparts(e, exp, pr, '___', ex, thing)
            B.mc(lvb, 'Concordância', f'Complete com <i>{e["head"]}</i> no presente.', gs(P), [c['pres'][2], c['pres'][5]], form,
                 f"O verbo concorda com a coisa, ‘{lab}’ ({'singular' if num == 'S' else 'plural'}) → <b>{form}</b>. A pessoa ({pr}) não manda no verbo.{infnote}", v, 'GB', shuffle=False)
            # GA escolher pronome
            if 'safe' in fl:
                P = gparts(e, exp, '___', form, ex, thing)
                B.mc(lvb, 'Completar', 'Complete com o pronome.', gs(P), ['me', 'te', 'le', 'nos', 'os', 'les'], pr,
                     f"‘{exp}’ → <b>{pr}</b>. Em <i>{nm}</i> a pessoa é objeto indireto, e o pronome é obrigatório mesmo com ‘{low(exp)}’." + (' A ordem é sempre <b>se</b> + pronome.' if se else ''), v, 'GA', shuffle=False)
            # GC pretérito
            tf = c['pret'][2] if num == 'S' else c['pret'][5]
            P = gparts(e, exp, pr, '___', ex, thing + ' ' + R.choice(PT_TIME))
            B.mc(min(3, lvb + 1), 'Concordância', f'Complete com <i>{e["head"]}</i> no pretérito indefinido.', gs(P),
                 [tf, c['pret'][5] if num == 'S' else c['pret'][2], c['pres'][2] if num == 'S' else c['pres'][5], c['pret'][0]], tf,
                 f"Pretérito concordando com ‘{lab}’ → <b>{tf}</b>. <i>{c['pret'][0]}</i> seria ‘eu …’ — concordar com a pessoa é o erro típico.", v, 'GC')
    # GE erros
    for exp, pr in exps:
        thing, num = R.choice(things)
        form = c['pres'][2] if num == 'S' else c['pres'][5]
        other = c['pres'][5] if num == 'S' else c['pres'][2]
        ex = gextra(e, pr)
        good = gparts(e, exp, pr, form, ex, thing)
        kinds = ['agr', 'miss', 'ok'] + (['pron'] if 'safe' in fl else []) + (['yo'] if exp in ('A mí', 'A ti') else [])
        kind = R.choice(kinds)
        ipr = len(exp.split(' ')) + (1 if se else 0)
        iv = ipr + 1
        lv = 2 if tier == 1 else 3
        if kind == 'agr':
            bad = gparts(e, exp, pr, other, ex, thing)
            B.err(lv, gs(bad), [iv], gs(good), f"O verbo concorda com ‘{label(e, thing)}’, não com a pessoa → <b>{form}</b>.", v, 'GE')
        elif kind == 'miss' and not se:
            bad = [exp, form] + ([ex] if ex else []) + [thing]
            B.err(lv, gs(bad), [len(exp.split(' '))], gs(good), f"Falta o pronome: com <i>{nm}</i> ele é obrigatório, mesmo com ‘{low(exp)}’ → <b>{pr} {form}</b>.", v, 'GE')
        elif kind == 'pron':
            wr = {'me': 'te', 'te': 'me', 'le': 'les', 'les': 'le', 'nos': 'os', 'os': 'nos'}[pr]
            bad = gparts(e, exp, wr, form, ex, thing)
            B.err(lv, gs(bad), [ipr], gs(good), f"‘{exp}’ pede <b>{pr}</b>, não <i>{wr}</i>.", v, 'GE')
        elif kind == 'yo':
            subj = 'Yo' if exp == 'A mí' else 'Tú'
            bad = [subj] + gparts(e, None, pr, form, ex, thing)
            B.err(lv, gs(bad), [0], gs(good), f"Com <i>{nm}</i> a pessoa não é sujeito: não se diz ‘{subj.lower()} {pr} {form}’, e sim <b>{exp.lower()} {pr} {form}</b> (ou só ‘{pr} {form}’).", v, 'GE')
        else:
            B.err(lv, gs(good), -1, gs(good), f"Correto: {pr} (a pessoa) + {form} (concorda com ‘{label(e, thing)}’).", v, 'GE')
    # GF transformar pessoa
    for thing, num in things:
        form = c['pres'][2] if num == 'S' else c['pres'][5]
        ex1 = gextra(e, 'me')
        exn = ADJ_PL.get(ex1, ex1) if 'adj' in fl else ex1
        src = gs(gparts(e, None, 'me', form, ex1, thing))
        dst = gs(gparts(e, None, 'nos', form, exn, thing))
        alt = 'A nosotros ' + dst[0].lower() + dst[1:]
        B.inp(1 if tier == 1 else 2, 'Transformar', 'Reescreva a frase para <b>nosotros</b> (troque só a pessoa).', src, [dst, alt],
              f"Troca só o pronome (me → <b>nos</b>); o verbo continua <b>{form}</b>, porque concorda com a coisa. Esse é o teste rápido do tipo gustar." + (' O adjetivo concorda com a pessoa.' if 'adj' in fl else ''), v, 'GF')
    # GD significado
    others = distractors(e, [o for o in GUSTAR if o['cat'] == e['cat']])
    if len(others) < 3:
        others += [d for d in distractors(e, GUSTAR, 8) if d not in others][:3 - len(others)]
    if len(others) >= 3:
        exs = sent(e['ex'])
        B.mc(2 if tier < 3 else 3, 'Vocabulário', f"Na frase, <b>{nm.split(' (')[0]}</b> significa:", exs, [e['pt']] + others[:3], e['pt'],
             f"<b>{nm}</b> = {e['pt']}." + (f" ({e['note']})" if e['note'] else '') + f" Estrutura tipo gustar: <i>{e['ex']}</i>.", v, 'GD')

# GG transitivos: OD + concordância do adjetivo (nível 6)
TR3 = [("A Ana", 'la', 'fs'), ("A mis hermanas", 'las', 'fp'), ("A Juan", 'lo', 'ms'), ("A mis padres", 'los', 'mp')]
FEM = {'loco': ('loca', 'locas'), 'harto': ('harta', 'hartas'), 'nervioso': ('nerviosa', 'nerviosas'), 'contento': ('contenta', 'contentas'), 'feliz': ('feliz', 'felices'), 'triste': ('triste', 'tristes')}
for e in GUSTAR:
    fl = e['flags'].split()
    if 'tr' not in fl or e['name'] in ('afectar', 'tener sin cuidado'):
        continue
    c = cj(e['head'], e['cls'])
    for exp, od, gnr in TR3:
        if 'adj' not in fl and gnr.startswith('m'):
            continue
        thing = R.choice(e['S'])
        vb = c['pres'][2]
        ex = e['extra']
        if ex == 'triste / contento':
            ex = 'triste'
        adjr = ex
        if 'adj' in fl:
            base = ex
            adjr = {'fs': FEM[base][0], 'fp': FEM[base][1], 'ms': base, 'mp': ADJ_PL[base]}[gnr]
        good = ' '.join([exp, od, vb] + ([adjr] if adjr else []) + [thing]) + '.'
        lele = {'la': 'le', 'las': 'les', 'lo': 'le', 'los': 'les'}[od]
        opts = [good, ' '.join([exp, lele, vb] + ([adjr] if adjr else []) + [thing]) + '.']
        if 'adj' in fl:
            opts.append(' '.join([exp, od, vb, ex, thing]) + '.' if adjr != ex else ' '.join([exp, od, vb, ADJ_PL[ex], thing]) + '.')
            opts.append(' '.join([exp, lele, vb, ex, thing]) + '.')
        x = (f"<i>{e['name']}</i> é transitivo: a pessoa é <b>objeto direto</b> → {od}" + (f", e o adjetivo concorda com ela (<b>{adjr}</b>)." if 'adj' in fl else '.') +
             (" Com homem no singular, <i>le</i> é leísmo admitido; com mulher ou no plural, a norma pede lo/la/los/las." if True else ''))
        B.mc(6, 'Norma', 'Qual é a forma recomendada pela norma?', '', opts, good, x, e['id'], 'GG')

# GH construções com se (ordem, pronome)
for e in GUSTAR:
    if 'se' not in e['flags'].split():
        continue
    c = cj(e['head'], e['cls'])
    for exp, pr in EXP:
        thing, num = R.choice([(t, 'S') for t in e['S']] + [(t, 'P') for t in e['P']])
        vb = c['pret'][2] if num == 'S' else c['pret'][5]
        ex = gextra(e, pr)
        good = ' '.join([exp, 'se', pr, vb] + ([ex] if ex else []) + [thing]) + '.'
        bad = ' '.join([exp, pr, 'se', vb] + ([ex] if ex else []) + [thing]) + '.'
        n = len(exp.split(' '))
        if R.random() < .7:
            B.err(5, bad, [n, n + 1], good, f"Ordem fixa: <b>se</b> vem sempre antes do pronome da pessoa → <b>se {pr}</b>. ‘{pr} se’ é comum na fala popular, mas está errado.", e['id'], 'GH')
        else:
            B.err(5, good, -1, good, f"Correto: <b>se {pr}</b> + verbo concordando com ‘{thing}’.", e['id'], 'GH')

# ============================================================== DUPLAS: me aburre × me aburro (nível 5)
GB_BY = {e['name']: e for e in GUSTAR}
for e in PRON:
    d = e.get('dual')
    if not d or d not in GB_BY:
        continue
    gE = GB_BY[d]
    cp = cj(e['verb'], e['cls'])
    cg = cj(gE['head'], gE['cls'])
    for t in pres_tails(e)[:2]:
        B.mc(5, 'Gustar × pronominal', 'Escolha a forma correta.', f"Yo ___ {t}.", [f"me {cp['pres'][0]}", f"me {cg['pres'][2]}"], f"me {cp['pres'][0]}",
             f"Aqui o sujeito é <b>yo</b> (eu fico …): verbo pronominal <i>{e['verb']}se</i> → <b>me {cp['pres'][0]}</b>. Com a coisa como sujeito seria <i>me {cg['pres'][2]} + coisa</i>.", [e['id'], gE['id']], 'DU', shuffle=False)
    for thing, num in [(gE['S'][0], 'S'), (gE['P'][0], 'P')]:
        f = cg['pres'][2] if num == 'S' else cg['pres'][5]
        B.mc(5, 'Gustar × pronominal', 'Escolha a forma correta.', f"___ {thing}.", [f"Me {f}", f"Me {cp['pres'][0]}"], f"Me {f}",
             f"Aqui quem faz o efeito é ‘{thing}’ (sujeito): tipo gustar → <b>me {f}</b>. <i>Me {cp['pres'][0]}</i> pediria ‘eu’ como sujeito: me {cp['pres'][0]} con/de …", [e['id'], gE['id']], 'DU', shuffle=False)

# ============================================================== IDENTIFICAR (teste rápido)
OPT_G, OPT_P = 'Tipo gustar (concorda com a coisa)', 'Pronominal (concorda com a pessoa)'
for e in ALL:
    ex = e['ex']
    if not ex.startswith('me ') or e.get('custom') or 'sensitive' in e['flags']:
        continue
    if e['kind'] == 'gustar':
        tu = 'te ' + ex[3:]
        x = f"Troque para tú: <i>{tu}</i> — só o pronome muda, o verbo fica igual → <b>tipo gustar</b>."
        ans = OPT_G
    else:
        c = cj(e['verb'], e['cls'])
        w = ex.split(' ')
        if len(w) < 2:
            continue
        f = w[1]
        if f == c['pres'][0]:
            tf = c['pres'][1]
        elif f == c['pret'][0]:
            tf = c['pret'][1]
        else:
            continue
        tu = 'te ' + tf + ' ' + ' '.join(w[2:])
        x = f"Troque para tú: <i>{tu.strip()}</i> — o verbo também muda ({f} → {tf}) → <b>pronominal</b>."
        ans = OPT_P
    lv = 1 if e['tier'] == 1 else (5 if e.get('grp') in ('emo', 'sen') or e['cat'].startswith('Emo') else 2)
    B.mc(lv, 'Identificar', 'Que tipo de verbo é este?', sent(ex), [OPT_G, OPT_P], ans, x, e['id'], 'ID', shuffle=False)

# ============================================================== HAND (curados)
H = []


def hm(lv, k, q, s, opts, x, v, shuffle=True):
    H.append(('mc', lv, k, q, s, opts, x, v, shuffle))


def hma(lv, k, q, s, opts, ans, x, v, shuffle=True):
    H.append(('mc_ans', ans, 'mc', lv, k, q, s, opts, x, v, shuffle))


def he(lv, sentence, bad, fix, x, v):
    H.append(('err', lv, sentence, bad, fix, x, v))


def hi(lv, k, q, s, answers, x, v):
    H.append(('in', lv, k, q, s, answers, x, v))


PAIRS = [
    ("—¡La cena está lista! —¡Ya ___!", ["voy", "me voy"], "<b>Ya voy</b> = já estou indo (até você). <i>Ya me voy</i> seria ‘já vou embora’.", 'p:irse'),
    ("Esta fiesta es aburrida; yo ___.", ["me voy", "voy"], "Sem destino, com a ideia de sair/partir → <b>irse</b>: me voy (vou embora).", 'p:irse'),
    ("El negocio ___ muy bien este año.", ["marcha", "se marcha"], "<b>marchar</b> = andar, funcionar (o negócio vai bem). <i>Marcharse</i> = ir embora.", 'p:marcharse'),
    ("Pedro ___ sin avisar a nadie.", ["se marchó", "marchó"], "<b>marcharse</b> = ir embora.", 'p:marcharse'),
    ("Anoche ___ ocho horas seguidas.", ["dormí", "me dormí"], "<b>dormir</b> = dormir (duração). <i>Dormirse</i> = pegar no sono (o momento).", 'p:dormirse'),
    ("La película era tan aburrida que ___ en el cine.", ["me dormí", "dormí"], "<b>dormirse</b> = pegar no sono.", 'p:dormirse'),
    ("¿Cuántas horas ___ normalmente? (tú)", ["duermes", "te duermes"], "Pergunta sobre a duração do sono → <b>dormir</b>.", 'p:dormirse'),
    ("___ con Ana a las ocho en la plaza. (yo, pretérito)", ["Quedé", "Me quedé"], "<b>quedar con alguien</b> = combinar/marcar encontro.", 'p:quedarse'),
    ("Llovía mucho, así que ___ en casa.", ["me quedé", "quedé"], "<b>quedarse</b> = ficar (permanecer).", 'p:quedarse'),
    ("Los dos países ___ un alto el fuego.", ["acordaron", "se acordaron"], "<b>acordar algo</b> = combinar, acordar.", 'p:acordarse'),
    ("No ___ de su nombre.", ["me acuerdo", "acuerdo"], "<b>acordarse de</b> = lembrar.", 'p:acordarse'),
    ("Siempre ___ paraguas en la mochila.", ["llevo", "me llevo"], "<b>llevar</b> = levar (consigo).", 'p:llevarse'),
    ("Mis hermanos y yo ___ muy bien.", ["nos llevamos", "llevamos"], "<b>llevarse bien/mal</b> = dar-se bem/mal.", 'p:llevarse'),
    ("Los ladrones ___ todas las joyas. (levaram embora)", ["se llevaron", "llevaron"], "<b>llevarse algo</b> = levar embora.", 'p:llevarse'),
    ("Ese chico ___ cansado.", ["parece", "se parece"], "<b>parecer</b> + adjetivo = parecer (aparência).", 'p:parecerse'),
    ("Ana ___ mucho a su madre.", ["se parece", "parece"], "<b>parecerse a</b> = parecer-se com (semelhança).", 'p:parecerse'),
    ("El ministro ___ las acusaciones.", ["negó", "se negó"], "<b>negar algo</b> = negar.", 'p:negarse'),
    ("El testigo ___ a declarar.", ["se negó", "negó"], "<b>negarse a</b> = recusar-se.", 'p:negarse'),
    ("La empresa ___ a diez empleados.", ["despidió", "se despidió"], "<b>despedir a alguien</b> = demitir.", 'p:despedirse'),
    ("Antes de salir, ___ de todos.", ["se despidió", "despidió"], "<b>despedirse de</b> = despedir-se.", 'p:despedirse'),
    ("Mi padre ___ del trabajo a las seis.", ["vuelve", "se vuelve"], "<b>volver</b> = voltar.", 'p:volverse'),
    ("Con la fama, ___ muy arrogante.", ["se volvió", "volvió"], "<b>volverse</b> + adjetivo = tornar-se (mudança de caráter).", 'p:volverse'),
    ("Mi abuela ___ un pastel delicioso.", ["hizo", "se hizo"], "<b>hacer</b> = fazer.", 'p:hacerse'),
    ("Trabajó mucho y ___ rico.", ["se hizo", "hizo"], "<b>hacerse</b> = tornar-se (com esforço/processo).", 'p:hacerse'),
    ("No ___ el tonto: sé que lo sabes. (tú)", ["te hagas", "hagas"], "<b>hacerse el tonto</b> = fingir-se de bobo.", 'p:hacerse'),
    ("___ las llaves en la mesa. (yo, pretérito)", ["Puse", "Me puse"], "<b>poner</b> = colocar.", 'p:ponerse'),
    ("Hacía frío, así que ___ la chaqueta.", ["me puse", "puse"], "<b>ponerse</b> (roupa) = vestir.", 'p:ponerse'),
    ("Cuando oyó la noticia, ___ muy triste.", ["se puso", "puso"], "<b>ponerse</b> + estado = ficar.", 'p:ponerse'),
    ("Por fin ___ mis gafas. (yo, pretérito)", ["encontré", "me encontré"], "<b>encontrar</b> = achar.", 'p:encontrarse'),
    ("Hoy no ___ bien; me voy a casa.", ["me encuentro", "encuentro"], "<b>encontrarse</b> + bien/mal = sentir-se.", 'p:encontrarse'),
    ("Ayer ___ con Pedro en el súper.", ["me encontré", "encontré"], "<b>encontrarse con alguien</b> = encontrar alguém (por acaso).", 'p:encontrarse'),
    ("Vamos a ___ la fecha de la boda.", ["fijar", "fijarnos"], "<b>fijar</b> = fixar, marcar.", 'p:fijarse'),
    ("¿___ en el sombrero que llevaba? (tú, pretérito)", ["Te fijaste", "Fijaste"], "<b>fijarse en</b> = reparar.", 'p:fijarse'),
    ("___ la paella, está buenísima. (tú, imperativo)", ["Prueba", "Pruébate"], "<b>probar</b> comida = provar.", 'p:probarse'),
    ("___ el vestido antes de comprarlo. (yo, pretérito)", ["Me probé", "Probé"], "<b>probarse</b> roupa = provar (vestindo).", 'p:probarse'),
    ("___ la ropa en la maleta. (yo, pretérito)", ["Metí", "Me metí"], "<b>meter</b> = colocar dentro.", 'p:meterse'),
    ("No ___ en mi vida. (tú)", ["te metas", "metas"], "<b>meterse en</b> = intrometer-se.", 'p:meterse'),
    ("___ a mi madre todos los domingos.", ["Llamo", "Me llamo"], "<b>llamar a alguien</b> = ligar/chamar.", 'p:llamarse'),
    ("Hola, ___ Diego.", ["me llamo", "llamo"], "<b>llamarse</b> = chamar-se.", 'p:llamarse'),
    ("Este sofá ___ demasiado espacio.", ["ocupa", "se ocupa"], "<b>ocupar</b> = ocupar.", 'p:ocuparse'),
    ("Tranquilo, yo ___ de la cena.", ["me ocupo", "ocupo"], "<b>ocuparse de</b> = cuidar de.", 'p:ocuparse'),
    ("Por ingenuo, ___ en la trampa.", ["caí", "me caí"], "<b>caer</b> em sentido figurado (cair na armadilha) → sem pronome.", 'p:caerse'),
    ("Tropecé con una piedra y ___ en la calle.", ["me caí", "caí"], "Levar um tombo → <b>caerse</b>: me caí.", 'p:caerse'),
    ("___ de casa a las ocho todos los días.", ["Salgo", "Me salgo"], "<b>salir</b> = sair.", 'p:salirse'),
    ("El agua ___ de la bañera.", ["se salió", "salió"], "<b>salirse</b> = vazar, transbordar.", 'p:salirse'),
    ("Cervantes ___ en 1616.", ["murió", "se murió"], "Em registro formal/histórico: <b>morir</b>. <i>Morirse</i> é coloquial ou enfático.", 'p:morirse'),
    ("¡Qué hambre! ___ de hambre.", ["Me muero", "Muero"], "Exagero coloquial → <b>morirse de</b> hambre, risa, ganas…", 'p:morirse'),
    ("Este cambio ___ muchos riesgos.", ["comporta", "se comporta"], "<b>comportar</b> = implicar.", 'p:comportarse'),
    ("El niño ___ muy bien en la boda.", ["se comportó", "comportó"], "<b>comportarse</b> = comportar-se.", 'p:comportarse'),
    ("Los soldados ___ armas.", ["portaban", "se portaban"], "<b>portar</b> = portar, carregar.", 'p:portarse'),
    ("¡___ bien en casa de la abuela! (tú)", ["Pórtate", "Porta"], "<b>portarse</b> = comportar-se.", 'p:portarse'),
    ("___ el buen tiempo para ir a la playa. (nosotros, pretérito)", ["Aprovechamos", "Nos aprovechamos"], "<b>aprovechar algo</b> = aproveitar.", 'p:aprovecharse'),
    ("El vendedor ___ de mi ignorancia.", ["se aprovechó", "aprovechó"], "<b>aprovecharse de</b> = aproveitar-se (abusar).", 'p:aprovecharse'),
    ("___ de llamarte. (yo, pretérito)", ["Me olvidé", "Olvidé"], "Com <i>de</i> → <b>olvidarse de</b>. <i>Olvidé de llamarte</i> mistura as duas construções.", 'p:olvidarse'),
    ("El accidente ___ a las tres.", ["ocurrió", "se ocurrió"], "<b>ocurrir</b> = acontecer.", 'g:ocurrir (ideia)'),
    ("___ una idea genial. (a mí)", ["Se me ocurrió", "Me ocurrió"], "<b>ocurrírsele algo a alguien</b> = ter uma ideia: se me ocurrió.", 'g:ocurrir (ideia)'),
    ("Le ___ un regalo a mi madre. (yo, pretérito)", ["di", "me di"], "<b>dar</b> = dar.", 'p:darse'),
    ("No ___ por vencido. (tú)", ["te des", "des"], "<b>darse por vencido</b> = desistir.", 'p:darse'),
    ("___ la carta al buzón. (yo, pretérito)", ["Eché", "Me eché"], "<b>echar</b> = jogar, pôr.", 'p:echarse'),
    ("Cuando lo vio, ___ a llorar.", ["se echó", "echó"], "<b>echarse a</b> + infinitivo = começar a (de repente).", 'p:echarse'),
    ("___ la basura antes de salir. (yo, pretérito)", ["Tiré", "Me tiré"], "<b>tirar</b> = jogar (fora).", 'p:tirarse'),
    ("Mi hijo ___ a la piscina de cabeza.", ["se tiró", "tiró"], "<b>tirarse</b> = atirar-se.", 'p:tirarse'),
    ("El profesor ___ una pregunta difícil.", ["planteó", "se planteó"], "<b>plantear</b> = propor, levantar (uma questão).", 'p:plantearse'),
    ("___ cambiar de trabajo. (yo, presente)", ["Me planteo", "Planteo"], "<b>plantearse</b> = considerar.", 'p:plantearse'),
    ("___ las vacaciones en la playa. (nosotros, pretérito)", ["Pasamos", "Nos pasamos"], "<b>pasar</b> (tempo) = passar.", 'p:pasarse'),
    ("Con ese comentario ___. (tú, pretérito)", ["te pasaste", "pasaste"], "<b>pasarse</b> = exagerar, passar do ponto.", 'p:pasarse'),
    ("___ el autobús por dos minutos. (yo, pretérito)", ["Perdí", "Me perdí"], "<b>perder</b> = perder (algo).", 'p:perderse'),
    ("Sin mapa, ___ en la ciudad. (nosotros)", ["nos perdimos", "perdimos"], "<b>perderse</b> = perder-se.", 'p:perderse'),
    ("El jurado ___ el ganador.", ["decidió", "se decidió"], "<b>decidir algo</b> = decidir.", 'p:decidirse'),
    ("Después de mucho dudar, por fin ___. (yo)", ["me decidí", "decidí"], "<b>decidirse</b> = decidir-se (depois de hesitar).", 'p:decidirse'),
    ("No ___ en fantasmas. (yo)", ["creo", "me creo"], "<b>creer en</b> = acreditar.", 'p:creerse'),
    ("___ muy listo, pero no lo es. (él)", ["Se cree", "Cree"], "<b>creerse</b> = achar-se.", 'p:creerse'),
    ("La serpiente ___ la piel.", ["muda", "se muda"], "<b>mudar</b> (pele, pena) = trocar.", 'p:mudarse'),
    ("___ a Madrid el mes pasado. (nosotros)", ["Nos mudamos", "Mudamos"], "<b>mudarse</b> = mudar de casa.", 'p:mudarse'),
    ("Mi padre ___ un camión.", ["conduce", "se conduce"], "<b>conducir</b> = dirigir.", 'p:conducirse'),
    ("En la reunión, ___ con mucho respeto. (él)", ["se condujo", "condujo"], "<b>conducirse</b> = comportar-se (formal).", 'p:conducirse'),
    ("Al llegar al hotel, ___ la maleta. (yo)", ["deshice", "me deshice"], "<b>deshacer</b> = desfazer.", 'p:deshacerse'),
    ("Por fin ___ de los muebles viejos. (yo)", ["me deshice", "deshice"], "<b>deshacerse de</b> = livrar-se.", 'p:deshacerse'),
    ("El médico ___ a sus pacientes con cariño.", ["trata", "se trata"], "<b>tratar</b> = tratar.", 'p:tratarse de'),
    ("No es grave: ___ de un simple error.", ["se trata", "trata"], "<b>se trata de</b> = trata-se de (impessoal, sem sujeito).", 'p:tratarse de'),
    ("Esta novela ___ de la guerra civil.", ["trata", "se trata"], "Com sujeito (esta novela) → <b>tratar de</b>. <i>Tratarse de</i> não leva sujeito.", 'p:tratarse de'),
    ("El periodista ___ el nombre de su fuente.", ["calló", "se calló"], "<b>callar algo</b> = calar, ocultar.", 'p:callarse'),
    ("¡___ un momento, por favor! (tú)", ["Cállate", "Cállalo"], "<b>callarse</b> = calar-se (parar de falar).", 'p:callarse'),
    ("Siempre ___ al bebé en la sillita. (yo)", ["siento", "me siento"], "<b>sentar a alguien</b> = sentar alguém.", 'p:sentarse'),
    ("___ aquí, por favor. (tú)", ["Siéntate", "Sienta"], "<b>sentarse</b> = sentar-se.", 'p:sentarse'),
    ("Primero ___ las manos y luego lavo los platos. (yo)", ["me lavo", "lavo"], "A ação recai sobre a própria pessoa (as próprias mãos) → <b>lavarse</b>. Com outro objeto (los platos), sem pronome.", 'p:lavarse'),
    ("Todas las mañanas ___ a mi hijo a las siete. (yo)", ["despierto", "me despierto"], "Despertar <b>outra pessoa</b> → sem pronome.", 'p:despertarse'),
]
for s, opts, x, v in PAIRS:
    hm(5, 'Mudam de sentido', 'Escolha a forma correta (com ou sem pronome).', s, opts, x, v)

CASES = [
    (5, "Tropecé con una piedra y ___ en la calle.", ["me caí", "caí", "se me cayó", "me cayó"], "Levei um tombo → <b>me caí</b> (caerse).", 'p:caerse'),
    (5, "Estaba hablando por teléfono y ___ el celular.", ["se me cayó", "me caí", "caí", "me cayó"], "Algo caiu da minha mão sem querer → <b>se me cayó</b> (se + pessoa afetada + verbo concordando com a coisa).", ['p:caerse', 'g:olvidar (involuntário)']),
    (5, "Lo detuvieron y ___ preso.", ["cayó", "se cayó", "se le cayó"], "<b>caer preso</b> (ser preso) é sentido figurado → sem pronome.", 'p:caerse'),
    (5, "De repente ___ en la cuenta: era su cumpleaños. (yo)", ["caí", "me caí", "se me cayó"], "<b>caer en la cuenta</b> = dar-se conta, sentido figurado → sem pronome.", 'p:caerse'),
    (5, "¡Cuidado! Casi ___. (yo)", ["me caigo", "caigo", "se me cae"], "<b>Casi me caigo</b> = quase levei um tombo (presente com valor de passado próximo).", 'p:caerse'),
    (5, "—¿Quién se cayó, tu hermano? —No, ___ yo.", ["me caí", "caí", "se cayó"], "O sujeito é <i>yo</i> → <b>me caí</b>; o <i>yo</i> só dá ênfase em quem caiu.", 'p:caerse'),
    (5, "A Juan ___ las gafas al agua.", ["se le cayeron", "se le cayó", "le se cayeron", "se cayeron"], "<b>se le cayeron</b>: se + le (Juan, afetado) + verbo no plural (las gafas).", ['p:caerse']),
    (5, "Mi hermano ___ de la bici y se rompió el brazo.", ["se cayó", "cayó", "se le cayó"], "Tombo → <b>se cayó</b>.", 'p:caerse'),
    (5, "La semana pasada ___ enfermo y no fui a trabajar. (registro narrativo)", ["caí", "me caí", "se me cayó"], "<b>caer enfermo</b> é expressão fixa, sempre sem pronome.", ['p:caerse', 'p:enfermarse']),
]
for lv, s, opts, x, v in CASES:
    hm(lv, 'Casos com caer', 'Escolha a forma correta.', s, opts, x, v)
hm(5, 'Casos com caer', 'Para dizer “fiquei doente na semana passada”, qual opção <b>não</b> soa natural?', '',
   ["Me caí enfermo la semana pasada.", "Caí enfermo la semana pasada.", "Me enfermé la semana pasada.", "Me puse enfermo la semana pasada."],
   "<i>Me caí enfermo</i> soa errado: o <i>me</i> traz de volta a ideia de tombo. <b>Me enfermé</b> (comum na América Latina), <b>me puse enfermo</b> (comum na Espanha) e <b>caí enfermo</b> (mais formal/narrativo) estão certos.", ['p:caerse', 'p:enfermarse', 'p:ponerse'])
hm(5, 'Casos com caer', 'Qual forma é a mais natural no dia a dia da América Latina para “fiquei doente”?', '',
   ["Me enfermé.", "Caí enfermo.", "Me caí enfermo.", "Enfermé."], "<b>Me enfermé</b> (enfermarse) é o mais natural na América Latina; na Espanha diz-se mais <i>me puse enfermo</i>.", 'p:enfermarse')
he(5, "Ayer me calió en la calle.", [2], "Ayer me caí en la calle.", "<i>Calió</i> não existe. Para ‘eu caí’: <b>me caí</b> (caerse: me caí, te caíste, se cayó).", 'p:caerse')
he(5, "Cuando entró el jefe, me calió.", [5], "Cuando entró el jefe, me callé.", "<i>Calió</i> não existe. Para ‘eu me calei’: <b>me callé</b> (callarse).", 'p:callarse')
hm(5, 'Casos com caer', '“Me calió” é:', '', ["Uma forma que não existe: o certo é ‘me caí’ ou ‘me callé’", "O pretérito de caerse", "O pretérito de callarse", "Uma variante coloquial aceita"],
   "Não existe. Provavelmente a ideia era <b>me caí</b> (caerse) ou <b>me callé</b> (callarse).", ['p:caerse', 'p:callarse'])

# olvidar / acordar
hm(5, 'Olvidar e acordarse', 'Qual destas frases <b>não</b> está correta?', '', ["Olvidé de cerrar la puerta.", "Olvidé cerrar la puerta.", "Me olvidé de cerrar la puerta.", "Se me olvidó cerrar la puerta."],
   "Três construções corretas: <i>olvidar algo</i>, <i>olvidarse de algo</i> e <i>olvidársele algo a alguien</i>. <b>Olvidé de</b> mistura as duas primeiras.", ['p:olvidarse', 'g:olvidar (involuntário)'])
he(5, "Olvidé de traer el libro.", [1], "Olvidé traer el libro.", "Sem pronome não há <i>de</i>: <b>olvidé traer</b>. Com pronome, sim: <i>me olvidé de traer</i>.", 'p:olvidarse')
hm(5, 'Olvidar e acordarse', 'Complete (a nós, sem querer).', "___ las entradas en casa.", ["Se nos olvidaron", "Se nos olvidó", "Nos se olvidaron", "Nos olvidamos"],
   "<b>Se nos olvidaron</b>: se + nos + verbo no plural (las entradas).", 'g:olvidar (involuntário)')
he(5, "Recuerdo de aquel día.", [0, 1], "Me acuerdo de aquel día.", "<i>recordar</i> não leva <i>de</i> (<b>recuerdo aquel día</b>); <i>acordarse</i> leva (<b>me acuerdo de aquel día</b>).", 'p:acordarse')
hm(5, 'Olvidar e acordarse', 'Complete.', "¿Te acuerdas ___ mí?", ["de", "a", "— (nada)", "con"], "<b>acordarse de</b> alguém/algo.", 'p:acordarse', False)
hm(5, 'Ênfase', 'Sem o pronome, “Comí toda la pizza”:', '', ["Continua correta, só perde a ideia de ‘comi tudinho’", "Fica errada", "Muda de sentido", "Só é correta na América"],
   "No pronome de ênfase, tirar o <i>me</i> não deixa a frase errada: ela só perde força.", 'p:comerse (ênfase)')

# llamarse
hm(1, 'Completar', 'Complete.', "—¿Cómo ___ llamas? —Me llamo Diego.", ["te", "se", "me", "tú"], "<b>llamarse</b>: tú → <b>te</b> llamas.", 'p:llamarse')
hm(1, 'Completar', 'Complete.', "Mis hermanas ___ llaman Ana y Lucía.", ["se", "nos", "les", "me"], "Ellas → <b>se</b> llaman.", 'p:llamarse')
hm(1, 'Completar', 'Complete.', "¿Cómo ___ llama usted?", ["se", "le", "te", "lo"], "Usted → <b>se</b> llama.", 'p:llamarse')
hm(2, 'Completar', 'Complete.', "Nosotros ___ García.", ["nos llamamos", "llamamos", "se llaman", "nos llaman"], "Nosotros → <b>nos llamamos</b>.", 'p:llamarse')
he(2, "Mi nombre se llama Diego.", [0, 1, 2], "Me llamo Diego.", "Calco do português ‘meu nome é’. Em espanhol: <b>Me llamo Diego</b> ou <i>Mi nombre es Diego</i>.", 'p:llamarse')
he(2, "Yo llamo Diego.", [1], "Yo me llamo Diego.", "Falta o pronome: <b>me llamo</b>.", 'p:llamarse')
he(3, "Ella llama Lucía.", [1], "Ella se llama Lucía.", "Sem <i>se</i>, <i>llama</i> = ela chama (alguém). Para o nome: <b>se llama</b>.", 'p:llamarse')

# tratarse de
he(6, "El libro se trata de la guerra.", [2], "El libro trata de la guerra.", "<i>Tratarse de</i> é impessoal (sem sujeito): <i>Se trata de un error</i>. Com sujeito, use <b>tratar de</b>.", 'p:tratarse de')
hm(6, 'Norma', 'Qual frase está correta?', '', ["Esta película trata de dos hermanos.", "Esta película se trata de dos hermanos.", "Se tratan de dos hermanos esta película.", "Esta película se tratan de dos hermanos."],
   "Com sujeito → <b>trata de</b>. <i>Se trata de</i> só sem sujeito: <i>Se trata de dos hermanos que…</i>", 'p:tratarse de')
hm(6, 'Completar', 'Complete.', "¿De qué ___? (= do que se trata?)", ["se trata", "trata", "se tratan"], "Pergunta impessoal → <b>se trata</b> (sempre singular).", 'p:tratarse de')

# suicidarse — apenas uso narrativo, em 3ª pessoa
hm(3, 'Identificar', 'Na frase literária “En la novela, el personaje se suicida al final”, o verbo é:', '',
   ["Pronominal: só existe com pronome", "Tipo gustar", "Recíproco", "Ênfase"], "<i>suicidarse</i> está na lista dos verbos que só existem com pronome.", 'p:suicidarse')

# ir (¿cómo te va?) / dar ganas / quedar
hm(1, 'Completar', 'Complete.', "¿Cómo ___ va? (tú)", ["te", "se", "le", "vas"], "<b>¿Cómo te va?</b> funciona como gustar: a pessoa vai no pronome.", 'g:ir (¿cómo te va?)')
hm(2, 'Concordância', 'Complete.', "¿Qué tal les ___ a tus padres en Lisboa?", ["va", "van"], "Sem sujeito expresso, fica no singular: <b>¿qué tal les va?</b>", 'g:ir (¿cómo te va?)', False)
hm(2, 'Concordância', 'Complete.', "Me ___ bien en el trabajo.", ["va", "voy", "vas"], "<b>me va bien</b>: a pessoa no pronome, verbo na 3ª pessoa.", ['g:ir (¿cómo te va?)', 'g:ir bien / mal'])
hm(3, 'Concordância', 'Complete.', "A mis hijos les ___ muy bien los estudios.", ["van", "va"], "Com sujeito plural (los estudios) → <b>van</b>.", ['g:ir (¿cómo te va?)', 'g:ir bien / mal'], False)
hm(2, 'Concordância', 'Complete.', "Esta canción me ___ ganas de bailar.", ["da", "dan"], "Sujeito: ‘esta canción’ (singular) → <b>da</b>.", 'g:dar ganas', False)
hm(2, 'Concordância', 'Complete.', "Me ___ ganas de llorar.", ["dan", "da"], "Sem outro sujeito, <i>ganas</i> é o sujeito (plural) → <b>me dan ganas</b>.", 'g:dar ganas', False)
hm(3, 'Concordância', 'Complete.', "Sus chistes me ___ ganas de reír.", ["dan", "da"], "Sujeito: ‘sus chistes’ (plural) → <b>dan</b>.", 'g:dar ganas', False)
for s, opts, x, v in [
    ("¿Cuánto dinero te ___?", ["queda", "quedas", "quedan"], "<b>quedar</b> (restar), tipo gustar: concorda com ‘dinero’ → queda.", 'g:quedar (restar)'),
    ("___ con Ana a las ocho. (yo, presente)", ["Quedo", "Me quedo", "Me queda"], "<b>quedar con alguien</b> = combinar → quedo.", 'p:quedarse'),
    ("Hoy ___ en casa. (yo)", ["me quedo", "quedo", "me queda"], "<b>quedarse</b> = ficar → me quedo.", 'p:quedarse'),
    ("Esa camisa te ___ muy bien.", ["queda", "quedas", "quedan"], "<b>quedar bien</b> (roupa), tipo gustar → te queda.", 'g:quedar bien / mal (roupa)'),
    ("Me ___ dos días de vacaciones.", ["quedan", "queda", "quedo"], "Restar, tipo gustar: concorda com ‘dos días’ → quedan.", 'g:quedar (restar)'),
    ("Al ver el precio, ___ sin palabras. (yo, pretérito)", ["me quedé", "me quedó", "quedé"], "<b>quedarse</b> + estado = ficar (sem palavras).", 'p:quedarse'),
]:
    hm(6, 'Quedar × quedarse', 'Escolha a forma correta.', s, opts, x, v)

# verbos de mudança
for s, opts, x, v in [
    ("Cuando vio al profesor, ___ rojo.", ["se puso", "se volvió", "se hizo", "se quedó"], "Mudança rápida e passageira → <b>ponerse</b>.", 'p:ponerse'),
    ("Después de la guerra, ___ muy desconfiado.", ["se volvió", "se puso", "se hizo", "se quedó"], "Mudança profunda de caráter → <b>volverse</b>.", 'p:volverse'),
    ("Trabajó muchísimo y ___ rico.", ["se hizo", "se puso", "se volvió", "se quedó"], "Mudança por esforço/processo → <b>hacerse</b>.", 'p:hacerse'),
    ("Con el accidente, ___ ciego.", ["se quedó", "se puso", "se hizo", "se volvió"], "Resultado/perda após um fato → <b>quedarse</b>.", 'p:quedarse'),
    ("Estaba ___ muy nerviosa antes del examen.", ["poniéndose", "volviéndose", "haciéndose", "quedándose"], "Estado passageiro → <b>ponerse</b>.", 'p:ponerse'),
    ("Mi abuelo ___ calvo a los treinta.", ["se quedó", "se puso", "se hizo", "se volvió"], "Resultado permanente após um processo físico → <b>quedarse</b> calvo.", 'p:quedarse'),
    ("___ vegetariano el año pasado. (él)", ["Se hizo", "Se puso", "Se quedó", "Se volvió"], "Decisão/ideologia → <b>hacerse</b> (vegetariano, budista, socio…).", 'p:hacerse'),
    ("___ pálido al ver la factura. (él)", ["Se puso", "Se hizo", "Se volvió", "Se quedó"], "Reação física momentânea → <b>ponerse</b>.", 'p:ponerse'),
    ("Con tanto estrés, casi ___ loco. (yo)", ["me vuelvo", "me pongo", "me hago", "me quedo"], "<b>volverse loco</b> é a expressão fixa.", 'p:volverse'),
    ("Al oír la noticia, ___ sin palabras. (nosotros)", ["nos quedamos", "nos pusimos", "nos hicimos", "nos volvimos"], "<b>quedarse sin palabras</b>.", 'p:quedarse'),
    ("___ el tonto para no pagar. (él, presente)", ["Se hace", "Se pone", "Se vuelve", "Se queda"], "<b>hacerse el tonto</b> = fingir.", 'p:hacerse'),
    ("Al oír su nombre, ___ hacia la puerta. (ella)", ["se volvió", "se puso", "se hizo", "se quedó"], "<b>volverse</b> também é virar-se.", 'p:volverse'),
]:
    hm(6, 'Verbos de mudança', 'Escolha o verbo de mudança adequado.', s, opts, x, v)

# pares extremos com sentidos
for s, opts, x, v in [
    ("¿A qué ___ usted? (= qual a sua profissão?)", ["se dedica", "dedica", "le dedica"], "<b>dedicarse a</b> = trabalhar com. Pergunta clássica.", 'p:ocuparse'),
    ("Me ___ a mi padre en la forma de hablar.", ["parezco", "parece", "pareces"], "<b>parecerse a</b>: concorda com a pessoa (yo) → me parezco.", 'p:parecerse'),
    ("¿Qué te ___ la idea?", ["parece", "pareces", "pareció mí"], "<b>parecer</b> (opinião) é tipo gustar: concorda com ‘la idea’ → te parece.", ['g:parecer', 'p:parecerse']),
    ("Mis hijos ___ bien con sus primos.", ["se llevan", "les llevan", "llevan"], "<b>llevarse bien con</b>.", 'p:llevarse'),
    ("Se me ___ bien las matemáticas.", ["dan", "da", "doy"], "<b>dársele bien algo a alguien</b>: concorda com ‘las matemáticas’ → dan.", 'g:darse bien / mal'),
    ("A mi hermano se le ___ fatal cocinar.", ["da", "dan", "doy"], "Infinitivo como sujeito → singular: <b>se le da</b>.", 'g:darse bien / mal'),
    ("Se me ___ un café ahora mismo.", ["antoja", "antojo", "antojan"], "<b>antojársele algo a alguien</b>: concorda com ‘un café’.", 'g:antojarse'),
    ("Me ___ una cerveza bien fría. (Colômbia)", ["provoca", "provoco", "provocan"], "Em partes da Colômbia e do Peru, <b>provocar</b> = dar vontade, tipo gustar.", 'g:provocar'),
    ("Me ___ tu cara: ¿nos conocemos?", ["suena", "sueno", "suenas"], "<b>sonar</b> = parecer familiar, tipo gustar: concorda com ‘tu cara’.", 'g:sonar (familiar)'),
    ("¿Qué te ___? Pareces preocupado.", ["pasa", "pasas", "pasan"], "<b>¿Qué te pasa?</b> = o que você tem?", 'g:pasar'),
    ("En Perú ___ de pie cuando entra el profesor. (ficam de pé)", ["se paran", "paran", "les paran"], "Na América Latina <b>pararse</b> também é ‘ficar de pé’.", 'p:pararse'),
    ("El reloj ___ a las tres.", ["se paró", "paró se", "le paró"], "<b>pararse</b> = parar (sozinho).", 'p:pararse'),
    ("El caballo ___ con el ruido.", ["se espantó", "espantó", "le espantó"], "<b>espantarse</b> = espantar-se.", 'p:espantarse'),
    ("El gato ___ debajo de la cama.", ["se escondió", "escondió", "le escondió"], "<b>esconderse</b> = esconder-se.", 'p:esconderse'),
    ("El vuelo ___ dos horas.", ["se retrasó", "retrasó", "le retrasó"], "<b>retrasarse</b> = atrasar-se.", 'p:retrasarse'),
    ("Se ___ el perro y no lo encontramos.", ["escapó", "escapé", "escaparon"], "<b>escaparse</b>: o sujeito é ‘el perro’.", 'p:escaparse'),
    ("El gato ___ junto a la chimenea.", ["se acurrucó", "acurrucó", "le acurrucó"], "<b>acurrucarse</b> = aconchegar-se.", 'p:acurrucarse'),
    ("El miedo ___ de mí.", ["se apoderó", "apoderó", "me apoderó"], "<b>apoderarse de</b>: aqui o sujeito é ‘el miedo’.", 'p:apoderarse'),
    ("Ni ___ a contestar mi mensaje. (él)", ["se dignó", "dignó", "le dignó"], "<b>dignarse a</b> (frequente com <i>ni</i>): nem se dignou a responder.", 'p:dignarse'),
    ("Me ___ temprano y salí. (Am. Lat. = tomei café da manhã)", ["desayuné", "desayunó", "desayunaste"], "Em partes da América Latina, <b>desayunarse</b> é usado com pronome; em geral basta <i>desayunar</i>.", 'p:desayunarse'),
    ("El barbero ___ la barba al cliente. (Am. Lat.)", ["le rasuró", "se rasuró", "rasuró se"], "Barbear <b>outra pessoa</b> → sem reflexivo (com OI do dono). <i>Rasurarse</i> = barbear-se.", 'p:rasurarse'),
]:
    hm(6, 'Casos-limite', 'Escolha a forma correta.', s, opts, x, v)

# queísmo / dequeísmo
for s, ans, x, v in [
    ("Me alegro ___ que vengas.", "de", "<i>Alegrarse</i> é pronominal: alegrarse <b>de</b> algo → <b>de que</b>. Sem <i>de</i> é queísmo.", 'p:alegrarse'),
    ("Me alegra ___ que vengas.", "— (nada)", "<i>Alegrar</i> é tipo gustar: a oração é o sujeito → sem <i>de</i>. Com <i>de</i> seria dequeísmo.", 'g:alegrar'),
    ("Me di cuenta ___ que era tarde.", "de", "<b>darse cuenta de que</b>. Omitir o <i>de</i> é queísmo.", 'p:darse cuenta'),
    ("Me acuerdo ___ que llovía.", "de", "<b>acordarse de que</b>.", 'p:acordarse'),
    ("Me preocupa ___ que no llame.", "— (nada)", "<i>Preocupar</i> (tipo gustar): a oração é o sujeito → <b>me preocupa que</b>. ‘De que’ seria dequeísmo.", 'g:preocupar'),
    ("Me preocupo ___ que no llame.", "de", "<i>Preocuparse</i> (pronominal) pede preposição: <b>me preocupo de/por que</b>.", 'p:preocuparse'),
    ("Se me olvidó ___ que tenía cita.", "— (nada)", "<i>Olvidársele algo</i>: a oração é o sujeito → sem <i>de</i>.", 'g:olvidar (involuntário)'),
    ("Me olvidé ___ que tenía cita.", "de", "<i>Olvidarse de</i> → <b>me olvidé de que</b>.", 'p:olvidarse'),
    ("Me extraña ___ que no llame.", "— (nada)", "<i>Extrañar</i> (achar estranho) é tipo gustar → sem <i>de</i>.", 'g:extrañar'),
    ("Me convencí ___ que era verdad.", "de", "<b>convencerse de que</b>.", 'p:convencerse'),
    ("Me enteré ___ que se casaba.", "de", "<b>enterarse de que</b>.", 'p:enterarse'),
    ("Me sorprende ___ que digas eso.", "— (nada)", "<i>Sorprender</i> tipo gustar → sem <i>de</i>.", 'g:sorprender'),
    ("Me sorprendí ___ que estuviera allí.", "de", "<i>Sorprenderse de</i> → <b>de que</b>.", 'p:sorprenderse'),
    ("Me da miedo ___ que se pierda.", "— (nada)", "<i>Dar miedo</i>: a oração é o sujeito → sem <i>de</i>.", 'g:dar miedo'),
    ("Me hace ilusión ___ que vengáis.", "— (nada)", "<i>Hacer ilusión</i>: a oração é o sujeito → sem <i>de</i>.", 'g:hacer ilusión'),
    ("Me arrepiento ___ no haber ido.", "de", "<b>arrepentirse de</b>.", 'p:arrepentirse'),
]:
    hma(6, 'Que × de que', 'Complete com “de” ou nada.', s, ['de', '— (nada)'], ans, x, v, False)
he(6, "Me di cuenta que era tarde.", [2, 3], "Me di cuenta de que era tarde.", "Queísmo: <i>darse cuenta</i> pede <b>de que</b>.", 'p:darse cuenta')
he(6, "Me preocupa de que no llame.", [2], "Me preocupa que no llame.", "Dequeísmo: com <i>preocupar</i> (tipo gustar) a oração é sujeito → sem <i>de</i>.", 'g:preocupar')

# me gustas
for s, ans, opts, x in [
    ("‘Me gustas’ significa:", "Eu gosto de você", ["Eu gosto de você", "Você gosta de mim", "Eu gosto de mim", "Você gosta de si mesmo"], "Quem agrada é <b>tú</b> (sujeito: gustas); quem gosta é <b>me</b> (eu)."),
    ("‘Te gusto’ significa:", "Você gosta de mim", ["Você gosta de mim", "Eu gosto de você", "Eu gosto de mim", "Você gosta de si"], "Sujeito <b>yo</b> (gusto); quem gosta: <b>te</b> (você)."),
    ("‘Le gustamos’ significa:", "Ele/ela gosta de nós", ["Ele/ela gosta de nós", "Nós gostamos dele/dela", "Nós gostamos de nós", "Eles gostam dele"], "Sujeito <b>nosotros</b> (gustamos); quem gosta: <b>le</b>."),
    ("‘Me gusto’ significa:", "Eu gosto de mim mesmo", ["Eu gosto de mim mesmo", "Eu gosto de você", "Você gosta de mim", "Eu gostei"], "Sujeito <b>yo</b> e pessoa afetada <b>me</b>: gosto de mim mesmo."),
    ("‘Nos caéis bien’ significa:", "Nós gostamos de vocês", ["Nós gostamos de vocês", "Vocês gostam de nós", "Vocês caíram bem", "Nós caímos bem"], "Sujeito <b>vosotros</b> (caéis); quem simpatiza: <b>nos</b>."),
    ("‘Le caes bien a mi madre’ significa:", "Minha mãe gosta de você", ["Minha mãe gosta de você", "Você gosta da minha mãe", "Você caiu perto da minha mãe", "Minha mãe gosta de si"], "Sujeito <b>tú</b> (caes); quem simpatiza: <b>a mi madre</b> (le)."),
]:
    hma(6, 'Me gustas', s, '', opts, ans, x, ['g:gustar'] if 'gust' in s else ['g:caer bien / mal'])
PERS_SUBJ = [('yo', 0), ('tú', 1), ('nosotros', 3), ('vosotros', 4), ('tus amigos', 5), ('tu hermana', 2)]
EXPP = [('a Ana', 'le', 'x'), ('a mí', 'me', 0), ('a ti', 'te', 1), ('a nosotros', 'nos', 3), ('a mis padres', 'les', 'x'), ('a vosotros', 'os', 4)]
for hd, cls, ex, gid in [('gustar', '', '', 'g:gustar'), ('caer', '', 'bien', 'g:caer bien / mal'), ('encantar', '', '', 'g:encantar'), ('molestar', '', '', 'g:molestar'), ('importar', '', '', 'g:importar')]:
    c = cj(hd, cls)
    for ps, i in PERS_SUBJ:
        for ea, pr, ei in EXPP:
            if ei == i or (i in (0, 3) and ei in (0, 3)) or (i in (1, 4) and ei in (1, 4)):
                continue
            if R.random() < .55:
                continue
            f = c['pres'][i]
            opts = list(dict.fromkeys([f, c['pres'][2], c['pres'][5], c['pres'][(i + 1) % 6]]))
            s = f"{cap(ps)} {pr} ___{(' ' + ex) if ex else ''} {ea}."
            H.append(('mc_ans', f, 'mc', 6, 'Me gustas', f'Complete com <i>{hd}</i> no presente.', s, opts,
                      f"Aqui quem agrada é <b>{ps}</b> (sujeito), então o verbo concorda com ele: <b>{f}</b>. Quem sente continua no pronome ({pr}).", gid, True))

for h in H:
    if h[0] == 'mc_ans':
        ans = h[1]
        _, lv, k, q, s, opts, x, v, sh = h[2:]
        B.mc(lv, k, q, s, opts, ans, x, v, 'hand', shuffle=sh)
    elif h[0] == 'mc':
        _, lv, k, q, s, opts, x, v, sh = h
        B.mc(lv, k, q, s, opts, opts[0], x, v, 'hand', shuffle=sh)
    elif h[0] == 'err':
        _, lv, sent, bad, fix, x, v = h
        B.err(lv, sent, bad, fix, x, v, 'hand')
    elif h[0] == 'in':
        _, lv, k, q, s, ans, x, v = h
        B.inp(lv, k, q, s, ans, x, v, 'hand')

# ============================================================== SELEÇÃO
ids_all = [e['id'] for e in ALL]
for it in B.items:
    for v in it['v']:
        assert v in BYID, v
chosen, cnt = select(B.items, ids_all, minc=3, targets={1: 220, 2: 320, 3: 320, 4: 300, 5: 260, 6: 240}, cap_per_entry=12, seed=7,
                     prio=[{'PD', 'GD'}, {'PA', 'GA', 'GB', 'PB'}, {'PG', 'PH', 'PK', 'GE', 'PF'}], gen_cap=0.25)
out = finalize(chosen, seed=11)

outdir = sys.argv[1] if len(sys.argv) > 1 else '.'
json.dump(out, open(os.path.join(outdir, 'pronominales.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
final_cnt = Counter(v for q in out for v in q['v'])
gloss = []
for e in ALL:
    gloss.append(dict(id=e['id'], v=e['name'], cat=e['cat'], kind=e['kind'], pt=e['pt'], ex=e['ex'], note=e.get('note', ''),
                      base=e.get('base') or '', base_pt=e.get('base_pt') or '', n=final_cnt.get(e['id'], 0)))
json.dump(gloss, open(os.path.join(outdir, 'pronominales-verbos.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

low_cov = [(e['id'], final_cnt.get(e['id'], 0)) for e in ALL if final_cnt.get(e['id'], 0) < 3]
print('candidatas:', len(B.items), '| escolhidas:', len(out), '| por nível:', dict(sorted(Counter(q['lv'] for q in out).items())), file=sys.stderr)
print('tipos:', dict(Counter(q['k'] for q in out).most_common()), file=sys.stderr)
print('itens do catálogo:', len(ALL), '| mínimo de questões por item:', min(final_cnt.get(i, 0) for i in ids_all), file=sys.stderr)
print('abaixo de 3:', low_cov, file=sys.stderr)
