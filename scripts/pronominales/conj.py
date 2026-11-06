# -*- coding: utf-8 -*-
"""Conjugador espanhol mínimo (presente, pretérito indefinido, subjuntivo presente,
imperativos, gerúndio) + colocação de clíticos com acentuação automática.

Classes de mudança de raiz (cls): 'ie', 'ue', 'i', 'ie-i', 'ue-u', 'í' (fiar), 'üe' (avergonzar).
Ortografia (c→qu, g→gu, z→c, g→j, c→zc, -uir→y) é deduzida do infinitivo.
"""

ACC = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}
UNACC = {v: k for k, v in ACC.items()}
VOW = set('aeiouáéíóúü')
STRONG = set('aeoáéóíú')  # vogais acentuadas fracas contam como fortes (rompem ditongo)


def strip(s):
    return ''.join(UNACC.get(c, c) for c in s)


# ---------------------------------------------------------------- irregulares
def _pref(full, base):
    return full[: len(full) - len(base)]

IRR_PRES = {
    'ir': 'voy vas va vamos vais van', 'dar': 'doy das da damos dais dan',
    'estar': 'estoy estás está estamos estáis están', 'ser': 'soy eres es somos sois son',
    'saber': 'sé sabes sabe sabemos sabéis saben', 'ver': 'veo ves ve vemos veis ven',
    'hacer': 'hago haces hace hacemos hacéis hacen', 'tener': 'tengo tienes tiene tenemos tenéis tienen',
    'venir': 'vengo vienes viene venimos venís vienen', 'decir': 'digo dices dice decimos decís dicen',
    'poner': 'pongo pones pone ponemos ponéis ponen', 'traer': 'traigo traes trae traemos traéis traen',
    'caer': 'caigo caes cae caemos caéis caen', 'salir': 'salgo sales sale salimos salís salen',
    'oír': 'oigo oyes oye oímos oís oyen',
}
IRR_PRET_FULL = {
    'ir': 'fui fuiste fue fuimos fuisteis fueron', 'ser': 'fui fuiste fue fuimos fuisteis fueron',
    'dar': 'di diste dio dimos disteis dieron', 'ver': 'vi viste vio vimos visteis vieron',
}
STRONG_PRET = {'hacer': 'hic', 'poner': 'pus', 'tener': 'tuv', 'estar': 'estuv', 'venir': 'vin',
               'querer': 'quis', 'poder': 'pud', 'saber': 'sup', 'decir': 'dij', 'traer': 'traj',
               'conducir': 'conduj', 'seducir': 'seduj', 'andar': 'anduv'}
IRR_SUBJ = {
    'ir': 'vaya vayas vaya vayamos vayáis vayan', 'dar': 'dé des dé demos deis den',
    'estar': 'esté estés esté estemos estéis estén', 'ser': 'sea seas sea seamos seáis sean',
    'saber': 'sepa sepas sepa sepamos sepáis sepan', 'ver': 'vea veas vea veamos veáis vean',
}
IRR_TU = {'poner': 'pon', 'hacer': 'haz', 'tener': 'ten', 'venir': 'ven', 'salir': 'sal',
          'decir': 'di', 'ir': 've', 'ser': 'sé'}
IRR_GER = {'ir': 'yendo', 'decir': 'diciendo', 'venir': 'viniendo', 'poder': 'pudiendo', 'oír': 'oyendo'}
# verbos derivados: prefixo + base irregular
DERIV = {'detener': 'tener', 'abstener': 'tener', 'entretener': 'tener', 'convenir': 'venir',
         'deshacer': 'hacer', 'atraer': 'traer', 'distraer': 'traer', 'satisfacer': 'hacer', 'descomponer': 'poner', 'componer': 'poner'}


def _base_irr(inf):
    if inf in DERIV:
        b = DERIV[inf]
        p = _pref(inf, b) if inf.endswith(b) else None
        if inf == 'satisfacer':
            return 'hacer', 'satisf', True
        return b, p, False
    return inf, '', False


def _re(form, pref, hf):
    """aplica prefixo; para satisfacer, o h- de hacer vira f-."""
    if hf:
        return pref + (form[1:] if form.startswith('h') else form)
    return pref + form


def _change_last(stem, src, dst):
    i = stem.rfind(src)
    return stem if i < 0 else stem[:i] + dst + stem[i + len(src):]


