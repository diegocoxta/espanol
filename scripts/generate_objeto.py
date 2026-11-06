# -*- coding: utf-8 -*-
import random, json, unicodedata, sys
R = random.Random(2026)

def cap(s):
    for i, c in enumerate(s):
        if c.isalpha():
            return s[:i] + c.upper() + s[i+1:]
    return s

def strip_acc(s):
    s = s.replace('ñ', '\0')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').replace('\0', 'ñ')

OD3 = {'ms': 'lo', 'fs': 'la', 'mp': 'los', 'fp': 'las'}
GN = {'ms': 'masculino singular', 'fs': 'feminino singular', 'mp': 'masculino plural', 'fp': 'feminino plural'}

SUBJ = [("Yo", 0, True), ("Tú", 1, True), ("María", 2, False), ("Mi padre", 2, False), ("Nosotros", 3, True),
        ("Vosotros", 4, True), ("Mis amigos", 5, False), ("Ustedes", 5, True), ("Ana", 2, False),
        ("Los niños", 5, False), ("Usted", 2, True), ("Mi hermana", 2, False)]
SUBJ3 = [s for s in SUBJ if not s[2] or s[0] in ("Usted", "Ustedes")]
NAMES = {"María", "Ana", "Juan", "Pedro", "Marta", "Laura", "Lucía"}

def P(*a): return list(a)

# ---------------- transitive verbs (things) ----------------
VT = {
 'comprar': dict(pres=P('compro','compras','compra','compramos','compráis','compran'), pret=P('compré','compraste','compró','compramos','comprasteis','compraron'), inf='comprar', ger='comprando',
    imp=('compra','cómpra','compres','compre','cómpre'),
    objs=[("el pan","ms"),("la leche","fs"),("los libros","mp"),("las flores","fp"),("el periódico","ms"),("las entradas","fp"),("la fruta","fs"),("los zapatos","mp")]),
 'leer': dict(pres=P('leo','lees','lee','leemos','leéis','leen'), pret=P('leí','leíste','leyó','leímos','leísteis','leyeron'), inf='leer', ger='leyendo',
    imp=('lee','lée','leas','lea','léa'),
    objs=[("el periódico","ms"),("la carta","fs"),("los libros","mp"),("las noticias","fp"),("la novela","fs"),("los mensajes","mp")]),
 'escribir': dict(pres=P('escribo','escribes','escribe','escribimos','escribís','escriben'), pret=P('escribí','escribiste','escribió','escribimos','escribisteis','escribieron'), inf='escribir', ger='escribiendo',
    imp=('escribe','escríbe','escribas','escriba','escríba'),
    objs=[("la carta","fs"),("el informe","ms"),("los correos","mp"),("las invitaciones","fp"),("el mensaje","ms")]),
 'comer': dict(pres=P('como','comes','come','comemos','coméis','comen'), pret=P('comí','comiste','comió','comimos','comisteis','comieron'), inf='comer', ger='comiendo',
    imp=('come','cóme','comas','coma','cóma'),
    objs=[("la manzana","fs"),("el pescado","ms"),("las galletas","fp"),("los tacos","mp"),("la sopa","fs")]),
 'beber': dict(pres=P('bebo','bebes','bebe','bebemos','bebéis','beben'), pret=P('bebí','bebiste','bebió','bebimos','bebisteis','bebieron'), inf='beber', ger='bebiendo',
    imp=('bebe','bébe','bebas','beba','béba'),
    objs=[("el café","ms"),("la leche","fs"),("los refrescos","mp"),("las cervezas","fp"),("el zumo","ms")]),
 'ver': dict(pres=P('veo','ves','ve','vemos','veis','ven'), pret=P('vi','viste','vio','vimos','visteis','vieron'), inf='ver', ger='viendo', imp=None,
    objs=[("la película","fs"),("el partido","ms"),("las series","fp"),("los documentales","mp"),("el programa","ms")]),
 'lavar': dict(pres=P('lavo','lavas','lava','lavamos','laváis','lavan'), pret=P('lavé','lavaste','lavó','lavamos','lavasteis','lavaron'), inf='lavar', ger='lavando',
    imp=('lava','láva','laves','lave','láve'),
    objs=[("los platos","mp"),("la ropa","fs"),("el coche","ms"),("las camisas","fp")]),
 'abrir': dict(pres=P('abro','abres','abre','abrimos','abrís','abren'), pret=P('abrí','abriste','abrió','abrimos','abristeis','abrieron'), inf='abrir', ger='abriendo',
    imp=('abre','ábre','abras','abra','ábra'),
    objs=[("la puerta","fs"),("las ventanas","fp"),("el regalo","ms"),("los paquetes","mp")]),
 'cerrar': dict(pres=P('cierro','cierras','cierra','cerramos','cerráis','cierran'), pret=P('cerré','cerraste','cerró','cerramos','cerrasteis','cerraron'), inf='cerrar', ger='cerrando',
    imp=('cierra','ciérra','cierres','cierre','ciérre'),
    objs=[("la puerta","fs"),("las ventanas","fp"),("el grifo","ms"),("los cajones","mp")]),
 'hacer': dict(pres=P('hago','haces','hace','hacemos','hacéis','hacen'), pret=P('hice','hiciste','hizo','hicimos','hicisteis','hicieron'), inf='hacer', ger='haciendo',
    imp=('haz','haz','hagas','haga','hága'),
    objs=[("la tarea","fs"),("los deberes","mp"),("la cama","fs"),("el pastel","ms"),("las maletas","fp")]),
 'traer': dict(pres=P('traigo','traes','trae','traemos','traéis','traen'), pret=P('traje','trajiste','trajo','trajimos','trajisteis','trajeron'), inf='traer', ger='trayendo',
    imp=('trae','tráe','traigas','traiga','tráiga'),
    objs=[("el vino","ms"),("las bebidas","fp"),("la tarta","fs"),("los documentos","mp")]),
 'buscar': dict(pres=P('busco','buscas','busca','buscamos','buscáis','buscan'), pret=P('busqué','buscaste','buscó','buscamos','buscasteis','buscaron'), inf='buscar', ger='buscando',
    imp=('busca','búsca','busques','busque','búsque'),
    objs=[("las llaves","fp"),("el móvil","ms"),("la dirección","fs"),("los billetes","mp")]),
 'preparar': dict(pres=P('preparo','preparas','prepara','preparamos','preparáis','preparan'), pret=P('preparé','preparaste','preparó','preparamos','preparasteis','prepararon'), inf='preparar', ger='preparando',
    imp=('prepara','prepára','prepares','prepare','prepáre'),
    objs=[("la cena","fs"),("el desayuno","ms"),("las maletas","fp"),("los informes","mp")]),
 'perder': dict(pres=P('pierdo','pierdes','pierde','perdemos','perdéis','pierden'), pret=P('perdí','perdiste','perdió','perdimos','perdisteis','perdieron'), inf='perder', ger='perdiendo', imp=None,
    objs=[("las llaves","fp"),("el autobús","ms"),("la cartera","fs"),("los papeles","mp")]),
 'limpiar': dict(pres=P('limpio','limpias','limpia','limpiamos','limpiáis','limpian'), pret=P('limpié','limpiaste','limpió','limpiamos','limpiasteis','limpiaron'), inf='limpiar', ger='limpiando',
    imp=('limpia','límpia','limpies','limpie','límpie'),
    objs=[("la cocina","fs"),("el baño","ms"),("las ventanas","fp"),("los muebles","mp")]),
 'terminar': dict(pres=P('termino','terminas','termina','terminamos','termináis','terminan'), pret=P('terminé','terminaste','terminó','terminamos','terminasteis','terminaron'), inf='terminar', ger='terminando',
    imp=('termina','termína','termines','termine','termíne'),
    objs=[("el proyecto","ms"),("la tesis","fs"),("los ejercicios","mp"),("las tareas","fp")]),
 'escuchar': dict(pres=P('escucho','escuchas','escucha','escuchamos','escucháis','escuchan'), pret=P('escuché','escuchaste','escuchó','escuchamos','escuchasteis','escucharon'), inf='escuchar', ger='escuchando',
    imp=('escucha','escúcha','escuches','escuche','escúche'),
    objs=[("la radio","fs"),("el disco","ms"),("las canciones","fp"),("los pódcasts","mp")]),
 'necesitar': dict(pres=P('necesito','necesitas','necesita','necesitamos','necesitáis','necesitan'), pret=P('necesité','necesitaste','necesitó','necesitamos','necesitasteis','necesitaron'), inf='necesitar', ger='necesitando', imp=None,
    objs=[("el ordenador","ms"),("la información","fs"),("los datos","mp"),("las tijeras","fp")]),
}

# ---------------- person-object verbs ----------------
VP = {
 'invitar': P('invito','invitas','invita','invitamos','invitáis','invitan'),
 'llamar': P('llamo','llamas','llama','llamamos','llamáis','llaman'),
 'visitar': P('visito','visitas','visita','visitamos','visitáis','visitan'),
 'ayudar': P('ayudo','ayudas','ayuda','ayudamos','ayudáis','ayudan'),
 'esperar': P('espero','esperas','espera','esperamos','esperáis','esperan'),
 'conocer': P('conozco','conoces','conoce','conocemos','conocéis','conocen'),
 'saludar': P('saludo','saludas','saluda','saludamos','saludáis','saludan'),
 'ver': P('veo','ves','ve','vemos','veis','ven'),
 'escuchar': P('escucho','escuchas','escucha','escuchamos','escucháis','escuchan'),
}
PERS = [("a Juan","ms"),("a María","fs"),("a los niños","mp"),("a mis primas","fp"),("a Pedro y a Ana","mp"),
        ("a mi abuela","fs"),("a sus vecinos","mp"),("a las profesoras","fp"),("a tu hermano","ms"),("al profesor","ms"),("a la doctora","fs")]

# ---------------- ditransitive verbs ----------------
# imp: (tu, tu1, tu2, neg, ud, ud1, ud2, nos, nos_acc, vos, vos2)
DT = {
 'dar': dict(pres=P('doy','das','da','damos','dais','dan'), pret=P('di','diste','dio','dimos','disteis','dieron'), inf='dar', ger='dando',
   imp=('da','da','dá','des','dé','de','dé','demos','démos','dad','dád'),
   th=[("el libro","ms"),("la llave","fs"),("los documentos","mp"),("las entradas","fp"),("el dinero","ms")]),
 'regalar': dict(pres=P('regalo','regalas','regala','regalamos','regaláis','regalan'), pret=P('regalé','regalaste','regaló','regalamos','regalasteis','regalaron'), inf='regalar', ger='regalando',
   imp=('regala','regála','regála','regales','regale','regále','regále','regalemos','regalémos','regalad','regalád'),
   th=[("el perfume","ms"),("la bufanda","fs"),("los libros","mp"),("las flores","fp")]),
 'enviar': dict(pres=P('envío','envías','envía','enviamos','enviáis','envían'), pret=P('envié','enviaste','envió','enviamos','enviasteis','enviaron'), inf='enviar', ger='enviando',
   imp=('envía','envía','envía','envíes','envíe','envíe','envíe','enviemos','enviémos','enviad','enviád'),
   th=[("la carta","fs"),("el paquete","ms"),("los documentos","mp"),("las fotos","fp")]),
 'mandar': dict(pres=P('mando','mandas','manda','mandamos','mandáis','mandan'), pret=P('mandé','mandaste','mandó','mandamos','mandasteis','mandaron'), inf='mandar', ger='mandando',
   imp=('manda','mánda','mánda','mandes','mande','mánde','mánde','mandemos','mandémos','mandad','mandád'),
   th=[("el mensaje","ms"),("la invitación","fs"),("los correos","mp"),("las fotos","fp")]),
 'prestar': dict(pres=P('presto','prestas','presta','prestamos','prestáis','prestan'), pret=P('presté','prestaste','prestó','prestamos','prestasteis','prestaron'), inf='prestar', ger='prestando',
   imp=('presta','présta','présta','prestes','preste','préste','préste','prestemos','prestémos','prestad','prestád'),
   th=[("el coche","ms"),("la bicicleta","fs"),("los apuntes","mp"),("las tijeras","fp")]),
 'explicar': dict(pres=P('explico','explicas','explica','explicamos','explicáis','explican'), pret=P('expliqué','explicaste','explicó','explicamos','explicasteis','explicaron'), inf='explicar', ger='explicando',
   imp=('explica','explíca','explíca','expliques','explique','explíque','explíque','expliquemos','expliquémos','explicad','explicád'),
   th=[("el problema","ms"),("la lección","fs"),("los ejercicios","mp"),("las reglas","fp")]),
 'contar': dict(pres=P('cuento','cuentas','cuenta','contamos','contáis','cuentan'), pret=P('conté','contaste','contó','contamos','contasteis','contaron'), inf='contar', ger='contando',
   imp=('cuenta','cuénta','cuénta','cuentes','cuente','cuénte','cuénte','contemos','contémos','contad','contád'),
   th=[("la historia","fs"),("el secreto","ms"),("los chistes","mp"),("las noticias","fp")]),
 'enseñar': dict(pres=P('enseño','enseñas','enseña','enseñamos','enseñáis','enseñan'), pret=P('enseñé','enseñaste','enseñó','enseñamos','enseñasteis','enseñaron'), inf='enseñar', ger='enseñando',
   imp=('enseña','enséña','enséña','enseñes','enseñe','enséñe','enséñe','enseñemos','enseñémos','enseñad','enseñád'),
   th=[("las fotos","fp"),("el piso","ms"),("la casa","fs"),("los dibujos","mp")]),
 'decir': dict(pres=P('digo','dices','dice','decimos','decís','dicen'), pret=P('dije','dijiste','dijo','dijimos','dijisteis','dijeron'), inf='decir', ger='diciendo',
   imp=('di','di','dí','digas','diga','díga','díga','digamos','digámos','decid','decíd'),
   th=[("la verdad","fs"),("el precio","ms"),("los nombres","mp"),("las respuestas","fp")]),
 'traer': dict(pres=P('traigo','traes','trae','traemos','traéis','traen'), pret=P('traje','trajiste','trajo','trajimos','trajisteis','trajeron'), inf='traer', ger='trayendo',
   imp=('trae','tráe','tráe','traigas','traiga','tráiga','tráiga','traigamos','traigámos','traed','traéd'),
   th=[("el café","ms"),("la cuenta","fs"),("las bebidas","fp"),("los platos","mp")]),
 'devolver': dict(pres=P('devuelvo','devuelves','devuelve','devolvemos','devolvéis','devuelven'), pret=P('devolví','devolviste','devolvió','devolvimos','devolvisteis','devolvieron'), inf='devolver', ger='devolviendo',
   imp=('devuelve','devuélve','devuélve','devuelvas','devuelva','devuélva','devuélva','devolvamos','devolvámos','devolved','devolvéd'),
   th=[("el libro","ms"),("la llave","fs"),("los discos","mp"),("las películas","fp")]),
 'vender': dict(pres=P('vendo','vendes','vende','vendemos','vendéis','venden'), pret=P('vendí','vendiste','vendió','vendimos','vendisteis','vendieron'), inf='vender', ger='vendiendo',
   imp=('vende','vénde','vénde','vendas','venda','vénda','vénda','vendamos','vendámos','vended','vendéd'),
   th=[("el coche","ms"),("la casa","fs"),("los muebles","mp"),("las entradas","fp")]),
 'entregar': dict(pres=P('entrego','entregas','entrega','entregamos','entregáis','entregan'), pret=P('entregué','entregaste','entregó','entregamos','entregasteis','entregaron'), inf='entregar', ger='entregando',
   imp=('entrega','entréga','entréga','entregues','entregue','entrégue','entrégue','entreguemos','entreguémos','entregad','entregád'),
   th=[("el informe","ms"),("la tarea","fs"),("los exámenes","mp"),("las llaves","fp")]),
 'pedir': dict(pres=P('pido','pides','pide','pedimos','pedís','piden'), pret=P('pedí','pediste','pidió','pedimos','pedisteis','pidieron'), inf='pedir', ger='pidiendo',
   imp=('pide','píde','píde','pidas','pida','pída','pída','pidamos','pidámos','pedid','pedíd'),
   th=[("el dinero","ms"),("la cuenta","fs"),("los apuntes","mp"),("las llaves","fp")]),
 'escribir': dict(pres=P('escribo','escribes','escribe','escribimos','escribís','escriben'), pret=P('escribí','escribiste','escribió','escribimos','escribisteis','escribieron'), inf='escribir', ger='escribiendo',
   imp=('escribe','escríbe','escríbe','escribas','escriba','escríba','escríba','escribamos','escribámos','escribid','escribíd'),
   th=[("la carta","fs"),("el poema","ms"),("los mensajes","mp"),("las postales","fp")]),
 'comprar': dict(pres=P('compro','compras','compra','compramos','compráis','compran'), pret=P('compré','compraste','compró','compramos','comprasteis','compraron'), inf='comprar', ger='comprando',
   imp=('compra','cómpra','cómpra','compres','compre','cómpre','cómpre','compremos','comprémos','comprad','comprád'),
   th=[("el regalo","ms"),("la bicicleta","fs"),("los juguetes","mp"),("las entradas","fp")]),
 'mostrar': dict(pres=P('muestro','muestras','muestra','mostramos','mostráis','muestran'), pret=P('mostré','mostraste','mostró','mostramos','mostrasteis','mostraron'), inf='mostrar', ger='mostrando',
   imp=('muestra','muéstra','muéstra','muestres','muestre','muéstre','muéstre','mostremos','mostrémos','mostrad','mostrád'),
   th=[("el camino","ms"),("la ciudad","fs"),("los resultados","mp"),("las fotos","fp")]),
}
REC3 = [("a Juan","le"),("a María","le"),("a mi madre","le"),("a mi hermano","le"),("a los alumnos","les"),
        ("a mis padres","les"),("a las chicas","les"),("a sus clientes","les"),("a la profesora","le"),("a los vecinos","les")]
REC12 = [("me", "te"), ("te", "me"), ("nos", "os"), ("os", "nos")]  # clitic, mirrored in answer
SUBJ_FOR_12 = [("María",2),("Mi padre",2),("Mis amigos",5),("Ana",2),("Juan",2),("Los niños",5)]

def inf_acc(inf):
    return inf[:-2] + {'a': 'á', 'e': 'é', 'i': 'í'}[inf[-2]] + inf[-1]
def ger_acc(g):
    if g.endswith('ando'): return g[:-4] + 'ándo'
    return g[:-4] + 'éndo'

AUX = [("ir a", P('voy a','vas a','va a','vamos a','vais a','van a')),
       ("querer", P('quiero','quieres','quiere','queremos','queréis','quieren')),
       ("tener que", P('tengo que','tienes que','tiene que','tenemos que','tenéis que','tienen que')),
       ("poder", P('puedo','puedes','puede','podemos','podéis','pueden')),
       ("deber", P('debo','debes','debe','debemos','debéis','deben')),
       ("acabar de", P('acabo de','acabas de','acaba de','acabamos de','acabáis de','acaban de'))]
ESTAR = P('estoy','estás','está','estamos','estáis','están')

Q = []
def item(lv, k, t, q, s, **kw):
    d = dict(lv=lv, k=k, t=t, q=q, s=s); d.update(kw); return d

def mc(lv, k, q, s, opts, correct, x, shuffle=True):
    opts = list(dict.fromkeys(opts))
    if shuffle: R.shuffle(opts)
    return item(lv, k, 'mc', q, s, o=opts, a=opts.index(correct), x=x)

def err(lv, s, bad, fix, x, q="Clique na palavra com erro — ou em “Não há erro”."):
    w = s.split(' ')
    if isinstance(bad, int): bad = [bad] if bad >= 0 else []
    return item(lv, 'Encontrar o erro', 'err', q, '', w=w, a=bad, fix=fix, x=x)

def inp(lv, k, q, s, answers, x):
    return item(lv, k, 'in', q, s, a=list(dict.fromkeys(answers)), x=x)

def ordq(lv, q, sentence, alts, x, keep=()):
    toks = sentence.rstrip('.?!').split(' ')
    toks = [t if t in NAMES else t.lower() for t in toks]
    answers = [a.rstrip('.?!').lower() for a in [sentence] + list(alts)]
    return item(lv, 'Ordenar', 'ord', q, '', w=toks, a=list(dict.fromkeys(answers)), x=x)

def drop_subj(subj, isp, rest):
    return cap(rest) if isp else None

def take(cands, n):
    seen, out = set(), []
    R.shuffle(cands)
    for c in cands:
        key = (c['t'], c['q'], c['s'], json.dumps(c.get('w')), json.dumps(c.get('o')))
        if key in seen: continue
        seen.add(key); out.append(c)
        if len(out) >= n: break
    if len(out) < n: print('WARN short', cands[0]['lv'] if cands else '?', cands[0]['k'] if cands else '', len(out), n, file=sys.stderr)
    return out

Q_SUB_OD = "Reescreva a frase trocando o objeto direto destacado pelo pronome."