def _boot(stem, cls):
    if cls in ('ie', 'ie-i'):
        return _change_last(stem, 'e', 'ie')
    if cls in ('ue', 'ue-u'):
        return _change_last(stem, 'o', 'ue')
    if cls == 'üe':
        return _change_last(stem, 'o', 'üe')
    if cls == 'i':
        return _change_last(stem, 'e', 'i')
    if cls == 'í':
        return _change_last(stem, 'i', 'í')
    return stem


def _weak(stem, cls):  # -ir: 3ª pessoa do pretérito, nós/vós do subjuntivo, gerúndio
    if cls in ('i', 'ie-i'):
        return _change_last(stem, 'e', 'i')
    if cls == 'ue-u':
        return _change_last(stem, 'o', 'u')
    return stem


def _orth_e(stem):
    """ar → antes de e: c→qu, g→gu, z→c"""
    if stem.endswith('c'):
        return stem[:-1] + 'qu'
    if stem.endswith('g'):
        return stem[:-1] + 'gu'
    if stem.endswith('z'):
        return stem[:-1] + 'c'
    return stem


BOOT = (0, 1, 2, 5)


def conj(inf, cls=''):
    inf = inf.strip()
    stem, end = inf[:-2], inf[-2:]
    b, pref, hf = _base_irr(inf)
    R = {'inf': inf}
    uir = inf.endswith('uir') and not inf.endswith('guir')

    # ---- presente
    if b in IRR_PRES:
        pres = [_re(f, pref, hf) for f in IRR_PRES[b].split()]
    else:
        E = {'ar': 'o as a amos áis an', 'er': 'o es e emos éis en', 'ir': 'o es e imos ís en'}[end].split()
        pres = []
        for p in range(6):
            s = _boot(stem, cls) if p in BOOT and cls else stem
            if uir and p in BOOT:
                s = stem + 'y'
            if p == 0 and end in ('er', 'ir') and not cls.startswith('ue') and not cls.startswith('ie'):
                if s.endswith('g'):
                    s = s[:-1] + 'j'
                elif s.endswith('c'):
                    s = s[:-1] + ('zc' if s[-2] in VOW else 'z')
            elif p == 0 and end in ('er', 'ir') and s.endswith('g'):
                s = s[:-1] + 'j'
            elif p == 0 and end in ('er', 'ir') and s.endswith('c') and cls.startswith('ue'):
                s = s[:-1] + 'z'  # escocer → escuezo
            pres.append(s + E[p])
    R['pres'] = pres

    # ---- pretérito
    if b in IRR_PRET_FULL:
        pret = [_re(f, pref, hf) for f in IRR_PRET_FULL[b].split()]
    elif b in STRONG_PRET:
        st = _re(STRONG_PRET[b], pref, hf)
        pret = [st + 'e', st + 'iste', st + 'o', st + 'imos', st + 'isteis', st + ('eron' if st.endswith('j') else 'ieron')]
        if b == 'hacer':
            pret[2] = st[:-1] + 'zo'
    elif end == 'ar':
        pret = [_orth_e(stem) + 'é', stem + 'aste', stem + 'ó', stem + 'amos', stem + 'asteis', stem + 'aron']
    else:
        if stem[-1] in 'aeou':
            e2 = ['í', 'iste', 'yó', 'imos', 'isteis', 'yeron'] if stem.endswith('u') else ['í', 'íste', 'yó', 'ímos', 'ísteis', 'yeron']
            pret = [stem + x for x in e2]
        else:
            w = _weak(stem, cls) if end == 'ir' else stem
            pret = [stem + 'í', stem + 'iste', w + 'ió', stem + 'imos', stem + 'isteis', w + 'ieron']
    R['pret'] = pret

    # ---- subjuntivo presente
    if b in IRR_SUBJ:
        subj = [_re(f, pref, hf) for f in IRR_SUBJ[b].split()]
    else:
        E = ('e es e emos éis en' if end == 'ar' else 'a as a amos áis an').split()
        yo = pres[0]
        if cls and b not in IRR_PRES:
            boot = _boot(stem, cls)
            non = _weak(stem, cls) if end == 'ir' else stem
            if cls == 'i':
                non = boot
            if end == 'ar':
                boot, non = _orth_e(boot), _orth_e(non)
            elif yo.endswith('jo') or yo.endswith('zo'):
                boot, non = yo[:-1], yo[:-1].replace('ue', 'o') if cls.startswith('ue') else yo[:-1]
            subj = [(boot if p in BOOT else non) + E[p] for p in range(6)]
        else:
            ys = yo[:-1]
            if end == 'ar':
                ys = _orth_e(ys)
            subj = [ys + E[p] for p in range(6)]
    R['subj'] = subj

    # ---- gerúndio
    if b in IRR_GER:
        ger = _re(IRR_GER[b], pref, hf)
    elif end == 'ar':
        ger = stem + 'ando'
    elif stem[-1] in 'aeou':
        ger = stem + 'yendo'
    else:
        ger = (_weak(stem, cls) if end == 'ir' else stem) + 'iendo'
    R['ger'] = ger

    # ---- imperativos
    if b in IRR_TU:
        tu = _re(IRR_TU[b], pref, hf)
        if pref and not hf and tu[-1] == 'n':  # detén, abstén, entretén
            tu = tu[:-2] + ACC[tu[-2]] + 'n'
    else:
        tu = pres[2]
    R['tu'] = tu
    R['ud'] = subj[2]
    R['nos'] = 'vamos' if inf == 'ir' else subj[3]
    R['vos'] = inf[:-1] + 'd'
    return R