# =========================== NÍVEL 1 ===========================
def n1():
    out = []
    # substituir
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            for subj, i, isp in SUBJ:
                neg = R.random() < 0.3
                n = 'no ' if neg else ''
                p = OD3[gn]; verb = v['pres'][i]
                s = f"{subj} {n}{verb} [[{np}]]."
                ans = [f"{subj} {n}{p} {verb}."]
                if isp and subj not in ('Usted', 'Ustedes'): ans.append(cap(f"{n}{p} {verb}."))
                x = f"‘{np}’ é objeto direto {GN[gn]} → <b>{p}</b>. Com verbo conjugado, o pronome vai <b>antes</b> do verbo" + (" (e depois do <i>no</i>)." if neg else ".")
                c.append(inp(1, 'Substituir', Q_SUB_OD, s, ans, x))
    out += take(c, 62)
    # completar diálogo
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            p = OD3[gn]
            pats = [(f"—¿{cap(v['pres'][1])} {np}? —Sí, ___ {v['pres'][0]}.", 'tú → yo'),
                    (f"—¿{cap(v['pres'][4])} {np}? —Sí, ___ {v['pres'][3]}.", 'vosotros → nosotros'),
                    (f"—¿María {v['pres'][2]} {np}? —No, no ___ {v['pres'][2]}.", ''),
                    (f"—¿Tus padres {v['pres'][5]} {np}? —Sí, ___ {v['pres'][5]}.", '')]
            for s, _ in pats:
                x = f"O pronome retoma ‘{np}’ ({GN[gn]}) → <b>{p}</b>, colocado antes do verbo conjugado."
                c.append(mc(1, 'Completar', 'Complete com o pronome de objeto direto.', s, ['lo','la','los','las'], p, x, shuffle=False))
    out += take(c, 52)
    # encontrar o erro
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            p = OD3[gn]
            for who in ["Mi madre", "Pablo", "Mi vecina", "Mis hermanos"]:
                i = 5 if who == "Mis hermanos" else 2
                verb = v['pres'][i]
                good = R.random() < 0.3
                w = p if good else R.choice([o for o in OD3.values() if o != p])
                s = f"—¿Quién {v['pres'][2]} {np}? —{who} {w} {verb}."
                fix = f"—¿Quién {v['pres'][2]} {np}? —{who} {p} {verb}."
                idx = -1 if good else len(f"—¿Quién {v['pres'][2]} {np}? —{who}".split(' '))
                x = (f"Está correto: ‘{np}’ é {GN[gn]} → {p}." if good else
                     f"‘{np}’ é {GN[gn]}, então o pronome é <b>{p}</b>, não <i>{w}</i>.")
                c.append(err(1, s, idx, fix, x))
    out += take(c, 28)
    # ordenar
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            for subj, i, isp in [("María",2,False),("Mi padre",2,False),("Los niños",5,False),("Ana",2,False),("Mis amigos",5,False)]:
                p = OD3[gn]; verb = v['pres'][i]
                sent = f"{subj} no {p} {verb}."
                alt = f"no {p} {verb} {subj}"
                x = f"Ordem: (sujeito) + <b>no</b> + pronome + verbo. O pronome ({p} = {np}) fica colado antes do verbo; o <i>no</i> vem antes de tudo."
                c.append(ordq(1, f"Monte a frase negativa em que o pronome substitui ‘{np}’.", sent, [alt], x))
    out += take(c, 14)
    # armadilhas de gênero
    traps = [
     ("—¿Dónde está el agua? —No sé, no ___ veo.","la","‘agua’ é <b>feminino</b>: usa <i>el</i> só porque começa com <i>a</i> tônica (el agua fría). O pronome é la."),
     ("—¿Entiendes el problema? —Sí, ___ entiendo.","lo","‘problema’ é masculino (palavras gregas em -ma: el tema, el sistema, el idioma)."),
     ("—¿Tienes el mapa? —Sí, ___ tengo aquí.","lo","‘mapa’ é masculino apesar do -a."),
     ("—¿Has visto la foto? —Sí, ya ___ he visto.","la","‘foto’ é feminino (abreviação de la fotografía)."),
     ("—¿Vendes la moto? —No, no ___ vendo.","la","‘moto’ é feminino (la motocicleta)."),
     ("—¿Compramos el sofá? —Sí, ___ compramos.","lo","‘sofá’ é masculino."),
     ("—¿Apagas la radio? —Sí, ahora ___ apago.","la","Na Espanha e em boa parte da América, ‘radio’ (aparelho/emissora) é feminino: la radio."),
     ("—¿Conoces el tema? —Sí, ___ conozco bien.","lo","‘tema’ é masculino."),
     ("—¿Estudias el idioma? —Sí, ___ estudio cada día.","lo","‘idioma’ é masculino."),
     ("—¿Usas el hacha? —Sí, ___ uso para la leña.","la","‘hacha’ é feminino (el hacha afilada)."),
     ("—¿Limpiaste el aula? —Sí, ___ limpié ayer.","la","‘aula’ é feminino (el aula vacía)."),
     ("—¿Ves el planeta? —Sí, ___ veo con el telescopio.","lo","‘planeta’ é masculino."),
     ("—¿Pintaste el águila? —Sí, ___ pinté de negro.","la","‘águila’ é feminino (el águila real)."),
     ("—¿Conoces el clima de aquí? —Sí, ___ conozco.","lo","‘clima’ é masculino."),
     ("—¿Tienes los mapas? —Sí, ___ tengo.","los","‘mapas’: masculino plural."),
     ("—¿Recibiste las fotos? —Sí, ___ recibí.","las","‘fotos’: feminino plural."),
     ("—¿Entendiste los problemas? —Sí, ___ entendí.","los","‘problemas’: masculino plural."),
     ("—¿Ya pediste el agua mineral? —Sí, ya ___ pedí.","la","‘agua’ continua feminino mesmo com <i>el</i>."),
     ("—¿Haces el crucigrama? —Sí, ___ hago cada domingo.","lo","‘crucigrama’ é masculino."),
     ("—¿Me prestas el lápiz? —Sí, aquí ___ tienes.","lo","‘lápiz’ é masculino."),
     ("—¿Viste el sistema nuevo? —Sí, ___ vi ayer.","lo","‘sistema’ é masculino."),
     ("—¿Tienes las manos limpias? —Sí, ___ tengo limpias.","las","‘mano’ é feminino apesar do -o."),
     ("—¿Arreglaste el reloj? —Sí, ___ arreglé.","lo","‘reloj’ é masculino."),
     ("—¿Tocas el piano? —Sí, ___ toco desde niño.","lo","‘piano’ é masculino."),
    ]
    for s, a, x in traps:
        out.append(mc(1, 'Completar', 'Atenção ao gênero do substantivo. Complete.', s, ['lo','la','los','las'], a, x, shuffle=False))
    return out

# =========================== NÍVEL 2 ===========================
def n2():
    out = []
    c = []
    for vk, conj in VP.items():
        for per, gn in PERS:
            for subj, i, isp in SUBJ:
                if vk == 'ver' and R.random() < .5: continue
                p = OD3[gn]
                s = f"{subj} {conj[i]} [[{per}]]."
                ans = [f"{subj} {p} {conj[i]}."]
                note = ''
                if gn == 'ms':
                    ans.append(f"{subj} le {conj[i]}.")
                    note = " (Na Espanha também se ouve <i>le</i> para homem no singular — leísmo admitido; <i>lo</i> é o recomendado.)"
                if isp and subj not in ('Usted','Ustedes'): ans.append(cap(f"{p} {conj[i]}."))
                extra = " Pessoas de sexos diferentes juntas → masculino plural." if 'y a' in per else ''
                x = f"‘{per}’ leva <i>a</i> pessoal, mas continua sendo <b>objeto direto</b> → <b>{p}</b>.{extra}{note}"
                c.append(inp(2, 'Substituir', Q_SUB_OD, s, ans, x))
    out += take(c, 40)
    # me/te/nos/os
    c = []
    vb = [('llamar', 'mañana'), ('invitar', 'a la fiesta'), ('visitar', 'este verano'), ('ayudar', 'con la mudanza'),
          ('esperar', 'en la estación'), ('ver', 'desde aquí'), ('escuchar', 'bien'), ('conocer', 'de algo')]
    for vk, tail in vb:
        cj = VP[vk]
        c.append(mc(2, 'Completar', 'Complete com o pronome adequado.', f"—¿Me {cj[1]} {tail}? —Sí, claro, ___ {cj[0]} {tail}.", ['me','te','nos','os'], 'te', "Quem pergunta diz <i>me</i> (a mim); quem responde fala com ‘tú’ → <b>te</b>."))
        c.append(mc(2, 'Completar', 'Complete com o pronome adequado.', f"—¿Nos {cj[1]} {tail}? —Sí, ___ {cj[0]} {tail}.", ['me','te','nos','os'], 'os', "‘Nos’ (a nosotros) na resposta vira <b>os</b> (a vosotros). Na América, onde não se usa vosotros: <i>los</i> invito."))
        c.append(mc(2, 'Completar', 'Complete com o pronome adequado.', f"—¿María te {cj[2]} {tail}? —Sí, ___ {cj[2]} {tail}.", ['me','te','nos','os'], 'me', "A pergunta é sobre ‘ti’; quem responde fala de si → <b>me</b>."))
        c.append(mc(2, 'Completar', 'Complete com o pronome adequado.', f"—¿Tus padres os {cj[5]} {tail}? —Sí, ___ {cj[5]} {tail}.", ['me','te','nos','os'], 'nos', "‘os’ (a vosotros) → resposta em 1ª pessoa do plural: <b>nos</b>."))
        c.append(mc(2, 'Completar', 'Complete com o pronome adequado.', f"—¿Me {cj[4]} {tail}? —Sí, ___ {cj[3]} {tail}.", ['me','te','nos','os'], 'te', "Perguntam a ‘vosotros’ sobre ‘me’ (a mim); a resposta (nosotros) se dirige a ‘ti’ → <b>te</b>."))
    out += take(c, 32)
    # OI simples
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            for rec, pr in REC3:
                for subj, i, isp in SUBJ:
                    if subj in ('Usted','Ustedes') and 'usted' in rec: continue
                    s = f"{subj} ___ {v['pres'][i]} {np} {rec}."
                    x = f"‘{rec}’ é quem recebe → <b>objeto indireto</b>. {'Singular' if pr=='le' else 'Plural'} → <b>{pr}</b> (o mesmo para masculino e feminino). A duplicação (le… {rec}) é normal e natural."
                    c.append(mc(2, 'Completar', 'Complete com o pronome de objeto indireto.', s, ['le','les','lo','la'], pr, x, shuffle=False))
    out += take(c, 26)
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            for rec, pr in REC3:
                for subj, i, isp in SUBJ3:
                    s = f"{subj} {v['pres'][i]} {np} [[{rec}]]."
                    ans = [f"{subj} {pr} {v['pres'][i]} {np}.", f"{subj} {pr} {v['pres'][i]} {np} {rec}."]
                    x = f"‘{rec}’ é objeto indireto → <b>{pr}</b>, antes do verbo. O OD (‘{np}’) continua no lugar."
                    c.append(inp(2, 'Substituir', 'Troque o objeto indireto destacado pelo pronome (mantenha o objeto direto).', s, ans, x))
    out += take(c, 14)
    # identificar
    c = []
    OPTS = ['Objeto direto', 'Objeto indireto', 'Sujeito', 'Complemento circunstancial']
    for vk, v in DT.items():
        for np, gn in v['th']:
            for rec, pr in REC3:
                subj, i, _ = R.choice(SUBJ3)
                c.append(mc(2, 'Identificar', 'Qual é a função da parte destacada?', f"{subj} {pr} {v['pres'][i]} [[{np}]] {rec}.", OPTS, 'Objeto direto', f"‘{np}’ é <i>o que</i> se {v['inf']} → objeto direto (viraria {OD3[gn]}).", shuffle=False))
                c.append(mc(2, 'Identificar', 'Qual é a função da parte destacada?', f"{subj} {pr} {v['pres'][i]} {np} [[{rec}]].", OPTS, 'Objeto indireto', f"‘{rec}’ é <i>a quem</i> se {v['inf']} algo → objeto indireto ({pr}).", shuffle=False))
    for vk, conj in VP.items():
        for per, gn in PERS:
            c.append(mc(2, 'Identificar', 'Qual é a função da parte destacada?', f"Mi hermana {conj[2]} [[{per}]] {R.choice(['todos los días','a menudo','los domingos'])}.", OPTS, 'Objeto direto', f"Cuidado: o <i>a</i> aqui é o ‘a pessoal’. ‘{per}’ é objeto direto (viraria <b>{OD3[gn]}</b>), não indireto.", shuffle=False))
    gus = [("A Juan le gusta [[el chocolate]].","el chocolate"),("A mis padres les encantan [[los viajes]].","los viajes"),("Me duele [[la cabeza]].","la cabeza"),
           ("A Ana le interesan [[las noticias]].","las noticias"),("Nos falta [[tiempo]].","tiempo"),("Te queda bien [[esa camisa]].","esa camisa")]
    for s, np in gus:
        c.append(mc(2, 'Identificar', 'Qual é a função da parte destacada?', s, OPTS, 'Sujeito', f"Com verbos como <i>gustar</i>, ‘{np}’ é o <b>sujeito</b> (concorda com o verbo); a pessoa é o objeto indireto.", shuffle=False))
    out += take(c, 34)
    # a pessoal
    c = []
    persons = ["mi hermano","María","mis abuelos","la vecina","el profesor","tu padre","Pedro","los niños","el médico"]
    things = ["las llaves","la casa","el coche","mi móvil","un taxi","la estación","el libro","una farmacia"]
    vlist = [("Busco",), ("Veo",), ("Espero",), ("Llamo",), ("Necesito",)]
    for v, in vlist:
        for p_ in persons:
            if p_.startswith('el '):
                c.append(mc(2, 'Completar', "Complete com ‘a’, ‘al’ ou nada.", f"{v} ___ {p_[3:]}.", ['a','al','— (nada)'], 'al', f"OD de pessoa determinada leva <i>a</i>; <i>a + el</i> = <b>al</b>.", shuffle=False))
            else:
                c.append(mc(2, 'Completar', "Complete com ‘a’, ‘al’ ou nada.", f"{v} ___ {p_}.", ['a','al','— (nada)'], 'a', "OD de pessoa determinada leva <b>a</b> pessoal.", shuffle=False))
        for t_ in things:
            if v == 'Llamo' and t_ != 'un taxi': continue
            c.append(mc(2, 'Completar', "Complete com ‘a’, ‘al’ ou nada.", f"{v} ___ {t_}.", ['a','al','— (nada)'], '— (nada)', "OD de coisa não leva preposição.", shuffle=False))
    hand = [("Tengo ___ dos hermanos.", '— (nada)', "<i>Tener</i> normalmente dispensa o <i>a</i> pessoal: Tengo dos hermanos."),
            ("Buscamos ___ un camarero que hable inglés.", '— (nada)', "Pessoa <b>não específica</b> (qualquer um que fale inglês) → sem <i>a</i>."),
            ("Buscamos ___ un camarero que se llama Luis.", 'a', "Pessoa específica (já existe e tem nome) → <i>a</i>."),
            ("No veo ___ nadie.", 'a', "<i>Nadie</i> e <i>alguien</i> como OD levam <i>a</i>."),
            ("¿Conoces ___ alguien en Madrid?", 'a', "<i>Alguien</i> como OD leva <i>a</i>."),
            ("Visité ___ Madrid el año pasado.", '— (nada)', "Lugar não leva <i>a</i> pessoal."),
            ("Quiero mucho ___ mi perro.", 'a', "Com animais de estimação tratados afetivamente, usa-se <i>a</i>."),
            ("Hay ___ muchos estudiantes en el aula.", '— (nada)', "<i>Hay</i> nunca leva <i>a</i>."),
            ("Necesitamos ___ un fontanero urgente.", '— (nada)', "Pessoa indeterminada → normalmente sem <i>a</i>."),
            ("Llamé ___ mi jefe ayer.", 'a', "Pessoa determinada → <i>a</i>."),
            ("Admiro ___ los médicos de urgencias.", 'a', "Grupo determinado de pessoas → <i>a</i>."),
            ("El perro mordió ___ cartero.", 'al', "a + el = <b>al</b>.")]
    for s, a, x in hand:
        c.append(mc(2, 'Completar', "Complete com ‘a’, ‘al’ ou nada.", s, ['a','al','— (nada)'], a, x, shuffle=False))
    out += take(c, 30)
    return out

# =========================== NÍVEL 3 ===========================
def n3():
    out = []
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            for rec, pr in REC3:
                for subj, i, isp in SUBJ:
                    if subj in ('Usted','Ustedes') and 'usted' in rec: continue
                    p = OD3[gn]
                    s = f"{subj} {pr} {v['pres'][i]} [[{np}]] [[{rec}]]."
                    ans = [f"{subj} se {p} {v['pres'][i]}.", f"{subj} se {p} {v['pres'][i]} {rec}."]
                    if isp and subj not in ('Usted','Ustedes'): ans.append(cap(f"se {p} {v['pres'][i]}."))
                    x = f"OI ({pr}) + OD ({p}). Quando <i>le/les</i> aparece antes de <i>lo/la/los/las</i>, vira <b>se</b>: {pr} + {p} → <b>se {p}</b>. Ordem: OI antes do OD."
                    c.append(inp(3, 'Substituir', 'Substitua os DOIS objetos destacados por pronomes.', s, ans, x))
    out += take(c, 50)
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            for cl, _ in REC12:
                for subj, i in SUBJ_FOR_12:
                    p = OD3[gn]
                    s = f"{subj} {cl} {v['pres'][i]} [[{np}]]."
                    ans = [f"{subj} {cl} {p} {v['pres'][i]}."]
                    x = f"<i>{cl}</i> (OI) não muda; só <i>le/les</i> viram <i>se</i>. Ordem: OI + OD → <b>{cl} {p}</b>."
                    c.append(inp(3, 'Substituir', Q_SUB_OD, s, ans, x))
    out += take(c, 26)
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            p = OD3[gn]
            for rec, pr in REC3:
                s = f"—¿{cap(pr)} {v['pret'][1]} {np} {rec}? —Sí, ya ___ {v['pret'][0]}."
                opts = [f"se {p}", f"{pr} {p}", f"{p} {pr}", f"se {pr}"]
                x = f"OD ‘{np}’ → {p}; OI ‘{rec}’ → {pr}, que diante de {p} vira <b>se</b>: <b>se {p}</b>."
                c.append(mc(3, 'Completar', 'Complete a resposta com os dois pronomes.', s, opts, f"se {p}", x))
            for cl, ans_cl in [("me","te"),("nos","os")]:
                s = f"—¿{cap(cl)} {v['pret'][1]} {np}? —Sí, ya ___ {v['pret'][0]}."
                opts = [f"{ans_cl} {p}", f"{p} {ans_cl}", f"se {p}", f"{ans_cl} le"]
                x = f"Responde-se a ‘tú/vosotros’: {cl} → <b>{ans_cl}</b>. Ordem fixa: OI + OD → <b>{ans_cl} {p}</b>."
                c.append(mc(3, 'Completar', 'Complete a resposta com os dois pronomes.', s, opts, f"{ans_cl} {p}", x))
    out += take(c, 42)
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            p = OD3[gn]
            for rec, pr in REC3:
                head = f"—¿Y {np}? —Ya"
                kind = R.choice(['ok', 'lele', 'order', 'gender'])
                tail = f"{v['pret'][0]} {rec}."
                if kind == 'ok':
                    s = f"{head} se {p} {tail}"; bad = -1
                    x = f"Correto: OI ({rec} → le/les → <b>se</b>) + OD ({np} → <b>{p}</b>)."
                elif kind == 'lele':
                    s = f"{head} {pr} {p} {tail}"; bad = len(head.split(' '))
                    x = f"<i>{pr} {p}</i> não existe: diante de lo/la/los/las, <i>le/les</i> vira <b>se</b> → se {p}."
                elif kind == 'order':
                    s = f"{head} {p} se {tail}"; n0 = len(head.split(' ')); bad = [n0, n0+1]
                    x = f"Ordem invertida. O pronome <i>se</i> (OI) vem sempre <b>antes</b> do OD: se {p}."
                else:
                    w = R.choice([o for o in OD3.values() if o != p])
                    s = f"{head} se {w} {tail}"; bad = len(head.split(' ')) + 1
                    x = f"‘{np}’ é {GN[gn]} → <b>{p}</b>, não <i>{w}</i>."
                fix = f"{head} se {p} {tail}"
                c.append(err(3, s, bad, fix, x))
    out += take(c, 30)
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            p = OD3[gn]
            for subj, i in SUBJ_FOR_12:
                sent = f"{subj} no se {p} {v['pret'][i]}."
                c.append(ordq(3, f"Monte a frase (OD = {np}; OI = outra pessoa, já como pronome).", sent, [f"no se {p} {v['pret'][i]} {subj}"],
                              f"Ordem: no + <b>se</b> (OI) + <b>{p}</b> (OD) + verbo."))
    out += take(c, 18)
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            for subj, i, isp in SUBJ:
                p = OD3[gn]; t = R.choice(['ayer', 'anoche', 'el lunes', 'la semana pasada'])
                s = f"{subj} {v['pret'][i]} [[{np}]] {t}."
                ans = [f"{subj} {p} {v['pret'][i]} {t}."]
                if isp and subj not in ('Usted','Ustedes'): ans.append(cap(f"{p} {v['pret'][i]} {t}."))
                c.append(inp(3, 'Substituir', Q_SUB_OD, s, ans, f"No pretérito a regra é a mesma: pronome (<b>{p}</b>) antes do verbo conjugado."))
    out += take(c, 14)
    return out