# ---------------------------------------------------------------- acentuação
def nuclei(w):
    """lista de núcleos silábicos (listas de índices de vogais)."""
    res, cur, prev_v = [], [], False
    i = 0
    while i < len(w):
        c = w[i]
        is_v = c in VOW
        if c == 'u' and i > 0 and w[i - 1] in 'qg' and i + 1 < len(w) and w[i + 1] in 'eiéí':
            is_v = False
        if is_v:
            if cur and prev_v and (w[cur[-1]] in STRONG and c in STRONG):
                res.append(cur)
                cur = [i]
            elif cur and prev_v:
                cur.append(i)
            else:
                if cur:
                    res.append(cur)
                cur = [i]
            prev_v = True
        else:
            prev_v = False
        i += 1
    if cur:
        res.append(cur)
    return res


def stress_idx(w):
    for i, c in enumerate(w):
        if c in UNACC:
            return i
    nu = nuclei(w)
    if not nu:
        return 0
    k = len(nu) - 2 if (w[-1] in 'aeiouns' and len(nu) > 1) else len(nu) - 1
    n = nu[k]
    strong = [i for i in n if w[i] in 'aeo']
    return strong[0] if strong else n[-1]


def place(word, s):
    """devolve word (sem acentos) com acento gráfico se as regras exigirem, sendo s o índice da vogal tônica."""
    w = strip(word)
    nu = nuclei(w)
    k = next(j for j, n in enumerate(nu) if s in n)
    need = False
    if w[s] in 'iu' and any(w[i] in 'aeo' for i in nu[k]):
        need = True  # hiato
    else:
        p = len(nu) - k
        last = w[-1]
        need = (p >= 3) or (p == 2 and last not in 'aeiouns') or (p == 1 and last in 'aeiouns' and len(nu) > 1)
    return w[:s] + ACC[w[s]] + w[s + 1:] if need else w


def attach(base, clitics, mode=''):
    """une clíticos à forma verbal (imperativo, infinitivo, gerúndio) com a acentuação correta."""
    if isinstance(clitics, str):
        clitics = clitics.split()
    s = stress_idx(base)
    b = base
    if mode == 'nos' and clitics and clitics[0] in ('nos', 'se'):
        b = b[:-1]
    if mode == 'vos' and clitics and clitics[0] == 'os' and b != 'id':
        b = b[:-1]
    return place(strip(b) + ''.join(clitics), s)