# =========================== NÍVEL 4 ===========================
def n4():
    out = []
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            for aux, forms in AUX:
                subj, i, isp = R.choice(SUBJ)
                p = OD3[gn]
                s = f"{subj} {forms[i]} {v['inf']} [[{np}]]."
                ans = [f"{subj} {p} {forms[i]} {v['inf']}.", f"{subj} {forms[i]} {v['inf']}{p}."]
                x = f"Com perífrase (verbo conjugado + infinitivo) há <b>duas</b> posições: antes do verbo conjugado (<i>{p} {forms[i]} {v['inf']}</i>) ou colado ao infinitivo (<i>{forms[i]} {v['inf']}{p}</i>). Infinitivo + 1 pronome não leva acento."
                c.append(inp(4, 'Substituir', Q_SUB_OD + ' (Aceita-se qualquer posição correta.)', s, ans, x))
    out += take(c, 34)
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            subj, i, isp = R.choice(SUBJ)
            p = OD3[gn]
            s = f"{subj} {ESTAR[i]} {v['ger']} [[{np}]]."
            g2 = ger_acc(v['ger']) + p
            ans = [f"{subj} {p} {ESTAR[i]} {v['ger']}.", f"{subj} {ESTAR[i]} {g2}."]
            x = f"Com gerúndio: <i>{p} {ESTAR[i]} {v['ger']}</i> ou <i>{ESTAR[i]} <b>{g2}</b></i>. Ao juntar o pronome, o gerúndio vira proparoxítona e <b>leva acento</b>."
            c.append(inp(4, 'Substituir', Q_SUB_OD + ' (Aceita-se qualquer posição correta.)', s, ans, x))
    out += take(c, 18)
    c = []
    for vk, v in DT.items():
        for np, gn in v['th']:
            for rec, pr in REC3:
                aux, forms = R.choice(AUX[:5])
                subj, i, isp = R.choice(SUBJ3)
                p = OD3[gn]
                s = f"{subj} {forms[i]} {v['inf']}{pr} [[{np}]] [[{rec}]]."
                ia = inf_acc(v['inf'])
                ans = [f"{subj} se {p} {forms[i]} {v['inf']}.", f"{subj} {forms[i]} {ia}se{p}.",
                       f"{subj} se {p} {forms[i]} {v['inf']} {rec}.", f"{subj} {forms[i]} {ia}se{p} {rec}."]
                x = f"Os dois pronomes andam <b>juntos</b>: <i>se {p} {forms[i]} {v['inf']}</i> ou <i>{forms[i]} <b>{ia}se{p}</b></i>. Infinitivo + 2 pronomes leva acento."
                c.append(inp(4, 'Substituir', 'Substitua os dois objetos destacados. (Aceita-se qualquer posição correta.)', s, ans, x))
    out += take(c, 24)
    # imperativo afirmativo tú (OD)
    c = []
    for vk, v in VT.items():
        if not v['imp']: continue
        tu, tu1, neg, ud, ud1 = v['imp']
        for np, gn in v['objs']:
            p = OD3[gn]
            s = f"{cap(tu)} [[{np}]]."
            a = cap(tu1 + p)
            x = f"No imperativo afirmativo o pronome vai <b>depois</b>, colado ao verbo: <b>{a}</b>." + ("" if tu == 'haz' else " A palavra vira proparoxítona → acento.")
            c.append(inp(4, 'Substituir', 'Imperativo: troque o objeto direto pelo pronome.', s, [a + '.'], x))
    out += take(c, 20)
    # imperativo afirmativo com dois pronomes
    c = []
    REC_IMP = [("a Juan","le"),("a tu madre","le"),("a tus padres","les"),("a los niños","les"),("a tu hermana","le"),("a los clientes","les")]
    for vk, v in DT.items():
        tu, tu1, tu2, neg = v['imp'][:4]
        for np, gn in v['th']:
            p = OD3[gn]
            for rec, pr in REC_IMP:
                s = f"{cap(tu1)}{pr} [[{np}]] [[{rec}]]."
                a = cap(f"{tu2}se{p}")
                c.append(inp(4, 'Substituir', 'Imperativo: substitua os dois objetos destacados.', s, [a + '.', f"{a} {rec}."],
                             f"le/les + {p} → se {p}, tudo colado ao imperativo: <b>{a}</b> (com acento)."))
            for cl in ['me', 'nos']:
                s = f"{cap(tu1)}{cl} [[{np}]]."
                a = cap(f"{tu2}{cl}{p}")
                c.append(inp(4, 'Substituir', 'Imperativo: troque o objeto direto pelo pronome.', s, [a + '.'],
                             f"OI ({cl}) + OD ({p}) depois do imperativo: <b>{a}</b>."))
    out += take(c, 24)
    # imperativo negativo
    c = []
    for vk, v in VT.items():
        if not v['imp']: continue
        tu, tu1, neg, ud, ud1 = v['imp']
        for np, gn in v['objs']:
            p = OD3[gn]
            c.append(inp(4, 'Substituir', Q_SUB_OD, f"No {neg} [[{np}]].", [f"No {p} {neg}."],
                         f"No imperativo <b>negativo</b> o pronome volta para <b>antes</b> do verbo: <b>No {p} {neg}</b>."))
    for vk, v in DT.items():
        neg = v['imp'][3]
        for np, gn in v['th']:
            p = OD3[gn]
            rec, pr = R.choice(REC_IMP)
            c.append(inp(4, 'Substituir', 'Substitua os dois objetos destacados.', f"No {pr} {neg} [[{np}]] [[{rec}]].", [f"No se {p} {neg}.", f"No se {p} {neg} {rec}."],
                         f"Negativo: pronomes antes do verbo, OI primeiro: <b>No se {p} {neg}</b>."))
    out += take(c, 18)
    # transformar
    c = []
    for vk, v in DT.items():
        tu, tu1, tu2, neg = v['imp'][:4]
        for np, gn in v['th']:
            p = OD3[gn]
            a = cap(f"{tu2}se{p}")
            c.append(inp(4, 'Transformar', 'Passe para o imperativo negativo.', f"{a}.", [f"No se {p} {neg}."],
                         f"Afirmativo: pronomes depois e colados. Negativo: <b>No se {p} {neg}</b> (pronomes antes, verbo no subjuntivo)."))
            a2 = cap(f"{tu2}me{p}")
            c.append(inp(4, 'Transformar', 'Passe para o imperativo negativo.', f"{a2}.", [f"No me {p} {neg}."],
                         f"<b>No me {p} {neg}</b>."))
    out += take(c, 14)
    # acentuação
    c = []
    def acc_opts(correct, plain_join, spaced):
        noacc = strip_acc(correct)
        opts = [correct]
        if noacc != correct: opts.append(noacc)
        # wrong accent: put accent on last vowel of word
        w = noacc
        for j in range(len(w)-1, -1, -1):
            if w[j] in 'aeio':
                wrong = w[:j] + {'a':'á','e':'é','i':'í','o':'ó'}[w[j]] + w[j+1:]; break
        opts.append(wrong)
        opts.append(spaced)
        return list(dict.fromkeys(opts))[:4]
    for vk, v in DT.items():
        tu, tu1, tu2 = v['imp'][:3]
        for p in ['lo', 'la', 'los']:
            cor = f"{tu2}se{p}"
            c.append(mc(4, 'Ortografia', 'Qual é a grafia correta?', f"Imperativo (tú) de <i>{v['inf']}</i> + se + {p}", acc_opts(cor, None, f"{tu} se {p}"), cor,
                        "Imperativo + 2 pronomes → a sílaba tônica fica na antepenúltima ou antes → <b>acento gráfico</b>."))
        cor = inf_acc(v['inf']) + 'selo'
        c.append(mc(4, 'Ortografia', 'Qual é a grafia correta?', f"Infinitivo <i>{v['inf']}</i> + se + lo", acc_opts(cor, None, f"{v['inf']} se lo"), cor,
                    "Infinitivo + 1 pronome: sem acento (<i>"+v['inf']+"lo</i>). Infinitivo + 2 pronomes: <b>com acento</b>."))
        cor = v['inf'] + 'lo'
        c.append(mc(4, 'Ortografia', 'Qual é a grafia correta?', f"Infinitivo <i>{v['inf']}</i> + lo", [cor, inf_acc(v['inf'])+'lo', v['inf']+'ló', v['inf']+' lo'], cor,
                    "Infinitivo + 1 pronome continua paroxítona terminada em vogal → <b>sem acento</b>."))
        cor = ger_acc(v['ger']) + 'lo'
        c.append(mc(4, 'Ortografia', 'Qual é a grafia correta?', f"Gerúndio <i>{v['ger']}</i> + lo", [cor, v['ger']+'lo', v['ger']+'ló', v['ger']+' lo'], cor,
                    "Gerúndio + pronome vira proparoxítona → <b>acento</b> sempre."))
    out += take(c, 22)
    # duplicação: OD/OI antepostos
    c = []
    for vk, v in VT.items():
        for np, gn in v['objs']:
            p = OD3[gn]
            s = f"{cap(np)} ___ {v['pret'][0]} {R.choice(['ayer','el sábado','esta mañana','hace un rato'])}."
            c.append(mc(4, 'Completar', 'O objeto vem antes do verbo. Complete.', s, ['lo','la','los','las','— (nada)'], p,
                        f"Quando o OD definido vai para o início da frase, é <b>obrigatório</b> retomá-lo com o pronome: {cap(np)} <b>{p}</b> …", shuffle=False))
    for vk, v in DT.items():
        for np, gn in v['th']:
            rec, pr = R.choice(REC3)
            s = f"{cap(rec)} ___ {v['pret'][0]} {np}."
            c.append(mc(4, 'Completar', 'O objeto vem antes do verbo. Complete.', s, ['le','les','lo','la','— (nada)'], pr,
                        f"OI anteposto exige o clítico: {cap(rec)} <b>{pr}</b> …", shuffle=False))
    out += take(c, 18)
    return out

# =========================== NÍVEL 5 ===========================
GUS = [
 ('gustar','gusta','gustan',["el chocolate","bailar","la música clásica"],["las películas de terror","los perros"]),
 ('encantar','encanta','encantan',["viajar","el cine"],["los dulces","las playas del Caribe"]),
 ('interesar','interesa','interesan',["la política","la historia"],["los idiomas","las noticias"]),
 ('molestar','molesta','molestan',["el ruido","madrugar"],["los mosquitos","las mentiras"]),
 ('preocupar','preocupa','preocupan',["el examen","la salud de su madre"],["los precios","las notas"]),
 ('doler','duele','duelen',["la cabeza","la espalda"],["los pies","las muelas"]),
 ('faltar','falta','faltan',["tiempo","un euro"],["dos sillas","tres páginas"]),
 ('apetecer','apetece','apetecen',["un café","salir esta noche"],["unas tapas","las vacaciones"]),
 ('importar','importa','importan',["la opinión de los demás","el dinero"],["los detalles","las formas"]),
 ('quedar','queda','quedan',["poco dinero","una semana"],["dos días","tres galletas"]),
]
EXP = [("A mí","me"),("A ti","te"),("A Juan","le"),("A mi madre","le"),("A nosotros","nos"),("A vosotros","os"),("A mis padres","les"),("A ustedes","les"),("A usted","le"),("A los niños","les")]
SEACC = [
 ('olvidar','olvidó','olvidaron',["el paraguas","la contraseña"],["las llaves","los deberes"]),
 ('caer','cayó','cayeron',["el vaso","la taza"],["las gafas","los platos"]),
 ('romper','rompió','rompieron',["el móvil","la pantalla"],["las gafas","los cordones"]),
 ('perder','perdió','perdieron',["la cartera","el pasaporte"],["los billetes","las entradas"]),
 ('quemar','quemó','quemaron',["la comida","el arroz"],["las tostadas","los macarrones"]),
 ('acabar','acabó','acabaron',["la leche","el dinero"],["las ideas","los ahorros"]),
]
REFL = [
 ('lavarse', ['lavo','lavas','lava','lavamos','laváis','lavan'], 'láva', [("las manos","fp"),("la cara","fs"),("el pelo","ms")]),
 ('ponerse', ['pongo','pones','pone','ponemos','ponéis','ponen'], 'pón', [("el abrigo","ms"),("la chaqueta","fs"),("los guantes","mp"),("las botas","fp")]),
 ('quitarse', ['quito','quitas','quita','quitamos','quitáis','quitan'], 'quíta', [("los zapatos","mp"),("la gorra","fs"),("el jersey","ms")]),
 ('cepillarse', ['cepillo','cepillas','cepilla','cepillamos','cepilláis','cepillan'], 'cepílla', [("los dientes","mp"),("el pelo","ms")]),
 ('secarse', ['seco','secas','seca','secamos','secáis','secan'], 'séca', [("el pelo","ms"),("las manos","fp")]),
 ('probarse', ['pruebo','pruebas','prueba','probamos','probáis','prueban'], 'pruéba', [("el vestido","ms"),("los pantalones","mp"),("la camisa","fs")]),
]
REFLP = ['me','te','se','nos','os','se']
REFL_IMP1 = {'lavarse':'Lávate','ponerse':'Ponte','quitarse':'Quítate','cepillarse':'Cepíllate','secarse':'Sécate','probarse':'Pruébate'}

def n5():
    out = []
    c = []
    for inf, s3, p3, sing, plur in GUS:
        for exp, pr in EXP:
            for thing in sing + plur:
                vb = s3 if thing in sing else p3
                distract = {'me':['mi','se','te'],'te':['ti','se','me'],'le':['les','lo','la'],'les':['le','los','las'],'nos':['os','se','los'],'os':['nos','se','vos']}[pr]
                c.append(mc(5, 'Completar', f'Complete com o pronome (verbo <i>{inf}</i>).', f"{exp} ___ {vb} {thing}.", [pr]+distract, pr,
                            f"Com <i>{inf}</i>, a pessoa afetada é <b>objeto indireto</b> e o pronome é obrigatório mesmo com ‘{exp.lower()}’: <b>{pr}</b>."))
                c.append(mc(5, 'Completar', f'Complete com a forma de <i>{inf}</i> no presente.', f"{exp} {pr} ___ {thing}.", [s3, p3], vb,
                            f"O verbo concorda com o <b>sujeito</b> ‘{thing}’ ({'singular' if vb==s3 else 'plural'}), não com a pessoa → <b>{vb}</b>.", shuffle=False))
    out += take(c, 42)
    c = []
    PERS_SE = [("A mí","me"),("A ti","te"),("A Juan","le"),("A mi madre","le"),("A nosotros","nos"),("A vosotros","os"),("A mis vecinos","les")]
    for inf, s3, p3, sing, plur in SEACC:
        for exp, pr in PERS_SE:
            for thing in sing + plur:
                vb = s3 if thing in sing else p3
                c.append(mc(5, 'Completar', 'Complete (ação involuntária com “se”).', f"{exp} se ___ {vb} {thing}.", [pr, {'me':'mi','te':'ti','le':'lo','nos':'los','os':'vos','les':'los'}[pr], 'se', 'lo'], pr,
                            f"Estrutura <i>se + OI + verbo</i>: o <i>se</i> marca o acidente e <b>{pr}</b> indica a pessoa afetada. O verbo concorda com ‘{thing}’."))
                good = R.random() < 0.3
                if good:
                    s = f"Se {pr} {vb} {thing}."; bad = -1; x = "Correto: ordem fixa <b>se</b> + pronome pessoal."
                else:
                    s = f"{cap(pr)} se {vb} {thing}."; bad = [0, 1]; x = f"Ordem errada: <i>se</i> vem sempre primeiro → <b>Se {pr} {vb}…</b> (‘{cap(pr)} se’ é vulgarismo)."
                c.append(err(5, s, bad, f"Se {pr} {vb} {thing}.", x))
    out += take(c, 22)
    c = []
    SUBJR = [("Yo",0,True),("Tú",1,True),("Juan",2,False),("Nosotros",3,True),("Vosotros",4,True),("Mis hijos",5,False),("Ana",2,False)]
    for inf, conj, imp2, objs in REFL:
        for np, gn in objs:
            p = OD3[gn]
            for subj, i, isp in SUBJR:
                s = f"{subj} {REFLP[i]} {conj[i]} [[{np}]]."
                ans = [f"{subj} {REFLP[i]} {p} {conj[i]}."]
                if isp: ans.append(cap(f"{REFLP[i]} {p} {conj[i]}."))
                c.append(inp(5, 'Substituir', Q_SUB_OD, s, ans,
                             f"O reflexivo (<i>{REFLP[i]}</i>) funciona como OI e vem primeiro: <b>{REFLP[i]} {p}</b>. Repare que em espanhol se diz ‘{np}’ e não ‘mis/sus…’ — o reflexivo já indica o dono."))
            a = cap(f"{imp2}te{p}")
            c.append(inp(5, 'Substituir', 'Imperativo: troque o objeto direto pelo pronome.', f"{REFL_IMP1[inf]} [[{np}]].", [a + '.'],
                         f"te (reflexivo) + {p}, colados ao imperativo e com acento: <b>{a}</b>."))
    out += take(c, 26)
    out += hand5()
    return out

def H(lv, k, s, opts, x, q='Escolha a opção correta.', fixed=False):
    return mc(lv, k, q, s, opts, opts[0], x, shuffle=not fixed)

def hand5():
    L = []
    A = L.append
    A(H(5,'Completar',"—¿Sabes a qué hora llega el tren? —No, no ___ sé.",["lo","la","le","— (nada)"],"O pronome retoma uma ideia inteira, não um substantivo → <b>lo neutro</b>."))
    A(H(5,'Completar',"—¿Es verdad que Marta se casa? —Sí, me ___ dijo ayer.",["lo","la","le","las"],"‘que Marta se casa’ é uma oração → lo neutro. <i>me</i> (OI) + <i>lo</i> (OD)."))
    A(H(5,'Completar',"No ___ creo: es imposible que haya aprobado sin estudiar.",["lo","la","le","se"],"<b>lo</b> neutro retoma o que foi dito antes."))
    A(H(5,'Completar',"Que estás cansado, ya ___ sé.",["lo","le","te","la"],"Oração anteposta (‘Que estás cansado’) retomada por <b>lo</b>."))
    A(H(5,'Completar',"Todo ___ sé ya; no hace falta que me lo cuentes.",["lo","— (nada)","le","se"],"Com <i>todo</i> como OD <b>antes</b> do verbo, o clítico é obrigatório: Todo <b>lo</b> sé."))
    A(H(5,'Completar',"Esas llaves ___ encontré debajo del sofá.",["las","— (nada)","les","la"],"OD definido no início da frase exige retomada: Esas llaves <b>las</b> encontré."))
    A(H(5,'Completar',"A tu hermano no ___ he visto hoy.",["lo","— (nada)","la","se"],"OD de pessoa anteposto exige clítico. <i>lo</i> é o recomendado (<i>le</i> seria leísmo admitido)."))
    A(H(5,'Completar',"Dinero no ___ tengo, pero tiempo sí.",["— (nada)","lo","le","la"],"Substantivo <b>sem determinante</b> anteposto (dinero, pan, tiempo) não leva clítico: Dinero no tengo."))
    A(H(5,'Completar',"Pan no ___ compré, pero traje fruta.",["— (nada)","lo","le","la"],"Nome sem artigo anteposto → sem pronome de retomada."))
    A(H(5,'Completar',"El pan ___ compré yo, no tu hermano.",["lo","— (nada)","le","la"],"Com artigo (<i>el pan</i>), a retomada é obrigatória: El pan <b>lo</b> compré yo."))
    A(H(5,'Completar',"A mí no ___ interesa la política.",["me","mi","le","se"],"Com pronome tônico (a mí, a ti…) o clítico é obrigatório: A mí <b>me</b> interesa."))
    A(H(5,'Completar',"—¿A quién le diste las llaves, a Juan o a Ana? —Se ___ di a ella.",["las","les","la","los"],"OD ‘las llaves’ → <b>las</b>; OI ‘a Ana’ → le → <b>se</b>. ‘a ella’ desfaz a ambiguidade de <i>se</i>."))
    A(H(5,'Escolher',"",["Me lo dieron a mí.","Lo dieron a mí.","Dieron lo a mí.","Lo me dieron a mí."],"Com <i>a mí</i> (pronome tônico) o clítico <i>me</i> é obrigatório, e a ordem é OI + OD: <b>Me lo dieron a mí</b>.",q="Qual frase está correta?"))
    A(H(5,'Escolher',"",["Esa película la vi el sábado.","Esa película vi el sábado.","Esa película le vi el sábado.","La esa película vi el sábado."],"OD definido anteposto → pronome obrigatório: Esa película <b>la</b> vi.",q="Qual frase soa natural e correta?"))
    A(H(5,'Norma RAE',"A Juan le vi ayer en el cine.",["Aceita (leísmo admitido com homem no singular), mas o recomendado é ‘lo vi’","Incorreta em qualquer variedade","A única forma correta","Um caso de laísmo"],"O DPD admite <i>le</i> como OD quando o referente é <b>pessoa do sexo masculino no singular</b>. Ainda assim recomenda <i>lo</i>.",q="Segundo a norma da RAE, a frase é:"))
    A(H(5,'Norma RAE',"A María le vi ayer en el cine.",["Incorreta: leísmo com feminino; o certo é ‘la vi’","Aceita como leísmo de pessoa","Correta porque María é OI","Um caso de loísmo"],"O leísmo admitido vale só para masculino singular. Com mulher: <b>la vi</b>.",q="Segundo a norma da RAE, a frase é:"))
    A(H(5,'Norma RAE',"A mis primos les invité a la boda.",["Desaconselhada: leísmo no plural; prefira ‘los invité’","Correta e recomendada","Laísmo","Loísmo"],"O leísmo no plural (<i>les</i> por <i>los</i>) é bem menos aceito; a RAE recomenda evitá-lo.",q="Segundo a norma da RAE, a frase é:"))
    A(H(5,'Norma RAE',"Le saludo atentamente, señora García.",["Aceita: leísmo de cortesia com ‘usted’","Incorreta: só ‘la saludo’ é possível","Laísmo","Correta porque ‘señora’ é OI"],"Com <i>usted</i>, o <i>le</i> como OD é tradicional e aceito mesmo para mulheres (leísmo de cortesia). <i>La saludo</i> também é correto.",q="Segundo a norma da RAE, a frase é:"))
    A(H(5,'Norma RAE',"Se le considera el mejor cirujano del país.",["Correta: com ‘se’ impessoal, ‘le’ é a forma mais usada e aceita","Incorreta: deve ser ‘se lo considera’ obrigatoriamente","Laísmo","Erro de concordância"],"Nas orações impessoais com <i>se</i>, <i>le/les</i> como OD de pessoa masculina é majoritário e aceito; <i>se lo</i> aparece em partes da América.",q="Segundo a norma da RAE, a frase é:"))
    A(H(5,'Norma RAE',"El libro le dejé encima de la mesa.",["Incorreta: leísmo com coisa; o certo é ‘lo dejé’","Correta: leísmo admitido","Correta: ‘libro’ é OI","Laísmo"],"O leísmo admitido vale só para <b>pessoas</b> do sexo masculino. Com coisas: <b>lo</b>.",q="Segundo a norma da RAE, a frase é:"))
    A(H(5,'Norma RAE',"Al perro le saqué a pasear esta mañana.",["Desaconselhada: com animais o normativo é ‘lo saqué’","Correta e recomendada","Laísmo","Loísmo"],"O leísmo admitido não se estende a animais: <b>lo saqué</b>.",q="Segundo a norma da RAE, a frase é:"))
    # verbos OD x OI
    A(H(5,'Completar',"—¿Llamaste a Marta? —Sí, ___ llamé ayer.",["la","le","lo","se"],"<i>Llamar</i> (telefonar) é transitivo: a pessoa é OD → <b>la</b>."))
    A(H(5,'Completar',"—¿Ayudaste a tu madre? —Sí, ___ ayudé con la cena.",["la","le","lo","les"],"<i>Ayudar</i> é transitivo: a pessoa é OD → <b>la</b>. (<i>Le ayudé</i> é leísmo, só admitido com masculino.)"))
    A(H(5,'Completar',"—¿Pagaste al fontanero? —Sí, ya ___ pagué.",["le","lo","la","se"],"<i>Pagar algo a alguien</i>: o que se paga é OD; <b>a quem</b> se paga é OI → <b>le</b>."))
    A(H(5,'Completar',"—¿Esperaste a Lucía? —Sí, ___ esperé dos horas.",["la","le","lo","les"],"<i>Esperar a alguien</i>: OD → <b>la</b>."))
    A(H(5,'Completar',"—¿Le robaron algo a tu padre? —Sí, ___ robaron la cartera.",["le","lo","la","les"],"<i>Robar algo a alguien</i>: a vítima é OI → <b>le</b>; a coisa roubada é OD."))
    A(H(5,'Completar',"—¿Preguntaste la dirección al policía? —Sí, se ___ pregunté.",["la","le","lo","las"],"OD ‘la dirección’ → <b>la</b>; OI ‘al policía’ → se."))
    A(H(5,'Completar',"—¿Escuchas a tus profesores? —Sí, ___ escucho siempre.",["los","les","las","le"],"<i>Escuchar a alguien</i>: OD → <b>los</b>."))
    A(H(5,'Completar',"___ lavé la cara al niño antes de salir.",["Le","Lo","Su","Se"],"Com partes do corpo o espanhol usa artigo + OI do possuidor (dativo possessivo): <b>Le</b> lavé la cara."))
    A(H(5,'Escolher',"",["Me duele la cabeza.","Me duele mi cabeza.","Duele mi cabeza.","Mi cabeza me duele mía."],"Com partes do corpo, o dono vai no pronome (<i>me</i>) e o substantivo leva artigo: <b>Me duele la cabeza</b>.",q="Qual é a forma natural?"))
    A(H(5,'Completar',"A mi padre ___ robaron el coche anoche.",["le","lo","su","se"],"Dativo possessivo/afetado: <b>le</b> robaron el coche (= o carro dele)."))
    E = [
     ("La dije a mi hermana que viniera.", 0, "Le dije a mi hermana que viniera.", "<b>Laísmo</b>: ‘a mi hermana’ é OI (dizer algo <i>a</i> alguém) → <b>le</b>."),
     ("A Marta la duele la cabeza.", 2, "A Marta le duele la cabeza.", "<i>Doler</i> funciona como <i>gustar</i>: a pessoa é OI → <b>le</b>."),
     ("Lo di un abrazo a mi abuelo.", 0, "Le di un abrazo a mi abuelo.", "<b>Loísmo</b>: o OD é ‘un abrazo’; o avô é OI → <b>le</b>."),
     ("Los escribí una carta a mis tíos.", 0, "Les escribí una carta a mis tíos.", "<b>Loísmo</b>: ‘a mis tíos’ é OI → <b>les</b>."),
     ("La regalé flores a mi novia.", 0, "Le regalé flores a mi novia.", "<b>Laísmo</b>: ‘a mi novia’ recebe → OI → <b>le</b>."),
     ("A las niñas les vi en el parque.", 3, "A las niñas las vi en el parque.", "Leísmo com feminino não é admitido: ‘a las niñas’ é OD → <b>las</b>."),
     ("A mi madre la encanta el cine.", 3, "A mi madre le encanta el cine.", "<i>Encantar</i> pede OI → <b>le</b>."),
     ("La pegó una bofetada sin motivo.", 0, "Le pegó una bofetada sin motivo.", "O OD é ‘una bofetada’; a pessoa que recebe é OI → <b>le</b>."),
     ("Le dije a mis padres la verdad.", 0, "Les dije a mis padres la verdad.", "Concordância: OI plural (‘a mis padres’) → <b>les</b>."),
     ("¿Las has dado las llaves a tus vecinas?", 0, "¿Les has dado las llaves a tus vecinas?", "OD = las llaves; ‘a tus vecinas’ é OI → <b>Les</b>."),
     ("A Laura le duele la espalda desde ayer.", -1, "A Laura le duele la espalda desde ayer.", "Correto: com <i>doler</i> a pessoa é OI → le."),
     ("A Pedro lo vi ayer en la playa.", -1, "A Pedro lo vi ayer en la playa.", "Correto: OD de pessoa anteposto retomado por <i>lo</i>."),
     ("A mis abuelos les escribo cada semana.", -1, "A mis abuelos les escribo cada semana.", "Correto: escrever <i>a</i> alguém → OI → les."),
     ("Lo pregunté la hora a un señor.", 0, "Le pregunté la hora a un señor.", "<b>Loísmo</b>: a hora é OD; o senhor é OI → <b>le</b>."),
     ("A mí me lo contó Juan.", -1, "A mí me lo contó Juan.", "Correto: duplicação obrigatória com <i>a mí</i>."),
     ("Esa canción la escuché ayer.", -1, "Esa canción la escuché ayer.", "Correto: OD anteposto retomado por <i>la</i>."),
     ("A Juan le gustan mucho los perros.", -1, "A Juan le gustan mucho los perros.", "Correto: <i>gustan</i> concorda com ‘los perros’."),
     ("A mis hermanos le encanta el fútbol.", 3, "A mis hermanos les encanta el fútbol.", "OI plural → <b>les</b>."),
     ("A nosotros nos gusta los conciertos.", 3, "A nosotros nos gustan los conciertos.", "O verbo concorda com o sujeito ‘los conciertos’ → <b>gustan</b>."),
     ("Se los di a Juan ayer (el libro).", 1, "Se lo di a Juan ayer (el libro).", "‘el libro’ é singular → <b>lo</b>. O <i>se</i> não indica número."),
    ]
    for s, b, f, x in E:
        L.append(err(5, s, b, f, x))
    return L