if __name__ == '__main__':
    T = [
        (attach('levanta', 'te'), 'levántate'), (attach('pon', 'te'), 'ponte'), (attach('pon', 'te lo'), 'póntelo'),
        (attach('di', 'se lo'), 'díselo'), (attach('di', 'me'), 'dime'), (attach('levantemos', 'nos', 'nos'), 'levantémonos'),
        (attach('vamos', 'nos', 'nos'), 'vámonos'), (attach('levantad', 'os', 'vos'), 'levantaos'),
        (attach('vestid', 'os', 'vos'), 'vestíos'), (attach('poned', 'os', 'vos'), 'poneos'), (attach('dé', 'lo'), 'delo'),
        (attach('dé', 'se lo'), 'déselo'), (attach('levantar', 'me'), 'levantarme'), (attach('levantar', 'se lo'), 'levantárselo'),
        (attach('levantando', 'me'), 'levantándome'), (attach('duerme', 'te'), 'duérmete'), (attach('cuide', 'se'), 'cuídese'),
        (attach('detén', 'te'), 'detente'), (attach('esté', 'se'), 'estese'), (attach('haz', 'te lo'), 'háztelo'),
        (attach('fíe', 'se'), 'fíese'), (attach('caed', 'os', 'vos'), 'caeos'), (attach('tranquiliza', 'te'), 'tranquilízate'),
        (attach('arrodilla', 'te'), 'arrodíllate'), (attach('dormid', 'os', 'vos'), 'dormíos'), (attach('sube', 'te'), 'súbete'),
        (attach('vistiendo', 'me'), 'vistiéndome'), (attach('yendo', 'me'), 'yéndome'), (attach('cayendo', 'me'), 'cayéndome'),
        (attach('date', ''), 'date'), (attach('da', 'te'), 'date'), (attach('ve', 'te'), 'vete'), (attach('vayamos', 'nos', 'nos'), 'vayámonos'),
        (attach('sentemos', 'nos', 'nos'), 'sentémonos'), (attach('pongamos', 'nos', 'nos'), 'pongámonos'), (attach('come', 'te la'), 'cómetela'),
        (attach('comiendo', 'me lo'), 'comiéndomelo'), (attach('comer', 'me lo'), 'comérmelo'), (attach('leer', 'me lo'), 'leérmelo'),
        (attach('lee', 'te'), 'léete'), (attach('atreved', 'os', 'vos'), 'atreveos'), (attach('divertid', 'os', 'vos'), 'divertíos'),
        (attach('espera', 'te'), 'espérate'), (attach('dad', 'se lo'), 'dádselo'), (attach('dad', 'lo'), 'dadlo'),
        (attach('fía', 'te'), 'fíate'), (attach('abriga', 'te'), 'abrígate'), (attach('acerca', 'te'), 'acércate'),
    ]
    C = [
        (conj('despertar', 'ie')['pres'], 'despierto despiertas despierta despertamos despertáis despiertan'),
        (conj('acostar', 'ue')['subj'], 'acueste acuestes acueste acostemos acostéis acuesten'),
        (conj('dormir', 'ue-u')['pret'], 'dormí dormiste durmió dormimos dormisteis durmieron'),
        (conj('dormir', 'ue-u')['subj'], 'duerma duermas duerma durmamos durmáis duerman'),
        (conj('vestir', 'i')['subj'], 'vista vistas vista vistamos vistáis vistan'),
        (conj('divertir', 'ie-i')['subj'], 'divierta diviertas divierta divirtamos divirtáis diviertan'),
        (conj('parecer')['pres'], 'parezco pareces parece parecemos parecéis parecen'),
        (conj('parecer')['subj'], 'parezca parezcas parezca parezcamos parezcáis parezcan'),
        (conj('dirigir')['pres'], 'dirijo diriges dirige dirigimos dirigís dirigen'),
        (conj('dirigir')['subj'], 'dirija dirijas dirija dirijamos dirijáis dirijan'),
        (conj('inmiscuir')['pres'], 'inmiscuyo inmiscuyes inmiscuye inmiscuimos inmiscuís inmiscuyen'),
        (conj('inmiscuir')['pret'], 'inmiscuí inmiscuiste inmiscuyó inmiscuimos inmiscuisteis inmiscuyeron'),
        (conj('inmiscuir')['subj'], 'inmiscuya inmiscuyas inmiscuya inmiscuyamos inmiscuyáis inmiscuyan'),
        (conj('fiar', 'í')['pres'], 'fío fías fía fiamos fiáis fían'),
        (conj('fiar', 'í')['subj'], 'fíe fíes fíe fiemos fiéis fíen'),
        (conj('avergonzar', 'üe')['pres'], 'avergüenzo avergüenzas avergüenza avergonzamos avergonzáis avergüenzan'),
        (conj('avergonzar', 'üe')['subj'], 'avergüence avergüences avergüence avergoncemos avergoncéis avergüencen'),
        (conj('avergonzar', 'üe')['pret'], 'avergoncé avergonzaste avergonzó avergonzamos avergonzasteis avergonzaron'),
        (conj('tropezar', 'ie')['subj'], 'tropiece tropieces tropiece tropecemos tropecéis tropiecen'),
        (conj('colgar', 'ue')['subj'], 'cuelgue cuelgues cuelgue colguemos colguéis cuelguen'),
        (conj('negar', 'ie')['pret'], 'negué negaste negó negamos negasteis negaron'),
        (conj('leer')['pret'], 'leí leíste leyó leímos leísteis leyeron'),
        (conj('caer')['pret'], 'caí caíste cayó caímos caísteis cayeron'),
        (conj('caer')['subj'], 'caiga caigas caiga caigamos caigáis caigan'),
        (conj('detener')['pres'], 'detengo detienes detiene detenemos detenéis detienen'),
        (conj('detener')['pret'], 'detuve detuviste detuvo detuvimos detuvisteis detuvieron'),
        (conj('abstener')['subj'], 'abstenga abstengas abstenga abstengamos abstengáis abstengan'),
        (conj('satisfacer')['pres'], 'satisfago satisfaces satisface satisfacemos satisfacéis satisfacen'),
        (conj('satisfacer')['pret'], 'satisfice satisficiste satisfizo satisficimos satisficisteis satisficieron'),
        (conj('deshacer')['pret'], 'deshice deshiciste deshizo deshicimos deshicisteis deshicieron'),
        (conj('convenir')['pret'], 'convine conviniste convino convinimos convinisteis convinieron'),
        (conj('seducir')['pres'], 'seduzco seduces seduce seducimos seducís seducen'),
        (conj('seducir')['pret'], 'seduje sedujiste sedujo sedujimos sedujisteis sedujeron'),
        (conj('conducir')['subj'], 'conduzca conduzcas conduzca conduzcamos conduzcáis conduzcan'),
        (conj('atraer')['pret'], 'atraje atrajiste atrajo atrajimos atrajisteis atrajeron'),
        (conj('convencer')['pres'], 'convenzo convences convence convencemos convencéis convencen'),
        (conj('escocer', 'ue')['pres'], 'escuezo escueces escuece escocemos escocéis escuecen'),
        (conj('ir')['subj'], 'vaya vayas vaya vayamos vayáis vayan'),
        (conj('despedir', 'i')['pret'], 'despedí despediste despidió despedimos despedisteis despidieron'),
        (conj('sentir', 'ie-i')['pret'], 'sentí sentiste sintió sentimos sentisteis sintieron'),
        (conj('querer', 'ie')['pret'], 'quise quisiste quiso quisimos quisisteis quisieron'),
        (conj('querer', 'ie')['subj'], 'quiera quieras quiera queramos queráis quieran'),
        (conj('saber')['pres'], 'sé sabes sabe sabemos sabéis saben'),
        (conj('mover', 'ue')['subj'], 'mueva muevas mueva movamos mováis muevan'),
        (conj('esforzar', 'ue')['subj'], 'esfuerce esfuerces esfuerce esforcemos esforcéis esfuercen'),
        (conj('enviar', 'í')['pres'], 'envío envías envía enviamos enviáis envían'),
        (conj('resfriar', 'í')['pret'], 'resfrié resfriaste resfrió resfriamos resfriasteis resfriaron'),
        (conj('morir', 'ue-u')['subj'], 'muera mueras muera muramos muráis mueran'),
        (conj('elegir', 'i')['pres'], 'elijo eliges elige elegimos elegís eligen'),
    ]
    G = [(conj('vestir', 'i')['ger'], 'vistiendo'), (conj('dormir', 'ue-u')['ger'], 'durmiendo'), (conj('inmiscuir')['ger'], 'inmiscuyendo'),
         (conj('caer')['ger'], 'cayendo'), (conj('detener')['tu'], 'detén'), (conj('abstener')['tu'], 'abstén'),
         (conj('ir')['nos'], 'vamos'), (conj('deshacer')['tu'], 'deshaz'), (conj('sentir', 'ie-i')['ger'], 'sintiendo')]
    bad = 0
    for got, exp in T + G:
        if got != exp:
            bad += 1; print('ATTACH/FORM', got, '!=', exp)
    for got, exp in C:
        if ' '.join(got) != exp:
            bad += 1; print('CONJ', ' '.join(got), '!=', exp)
    print('falhas:', bad, 'de', len(T) + len(C) + len(G))