# =========================== NÍVEL 6 ===========================
def n6():
    out = []
    c = []
    ATR = [("¿Están cansadas tus hermanas?","están","fp"),("¿Es médico tu padre?","es","ms"),("¿Son simpáticos tus amigos?","son","mp"),
           ("¿Está lista Ana?","está","fs"),("¿Parecen contentas las niñas?","parecen","fp"),("¿Son ruidosos los vecinos?","son","mp"),
           ("¿Es abogada tu madre?","es","fs"),("¿Está caliente la sopa?","está","fs"),("¿Son altos los precios?","son","mp"),
           ("¿Es grande la casa?","es","fs"),("¿Están listas las maletas?","están","fp"),("¿Parece fácil el examen?","parece","ms"),
           ("¿Son tuyas estas gafas?","son","fp"),("¿Está enfadado tu jefe?","está","ms"),("¿Eran profesoras tus tías?","eran","fp")]
    for qs, vb, gn in ATR:
        resp = 'No, no ___ ' + vb + '.' if R.random() < .4 else 'Sí, ___ ' + vb + '.'
        c.append(mc(6, 'Completar', 'Complete. (Atenção: retomada de atributo.)', f"—{qs} —{resp}", ['lo', OD3[gn], 'le', 'se'], 'lo',
                    f"Com <i>ser, estar, parecer</i>, o pronome retoma o <b>atributo</b> e é sempre o neutro invariável <b>lo</b>, qualquer que seja o gênero ou número: {resp.replace('___','lo')}"))
        w = OD3[gn] if OD3[gn] != 'lo' else 'la'
        c.append(err(6, f"—{qs} —Sí, {w} {vb}.", len(f"—{qs} —Sí,".split(' ')), f"—{qs} —Sí, lo {vb}.",
                     f"Atributo → <b>lo</b> neutro, nunca concordando com o sujeito."))
    out += take(c, 20)
    # subida de clíticos
    c = []
    for vk, v in DT.items():
        for np, gn in v['th'][:3]:
            p = OD3[gn]
            aux, forms = R.choice(AUX[:5])
            i = R.choice([0, 1, 2, 3])
            a = forms[i]; inf = v['inf']; ia = inf_acc(inf)
            good = [f"Se {p} {a} {inf}.", cap(f"{a} {ia}se{p}.")]
            bad = [f"Se {a} {inf}{p}.", cap(f"{p} {a} {inf}le."), cap(f"{a} se {p} {inf}.")]
            ok = R.choice(good)
            c.append(mc(6, 'Escolher', 'Qual frase está CORRETA? (OD = ' + np + '; OI = a él)', '', [ok] + bad, ok,
                        "Os clíticos são um <b>bloco inseparável</b>: ou sobem juntos para antes do verbo conjugado, ou ficam juntos depois do infinitivo. Nunca se dividem nem ficam entre os verbos."))
            wrong = R.choice(bad)
            c.append(mc(6, 'Escolher', 'Qual frase está INCORRETA? (OD = ' + np + '; OI = a él)', '', [wrong] + good + [f"No se {p} {a} {inf}."], wrong,
                        "Pronomes não se separam: <i>se lo</i> vai inteiro antes do verbo conjugado ou inteiro colado ao infinitivo."))
    out += take(c, 22)
    # nosotros / vosotros / usted
    c = []
    RECN = [("a Juan","le"),("a los alumnos","les"),("a la directora","le"),("a nuestros padres","les")]
    for vk, v in DT.items():
        tu, tu1, tu2, neg, ud, ud1, ud2, nos, nosa, vos, vos2 = v['imp']
        np, gn = R.choice(v['th']); p = OD3[gn]
        rec, pr = R.choice(RECN)
        a = cap(f"{nosa[:-1]}se{p}")
        c.append(inp(6, 'Substituir', 'Imperativo de <i>nosotros</i>: substitua os dois objetos.', f"{cap(nos)} [[{np}]] [[{rec}]].", [a + '.', f"{a} {rec}."],
                     f"<i>{nos}</i> + se + {p}: o <b>-s final cai</b> diante de <i>se</i> (não se escreve ‘-mossse’) e a palavra leva acento: <b>{a}</b>."))
        a1 = cap(f"{nosa}{p}")
        c.append(inp(6, 'Substituir', 'Imperativo de <i>nosotros</i>: troque o OD pelo pronome.', f"{cap(nos)} [[{np}]].", [a1 + '.'],
                     f"Com um só pronome (lo/la) o -s se mantém: <b>{a1}</b>."))
        c.append(mc(6, 'Ortografia', 'Qual é a grafia correta?', f"Imperativo de <i>nosotros</i> de <i>{v['inf']}</i> + se + {p}",
                    [cap(f"{nosa[:-1]}se{p}"), cap(f"{nosa}se{p}"), cap(strip_acc(f"{nosa[:-1]}se{p}")), cap(f"{nos} se {p}")], cap(f"{nosa[:-1]}se{p}"),
                    "Diante de <i>se</i> cai o -s de <i>-mos</i>; e a forma leva acento."))
        np2, gn2 = R.choice(v['th']); p2 = OD3[gn2]
        a = cap(f"{vos2}se{p2}")
        c.append(inp(6, 'Substituir', 'Imperativo de <i>vosotros</i>: substitua os dois objetos.', f"{cap(vos)}le [[{np2}]] [[a Juan]].", [a + '.', f"{a} a Juan."],
                     f"<i>{vos}</i> + se + {p2} → <b>{a}</b> (o -d se mantém; com dois pronomes, acento)."))
        a1 = cap(f"{vos}{p2}")
        c.append(inp(6, 'Substituir', 'Imperativo de <i>vosotros</i>: troque o OD pelo pronome.', f"{cap(vos)} [[{np2}]].", [a1 + '.'],
                     f"<i>{vos}</i> + {p2} → <b>{a1}</b>: paroxítona terminada em vogal, sem acento."))
        np3, gn3 = R.choice(v['th']); p3 = OD3[gn3]
        a = cap(f"{ud2}se{p3}")
        c.append(inp(6, 'Substituir', 'Imperativo de <i>usted</i>: substitua os dois objetos.', f"{cap(ud1)}le [[{np3}]] [[a su hijo]].", [a + '.', f"{a} a su hijo."],
                     f"<i>{ud}</i> + se + {p3} → <b>{a}</b>."))
        a1 = cap(f"{ud1}{p3}")
        c.append(inp(6, 'Substituir', 'Imperativo de <i>usted</i>: troque o OD pelo pronome.', f"{cap(ud)} [[{np3}]].", [a1 + '.'],
                     f"<i>{ud}</i> + {p3} → <b>{a1}</b>." + (" O acento diacrítico de <i>dé</i> desaparece ao juntar um só pronome (delo, dele, deme)." if vk == 'dar' else "")))
    out += take(c, 40)
    out += hand6()
    return out

def hand6():
    L = []; A = L.append
    A(H(6,'Escolher',"",["Se me olvidó.","Me se olvidó.","Se olvidó me.","Me olvidó se."],"Ordem fixa dos clíticos: <b>se</b> › 2ª pessoa › 1ª pessoa › 3ª pessoa. ‘Me se’ é vulgarismo.",q="Qual é a ordem correta?"))
    A(err(6,"Te se cayó el vaso.",[0,1],"Se te cayó el vaso.","<i>se</i> sempre vem antes: <b>Se te</b> cayó."))
    A(err(6,"No te me pongas nervioso.",-1,"No te me pongas nervioso.","Correto: <i>te</i> (reflexivo de ponerse) + <i>me</i> (dativo ético). Ordem: 2ª antes de 1ª pessoa."))
    A(H(6,'Identificar',"No te me pongas nervioso.",["Dativo ético (envolvimento afetivo do falante)","Objeto direto","Objeto indireto que recebe algo","Pronome reflexivo"],"Esse <i>me</i> não é exigido pelo verbo: expressa o interesse/afeto do falante — <b>dativo ético</b>.",q="Qual a função de <i>me</i>?"))
    A(H(6,'Identificar',"Mi hijo no me come nada.",["Dativo ético (envolvimento afetivo do falante)","Objeto direto","Objeto indireto que recebe algo","Pronome reflexivo"],"A mãe/pai não é comido nem recebe nada: <i>me</i> mostra que o falante se sente afetado → <b>dativo ético</b>.",q="Qual a função de <i>me</i>?"))
    A(H(6,'Identificar',"Juan se comió toda la pizza.",["Dativo aspectual/de interesse (ênfase na ação completa)","Reflexivo (Juan come a si mesmo)","Passiva reflexa","Impessoal"],"<i>Comerse, beberse, leerse…</i> com OD quantificado: o <i>se</i> reforça a ação total → valor <b>aspectual</b>.",q="Qual a função de <i>se</i>?"))
    A(H(6,'Identificar',"Se venden pisos en el centro.",["Passiva reflexa","Reflexivo","Variante de ‘le’ (OI)","Dativo ético"],"‘pisos’ é sujeito (o verbo concorda: <i>venden</i>) → <b>passiva reflexa</b>.",q="Qual a função de <i>se</i>?"))
    A(H(6,'Identificar',"Se lo di a Juan.",["Variante de ‘le’ (OI) diante de ‘lo’","Reflexivo","Passiva reflexa","Impessoal"],"<i>le</i> + <i>lo</i> → <b>se lo</b>: aqui <i>se</i> é o OI (a Juan).",q="Qual a função de <i>se</i>?"))
    A(H(6,'Identificar',"Aquí se vive muy bien.",["Impessoal","Passiva reflexa","Reflexivo","Variante de ‘le’"],"Não há sujeito nem OD: <b>se impessoal</b> (‘vive-se’).",q="Qual a função de <i>se</i>?"))
    A(H(6,'Identificar',"Se me cayeron las gafas.",["Objeto indireto (pessoa afetada pelo acidente)","Objeto direto","Sujeito","Reflexivo"],"Em <i>se + OI + verbo</i>, o <i>me</i> indica quem sofre o acidente; ‘las gafas’ é o sujeito.",q="Qual a função de <i>me</i>?"))
    A(H(6,'Escolher',"",["Lo insisto en hacer.","Insisto en hacerlo.","Lo acabo de hacer.","Lo vuelvo a intentar."],"A subida do clítico só acontece com auxiliares/perífrases (ir a, acabar de, volver a, tener que, poder, querer…). <i>Insistir en</i> bloqueia: <b>Insisto en hacerlo</b>.",q="Qual frase está INCORRETA?"))
    A(H(6,'Escolher',"",["Lo pienso en hacer.","Pienso en hacerlo.","Lo pienso hacer.","Pienso hacerlo."],"<i>Pensar</i> (= pretender) + infinitivo permite subida: <i>Lo pienso hacer</i>. Mas com a preposição <i>en</i> não: <b>Pienso en hacerlo</b>.",q="Qual frase está INCORRETA?"))
    A(H(6,'Escolher',"",["He lo visto.","Lo he visto.","Lo había visto.","Lo habrá visto."],"Nos tempos compostos o pronome vai <b>antes do auxiliar haber</b>: Lo he visto. Nunca entre <i>haber</i> e o particípio.",q="Qual frase está INCORRETA?"))
    A(H(6,'Ortografia',"Gerúndio composto de <i>ver</i> + lo",["Habiéndolo visto","Lo habiendo visto","Habiendo vistolo","Habiendolo visto"],"No gerúndio composto o pronome se junta a <i>habiendo</i> (com acento): <b>habiéndolo visto</b>.",q="Qual é a forma correta?"))
    A(H(6,'Escolher',"",["Hay que hacerlo.","Lo hay que hacer.","Hay que lo hacer.","Hay lo que hacer."],"Com <i>hay que</i> a forma padrão é o pronome no infinitivo: <b>hay que hacerlo</b>. <i>Lo hay que hacer</i> se ouve na fala, mas é menos recomendada.",q="Qual é a forma padrão recomendada?"))
    A(inp(6,'Substituir',"Troque o objeto destacado pelo pronome.","Hice reír [[a los niños]].",["Los hice reír."],"Sem OD próprio do infinitivo, quem é ‘feito fazer’ é <b>OD</b> → <b>los</b>, que sobe para antes de <i>hice</i>."))
    A(H(6,'Completar',"___ hice leer el libro a los niños.",["Les","Los","Las","Se"],"Quando o infinitivo tem <b>OD próprio</b> (el libro), o causado passa a <b>OI</b> → <b>les</b>.",q="Complete (construção causativa)."))
    A(inp(6,'Substituir',"Substitua os dois objetos destacados.","Hice leer [[el libro]] [[a los niños]].",["Se lo hice leer.","Se lo hice leer a los niños."],"OI (les → se) + OD (lo), ambos antes de <i>hice</i>: <b>Se lo hice leer</b>."))
    A(inp(6,'Substituir',"Troque o objeto destacado pelo pronome.","Dejé salir [[a mi hija]].",["La dejé salir."],"Causado sem OD próprio → OD → <b>la</b>."))
    A(inp(6,'Substituir',"Troque o objeto destacado pelo pronome.","Mandé arreglar [[el coche]].",["Lo mandé arreglar."],"O OD de <i>arreglar</i> sobe para antes de <i>mandé</i>: <b>Lo mandé arreglar</b>."))
    A(inp(6,'Substituir',"Troque o objeto destacado pelo pronome.","Vi entrar [[a Pedro]] en el bar.",["Lo vi entrar en el bar.","Le vi entrar en el bar."],"Com verbos de percepção + infinitivo sem OD, o percebido é OD: <b>Lo vi entrar</b> (<i>le</i>: leísmo admitido)."))
    A(H(6,'Completar',"___ ve muy feliz a Juan desde que cambió de trabajo.",["Se le","Se lo","Le se","Lo se"],"Impessoal com <i>se</i> + OD de pessoa masculina: <b>se le</b> é o uso majoritário (em parte da América: <i>se lo</i>). A ordem é sempre <i>se</i> primeiro.",q="Complete."))
    A(H(6,'Completar',"A los presos ___ trasladó a otra cárcel.",["se les","se los","les se","los se"],"Impessoal com <i>se</i>: predomina <b>se les</b> para pessoas.",q="Complete."))
    A(H(6,'Interpretar',"Díjole el rey que se marchara.",["Le dijo","Lo dijo","Se dijo","Dijo a él (sem pronome)"],"Pronome depois de verbo conjugado é <b>arcaico/literário</b>. Hoje: <i>Le dijo el rey…</i>",q="Na prosa antiga, ‘díjole’ equivale a:"))
    A(H(6,'Norma RAE',"",["O normativo é ‘Ya se lo dije’ (lo = eso; se = a ustedes)","O normativo é ‘Ya les los dije’","‘Se los dije’ é a única forma correta","O normativo é ‘Ya los se dije’"],"Como <i>se</i> não marca plural, muitos falantes transferem o plural para o OD (‘se los’). É muito difundido na América, mas a norma culta mantém <b>se lo</b> quando o OD é singular.",q="Na América ouve-se ‘Ya se los dije’ (= já disse isso a vocês). Pela norma culta:"))
    A(H(6,'Completar',"A Ana ___ preocupa mucho el examen de mañana.",["le","la","lo","se"],"Verbos de afeto com sujeito inanimado e sem intenção (preocupar, molestar, asustar…) tomam a pessoa como <b>OI</b> → <b>le</b>."))
    A(H(6,'Completar',"(A Ana) Juan ___ asustó a propósito, escondido detrás de la puerta.",["la","le","lo","se"],"Com sujeito <b>agente</b> e ação intencional, o verbo de afeto é transitivo: a pessoa é <b>OD</b> → <b>la</b>."))
    A(H(6,'Completar',"Ojalá ___ hubieras dicho antes (eso, a mí).",["me lo","lo me","me le","se me"],"OI + OD: <b>me lo</b>, antes do auxiliar <i>hubieras</i>."))
    A(H(6,'Ortografia',"",["Quiero ponérmelo.","Quiero ponermelo.","Quiero ponermélo.","Quiero pónermelo."],"Infinitivo + 2 pronomes → acento na sílaba tônica do infinitivo: <b>ponérmelo</b>.",q="Qual é a grafia correta?"))
    A(H(6,'Ortografia',"<i>Dé</i> (usted) + lo",["Delo","Délo","Dé lo","Dello"],"Ao juntar um só pronome, <i>dé</i> forma uma paroxítona terminada em vogal e perde o acento: <b>delo, dele, deme</b>. Com dois: <i>déselo, démelo</i>.",q="Qual é a grafia correta?"))
    A(H(6,'Ortografia',"Imperativo de <i>estarse</i> (usted): ‘___ quieto, por favor.’",["Estese","Estése","Esté se","Estésse"],"<i>esté</i> + se → <b>estese</b>: paroxítona terminada em vogal, sem acento.",q="Qual é a grafia correta?"))
    A(H(6,'Ortografia',"Imperativo de <i>sentarse</i> (nosotros)",["Sentémonos","Sentémosnos","Sentemonos","Sentamosnos"],"Diante de <i>nos</i> cai o -s de <i>-mos</i>: <b>sentémonos</b> (e leva acento).",q="Qual é a forma correta?"))
    A(H(6,'Ortografia',"Imperativo de <i>irse</i> (nosotros)",["Vámonos","Vámosnos","Vamosnos","Vamonós"],"<i>vamos</i> + nos → cai o -s: <b>vámonos</b>.",q="Qual é a forma correta?"))
    A(H(6,'Ortografia',"Imperativo de <i>sentarse</i> (vosotros)",["Sentaos","Sentados","Sentaros","Sentados os"],"Diante de <i>os</i> cai o -d: <b>sentaos</b>. <i>Sentaros</i> (infinitivo) é muito comum na fala, mas não é a forma normativa.",q="Qual é a forma normativa?"))
    A(H(6,'Ortografia',"<i>Poneos</i> (vosotros) + el abrigo → pronome",["Ponéoslo","Poneoslo","Ponedoslo","Poneroslo"],"<i>poneos</i> + lo → <b>ponéoslo</b>: a tônica cai na antepenúltima sílaba → acento.",q="Qual é a forma correta?"))
    A(inp(6,'Substituir',"Imperativo: substitua os dois objetos destacados.","Ponle [[el abrigo]] [[al niño]].",["Pónselo.","Pónselo al niño."],"<i>pon</i> + se + lo → <b>pónselo</b> (com dois pronomes até o monossílabo leva acento)."))
    A(inp(6,'Substituir',"Imperativo: substitua os dois objetos destacados.","Hazle [[la cena]] [[a tu padre]].",["Házsela.","Házsela a tu padre."],"<i>haz</i> + se + la → <b>házsela</b>."))
    A(inp(6,'Substituir',"Imperativo: substitua os dois objetos destacados.","Dile [[la verdad]] [[a tu madre]].",["Dísela.","Dísela a tu madre."],"<i>di</i> + se + la → <b>dísela</b>."))
    A(H(6,'Completar',"Parece fácil, pero no ___ es.",["lo","la","le","se"],"Retoma o atributo ‘fácil’ → <b>lo</b> neutro."))
    A(H(6,'Completar',"Mis vecinos son simpáticos, pero sus hijos no ___ son.",["lo","los","les","se"],"Atributo retomado → <b>lo</b>, mesmo com sujeito plural."))
    A(H(6,'Completar',"—¿Está lista la cena? —Ya casi ___ está.",["lo","la","le","se"],"Atributo (‘lista’) → <b>lo</b>."))
    A(H(6,'Escolher',"",["Se lo quiero regalar a ella.","Lo se quiero regalar a ella.","Se quiero regalarlo a ella.","Quiero se lo regalar a ella."],"Bloco <i>se lo</i> inteiro antes do verbo conjugado (ou inteiro no infinitivo: <i>quiero regalárselo</i>).",q="Qual frase está correta?"))
    A(H(6,'Escolher',"",["Quiero empezar a leerlo.","Quiero empezar lo a leer.","Quiero lo empezar a leer.","Quiero empezar a lo leer."],"O pronome nunca fica solto entre verbos: vai colado ao último infinitivo (<i>leerlo</i>) ou antes do verbo conjugado (<i>Lo quiero empezar a leer</i>).",q="Qual frase está correta?"))
    A(H(6,'Escolher',"",["Lo quiero empezar a leer.","Quiero lo empezar a leer.","Quiero empezar a lo leer.","Quiero empezar lo a leer."],"Com cadeia de perífrases, o pronome pode subir até o verbo conjugado: <b>Lo quiero empezar a leer</b>.",q="Qual frase está correta?"))
    A(err(6,"Se lo voy a decirle mañana.",[4],"Se lo voy a decir mañana.","O OI já está em <i>se</i>; o <i>-le</i> repete o mesmo objeto. Clíticos não se duplicam entre si: <b>Se lo voy a decir</b>."))
    A(err(6,"Me lo dieron a mí y a mi hermano.",-1,"Me lo dieron a mí y a mi hermano.","Correto (embora ‘nos lo dieron a mí y a mi hermano’ também seja possível)."))
    A(err(6,"Les compré un regalo a los niños.",-1,"Les compré un regalo a los niños.","Correto: OI plural duplicado."))
    A(err(6,"A ese señor no le conozco de nada.",-1,"A ese señor no le conozco de nada.","Aceito: leísmo de pessoa masculina singular (admitido). O recomendado seria <i>lo conozco</i>."))
    A(err(6,"A esas chicas no les conozco de nada.",4,"A esas chicas no las conozco de nada.","Leísmo com feminino plural não é admitido: OD → <b>las</b>."))
    A(err(6,"Dígaselo usted a sus clientes.",-1,"Dígaselo usted a sus clientes.","Correto: <i>diga</i> + se + lo, com acento."))
    A(err(6,"Digámossela ahora mismo.",0,"Digámosela ahora mismo.","Diante de <i>se</i> cai o -s: <b>digámosela</b>."))
    A(err(6,"Dádselo a vuestro hermano.",-1,"Dádselo a vuestro hermano.","Correto: <i>dad</i> + se + lo com acento."))
    A(err(6,"Me se ha roto el móvil.",[0,1],"Se me ha roto el móvil.","Ordem: <b>se</b> antes de <i>me</i>."))
    A(err(6,"Les los di a mis primos.",[0],"Se los di a mis primos.","<i>les</i> diante de <i>los</i> vira <b>se</b>."))
    return L

ALL = n1() + n2() + n3() + n4() + n5() + n6()
# ids + stats
from collections import Counter
cnt = Counter(q['lv'] for q in ALL)
for i, q in enumerate(ALL): q['id'] = i + 1
print(len(ALL), dict(sorted(cnt.items())), file=sys.stderr)
print(Counter(q['k'] for q in ALL), file=sys.stderr)
json.dump(ALL, open(sys.argv[1], 'w'), ensure_ascii=False, separators=(',', ':'))
