# -*- coding: utf-8 -*-
"""Gera data/usos-se.json (questões) e data/usos-se-verbos.json (glossário: usos + verbos citados).

Uso: python3 scripts/pronominales/gen_se.py data
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from conj import conj, attach, strip  # noqa: E402
from catalog import PRON  # noqa: E402
from qlib import Bank, cap, low, select, finalize  # noqa: E402

B = Bank(20261106)
R = B.R
REF = ['me', 'te', 'se', 'nos', 'os', 'se']
CJ = {}


def cj(v, cls=''):
    if (v, cls) not in CJ:
        CJ[(v, cls)] = conj(v, cls)
    return CJ[(v, cls)]


# ------------------------------------------------------------------ usos (glossário)
USES = [
    ('u:reflexivo', 'Reflexivo', 'a ação volta para quem faz', 'se lava las manos', 'Cabe “a sí mismo”.'),
    ('u:reciproco', 'Recíproco', 'um ao outro (só plural)', 'se abrazan', 'Cabe “el uno al otro”.'),
    ('u:pronominal', 'Pronominal', 'o verbo exige o pronome', 'se arrepiente / se va', '“A sí mismo” não funciona; o verbo exige ou muda com o pronome.'),
    ('u:espontaneo', 'Mudança espontânea', 'algo acontece sozinho', 'la puerta se abrió', 'Algo mudou de estado sem causador.'),
    ('u:acidental', 'Acidental', 'aconteceu sem querer', 'se me cayó el vaso', 'Tem me/te/le… logo depois do se e algo aconteceu sem querer.'),
    ('u:enfase', 'Ênfase', '“tudo, até o fim”', 'se comió la pizza', 'Dá para tirar o se e o sentido continua, só mais fraco.'),
    ('u:pasivo', 'Passivo', 'algo é feito, sem dizer por quem', 'se venden casas', 'Uma coisa sofre a ação e o verbo concorda com ela.'),
    ('u:impersonal', 'Impessoal', '“a gente”, “as pessoas”', 'se vive bien aquí', 'Sem sujeito, verbo sempre no singular.'),
    ('u:lele', 'No lugar de le/les', 'evita “le lo”', 'se lo di', 'Vem antes de lo/la/los/las e substitui le/les.'),
    ('u:sesi', 'Se, sé, si, sí', 'quatro palavras diferentes', 'no sé si viene', 'se pronome; sé = sei/seja; si = condicional; sí = sim / si mesmo.'),
]
LABEL = {u[0]: u[1] for u in USES}
TEST = {u[0]: u[4] for u in USES}
USE_IDS = [u[0] for u in USES if u[0] != 'u:sesi']

# ------------------------------------------------------------------ 7. passivo
PASSIVE = [
    ('vender', '', ['casa', 'esta moto', 'pan casero'], ['casas', 'pisos', 'coches usados'], ['en el centro', 'a buen precio', 'en esta calle']),
    ('alquilar', '', ['apartamento', 'habitación', 'esta oficina'], ['pisos', 'bicicletas', 'apartamentos'], ['en la playa', 'por días', 'en verano']),
    ('hablar', '', ['español', 'inglés', 'portugués'], ['varios idiomas', 'cuatro lenguas'], ['en esta tienda', 'en la oficina', 'aquí']),
    ('necesitar', '', ['un cocinero', 'experiencia', 'un traductor'], ['camareros', 'voluntarios', 'profesores de inglés'], ['para el verano', 'urgentemente', 'en este hotel']),
    ('arreglar', '', ['ropa', 'calzado'], ['zapatos', 'relojes', 'ordenadores'], ['en esta tienda', 'en el acto']),
    ('aceptar', '', ['tarjeta', 'efectivo'], ['tarjetas', 'cheques'], ['en esta tienda', 'aquí']),
    ('ofrecer', '', ['un buen sueldo', 'alojamiento'], ['clases particulares', 'descuentos'], ['a los estudiantes', 'este mes']),
    ('comprar', '', ['oro', 'plata'], ['libros usados', 'muebles antiguos'], ['aquí', 'al mejor precio']),
    ('servir', 'i', ['el desayuno', 'la cena'], ['comidas', 'bebidas'], ['hasta las once', 'en la terraza']),
    ('reparar', '', ['calzado', 'maquinaria'], ['bicicletas', 'móviles'], ['en una hora', 'aquí']),
    ('buscar', '', ['piso', 'socio'], ['socios', 'ideas nuevas'], ['en el barrio', 'para el proyecto']),
    ('prohibir', 'í', ['el paso', 'la entrada'], ['las motos', 'los perros', 'las fotos'], ['en este edificio', 'en el museo', 'en la playa']),
    ('publicar', '', ['el resultado', 'la lista'], ['los resultados', 'las notas'], ['mañana', 'en la web']),
    ('construir', '', ['un puente', 'el estadio'], ['tres puentes', 'muchas casas'], ['en esta zona', 'cerca del río']),
]
PAST_CTX = ['el año pasado', 'en 2010', 'ayer', 'el mes pasado']

for vb, cls, S, P, ctx in PASSIVE:
    c = cj(vb, cls)
    for nouns, num in ((S, 'S'), (P, 'P')):
        for n in nouns:
            for k in ctx:
                f = c['pres'][2] if num == 'S' else c['pres'][5]
                o = c['pres'][5] if num == 'S' else c['pres'][2]
                s = f"Se ___ {n} {k}." if R.random() < .5 else f"{cap(k)} se ___ {n}."
                lv = 2 if vb in ('vender', 'alquilar', 'hablar', 'necesitar', 'comprar', 'aceptar') else 3
                B.mc(lv, 'Concordância', f'Complete com <i>{vb}</i> no presente.', s, [c['pres'][2], c['pres'][5]], f,
                     f"Se passivo: ‘{n}’ é o <b>sujeito</b>, e o verbo concorda com ele ({'singular' if num == 'S' else 'plural'}) → <b>se {f}</b>.", 'u:pasivo', 'PA1', shuffle=False)
                good = f"Se {f} {n} {k}."
                if R.random() < .6:
                    B.err(lv + 1 if lv < 3 else 3, f"Se {o} {n} {k}.", [1], good,
                          f"Concordância do passivo: ‘{n}’ é {'singular' if num == 'S' else 'plural'} → <b>se {f}</b>." + (" (<i>Se vende casas</i> é um erro comum, inclusive de nativos.)" if num == 'P' else ''), 'u:pasivo', 'PA2')
                else:
                    B.err(3, good, -1, good, f"Correto: o verbo concorda com ‘{n}’.", 'u:pasivo', 'PA2')
                B.inp(3, 'Transformar', 'Reescreva com <b>se</b> passivo (sem dizer quem faz).', f"{cap(c['pres'][5])} {n} {k}.", [good],
                      f"‘Eles {c['pres'][5]}…’ → <b>se {f} {n}</b>: o verbo passa a concordar com a coisa.", 'u:pasivo', 'PA3')
            if vb in ('construir', 'vender', 'publicar', 'alquilar', 'reparar'):
                n = R.choice(nouns)
                t = R.choice(PAST_CTX)
                f = c['pret'][2] if num == 'S' else c['pret'][5]
                B.mc(3, 'Concordância', f'Complete com <i>{vb}</i> no pretérito.', f"{cap(t)} se ___ {n}.", [c['pret'][2], c['pret'][5], c['pres'][2]], f,
                     f"No passado vale a mesma regra: concorda com ‘{n}’ → <b>se {f}</b>.", 'u:pasivo', 'PA4')

# ------------------------------------------------------------------ 8. impessoal
IMPERS = [('vivir', '', 'bien aquí'), ('comer', '', 'muy bien en Perú'), ('trabajar', '', 'mucho en esta empresa'), ('dormir', 'ue-u', 'bien en este hotel'),
          ('estar', '', 'muy bien en la terraza'), ('ir', '', 'al centro por esta calle'), ('entrar', '', 'por la puerta de atrás'), ('llegar', '', 'al museo en metro'),
          ('salir', '', 'muy tarde en Madrid'), ('cenar', '', 'tarde en España'), ('pagar', '', 'en la caja'), ('bailar', '', 'hasta el amanecer en las fiestas'),
          ('estudiar', '', 'mucho en esta universidad'), ('vivir', '', 'mejor en el campo'), ('viajar', '', 'barato en temporada baja')]
for vb, cls, rest in IMPERS:
    c = cj(vb, cls)
    f = c['pres'][2]
    B.mc(2, 'Impessoal', 'Complete (sentido de “a gente”, “as pessoas”).', f"Se ___ {rest}.", [f, c['pres'][5], c['pres'][3]], f,
         f"Se impessoal: não há sujeito, e o verbo fica <b>sempre no singular</b> → se {f}.", 'u:impersonal', 'IM1', shuffle=False)
    B.err(3, f"Se {c['pres'][5]} {rest}.", [1], f"Se {f} {rest}.", f"No impessoal o verbo fica no singular: <b>se {f}</b>.", 'u:impersonal', 'IM2')
    B.inp(3, 'Transformar', 'Reescreva com <b>se</b> impessoal (“a gente…”).', f"La gente {f} {rest}.", [f"Se {f} {rest}."],
          f"‘La gente {f}…’ = <b>Se {f} {rest}</b>.", 'u:impersonal', 'IM3')
for q, f, x in [("¿Cómo ___ “saudade” en español?", "se dice", "Pergunta impessoal: <b>¿cómo se dice…?</b>"),
                ("¿Cómo ___ tu apellido?", "se escribe", "<b>¿Cómo se escribe…?</b> — o verbo concorda com o que se escreve (singular)."),
                ("¿Cómo ___ esta palabra?", "se pronuncia", "<b>¿Cómo se pronuncia…?</b>"),
                ("¿Por dónde ___ a la estación?", "se va", "<b>¿Por dónde se va…?</b> — impessoal, singular.")]:
    B.mc(1, 'Impessoal', 'Complete.', q, [f, f.replace('se ', 'si '), f.replace('se ', 'sé ')], f, x, 'u:impersonal', 'IM4')

IMP_A = [('buscar', '', 'a los culpables'), ('contratar', '', 'a profesores nativos'), ('respetar', '', 'a los mayores'), ('ayudar', '', 'a los vecinos'),
         ('atender', 'ie', 'a los clientes por orden'), ('premiar', '', 'a los mejores alumnos'), ('entrevistar', '', 'a los candidatos'), ('invitar', '', 'a todos los socios'),
         ('vacunar', '', 'a los niños en la escuela'), ('llamar', '', 'a los pasajeros por megafonía'), ('detener', '', 'a los sospechosos'), ('despedir', 'i', 'a los trabajadores')]
for vb, cls, rest in IMP_A:
    c = cj(vb, cls)
    tense = 'pret' if vb in ('detener', 'despedir') else 'pres'
    f, o = c[tense][2], c[tense][5]
    B.mc(5, 'Impessoal', 'Complete (pessoas determinadas, com <b>a</b>).', f"Se ___ {rest}.", [f, o], f,
         f"Pessoas determinadas com <b>a</b> → se impessoal, verbo no <b>singular</b>: se {f} {rest}. A forma <i>se {o} {rest[2:]}</i> (sem a) também aparece, mas é menos indicada.", 'u:impersonal', 'IM5', shuffle=False)
    B.err(5, f"Se {o} {rest}.", [1], f"Se {f} {rest}.", f"Com <b>a</b> + pessoas, o se é impessoal: o verbo fica no singular → <b>se {f}</b>.", 'u:impersonal', 'IM6')

# ------------------------------------------------------------------ 4. mudança espontânea
SPONT = [
    ('abrir', '', 'Juan', [('la puerta', 'La puerta', 0), ('las ventanas', 'Las ventanas', 1)], 'abrir-se'),
    ('derretir', 'i', 'El sol', [('el hielo', 'El hielo', 0), ('la nieve', 'La nieve', 0), ('los helados', 'Los helados', 1)], 'derreter'),
    ('apagar', '', 'El viento', [('la vela', 'La vela', 0), ('las velas', 'Las velas', 1)], 'apagar'),
    ('romper', '', 'El niño', [('el vaso', 'El vaso', 0), ('los platos', 'Los platos', 1)], 'quebrar'),
    ('secar', '', 'El calor', [('la ropa', 'La ropa', 0), ('las sábanas', 'Las sábanas', 1)], 'secar'),
    ('cerrar', 'ie', 'El viento', [('la ventana', 'La ventana', 0), ('las puertas', 'Las puertas', 1)], 'fechar-se'),
    ('mover', 'ue', 'El terremoto', [('la mesa', 'La mesa', 0), ('los muebles', 'Los muebles', 1)], 'mover-se'),
    ('hundir', '', 'La tormenta', [('el barco', 'El barco', 0), ('los barcos', 'Los barcos', 1)], 'afundar'),
    ('quemar', '', 'El fuego', [('el bosque', 'El bosque', 0), ('las cortinas', 'Las cortinas', 1)], 'queimar'),
    ('mojar', '', 'La lluvia', [('la ropa', 'La ropa', 0), ('los zapatos', 'Los zapatos', 1)], 'molhar'),
    ('llenar', '', 'El agua', [('la piscina', 'La piscina', 0), ('los cubos', 'Los cubos', 1)], 'encher'),
    ('vaciar', 'í', 'La policía', [('la sala', 'La sala', 0), ('las calles', 'Las calles', 1)], 'esvaziar'),
    ('enfriar', 'í', 'El aire', [('la sopa', 'La sopa', 0), ('los platos', 'Los platos', 1)], 'esfriar'),
    ('calentar', 'ie', 'El sol', [('el agua', 'El agua', 0), ('las piedras', 'Las piedras', 1)], 'esquentar'),
    ('despertar', 'ie', 'El ruido', [('al bebé', 'El bebé', 0), ('a los niños', 'Los niños', 1)], 'acordar'),
    ('encender', 'ie', 'Alguien', [('la luz', 'La luz', 0), ('las farolas', 'Las farolas', 1)], 'acender'),
    ('congelar', '', 'El frío', [('el lago', 'El lago', 0), ('las tuberías', 'Las tuberías', 1)], 'congelar'),
    ('estropear', '', 'El niño', [('la lavadora', 'La lavadora', 0), ('los frenos', 'Los frenos', 1)], 'estragar'),
]
VERBS = []  # glossário de verbos citados
for vb, cls, causer, objs, pt in SPONT:
    vid = 'v:espontaneo:' + vb
    VERBS.append(dict(id=vid, name=vb + 'se', cat='Mudança espontânea', pt=pt, ex=f"{objs[0][1].lower()} se {cj(vb, cls)['pret'][2]}"))
    c = cj(vb, cls)
    for obj, subj, pl in objs:
        f = c['pret'][5] if pl else c['pret'][2]
        o = c['pret'][2] if pl else c['pret'][5]
        lv = 3
        B.inp(lv, 'Transformar', 'Reescreva <b>sem o causador</b> (algo aconteceu sozinho).', f"{causer} {c['pret'][2]} {obj}.", [f"{subj} se {f}."],
              f"Sem causador, a coisa vira sujeito e o <b>se é obrigatório</b>: {subj} se {f}. (Em português muitas vezes não há pronome: ‘o gelo derreteu’.)", [vid, 'u:espontaneo'], 'SP1')
        B.err(lv, f"{subj} {f}.", [len(subj.split(' '))], f"{subj} se {f}.",
              f"Falta o <b>se</b>: em espanhol a mudança espontânea pede o pronome → {subj.lower()} se {f}.", [vid, 'u:espontaneo'], 'SP2')
        B.mc(2, 'Completar', 'Complete (ninguém causou: aconteceu sozinho).', f"{subj} ___ de repente.", [f"se {f}", f, f"se {o}"], f"se {f}",
             f"Mudança espontânea: <b>se {f}</b>, concordando com ‘{subj.lower()}’.", [vid, 'u:espontaneo'], 'SP3')
        B.mc(4, 'Identificar', 'Qual é o uso do <i>se</i>?', f"{subj} se {f}.", None or [LABEL['u:espontaneo'], LABEL['u:reflexivo'], LABEL['u:pasivo'], LABEL['u:pronominal']],
             LABEL['u:espontaneo'], f"Algo mudou de estado sozinho, sem causador → <b>mudança espontânea</b> (se medio). Não é reflexivo: ‘{subj.lower()}’ não faz nada a si mesmo.", [vid, 'u:espontaneo'], 'SP4')

# ------------------------------------------------------------------ 5. acidental
ACC = [
    ('caer', '', ['el vaso', 'el móvil', 'la taza'], ['las llaves', 'las gafas'], None, 'cair'),
    ('olvidar', '', ['la cartera', 'su cumpleaños'], ['las entradas', 'los deberes'], 'olvidar', 'esquecer'),
    ('romper', '', ['el vaso', 'la pantalla'], ['las gafas', 'los platos'], 'romper', 'quebrar'),
    ('perder', 'ie', ['el pasaporte', 'la cartera'], ['las llaves', 'los billetes'], 'perder', 'perder'),
    ('quemar', '', ['la comida', 'el arroz'], ['las tostadas', 'los macarrones'], 'quemar', 'queimar'),
    ('acabar', '', ['la paciencia', 'el dinero'], ['las ideas', 'los ahorros'], None, 'acabar'),
    ('escapar', '', ['el autobús', 'un secreto'], ['dos errores', 'los detalles'], None, 'escapar'),
    ('ocurrir', '', ['una idea', 'algo mejor'], ['varias ideas', 'dos soluciones'], None, 'ocorrer'),
    ('quedar', '', ['el paraguas en el bar', 'la chaqueta en casa'], ['las llaves en el coche', 'los papeles en la oficina'], None, 'ficar (esquecido em algum lugar)'),
    ('pasar', '', ['tu cumpleaños', 'la fecha'], ['dos errores', 'las horas volando'], None, 'passar batido'),
    ('descomponer', '', ['el coche', 'la lavadora'], ['los frenos', 'las luces'], None, 'quebrar, enguiçar (Am. Lat.)'),
    ('manchar', '', ['la camisa', 'el vestido'], ['los pantalones', 'las zapatillas'], 'manchar', 'manchar'),
]
EXP = [("A mí", "me"), ("A ti", "te"), ("A Juan", "le"), ("A mi madre", "le"), ("A usted", "le"), ("A nosotros", "nos"), ("A vosotros", "os"),
       ("A mis padres", "les"), ("A ustedes", "les"), ("A los niños", "les")]
PERS = [("Yo", 0, "me", "A mí"), ("Tú", 1, "te", "A ti"), ("Mi padre", 2, "le", "A mi padre"), ("Nosotros", 3, "nos", "A nosotros"), ("Mis hijos", 5, "les", "A mis hijos")]
for vb, cls, S, P, tr, pt in ACC:
    vid = 'v:acidental:' + vb
    c = cj(vb, cls)
    VERBS.append(dict(id=vid, name=f"se me {c['pret'][2]}", cat='Acidental', pt=pt, ex=f"se me {c['pret'][2]} {S[0]}"))
    th = [(t, 'S') for t in S] + [(t, 'P') for t in P]
    for exp, pr in EXP:
        for t, num in th:
            f = c['pret'][2] if num == 'S' else c['pret'][5]
            o = c['pret'][5] if num == 'S' else c['pret'][2]
            lv = 2 if vb in ('caer', 'olvidar', 'romper', 'perder') else (3 if vb in ('quemar', 'acabar', 'manchar') else 5)
            B.mc(lv, 'Completar', 'Complete com o pronome da pessoa afetada.', f"{exp} se ___ {f} {t}.", ['me', 'te', 'le', 'nos', 'os', 'les'], pr,
                 f"Estrutura: <b>se + {pr}</b> (pessoa afetada: {low(exp)}) + verbo concordando com a coisa.", [vid, 'u:acidental'], 'AC1', shuffle=False)
            B.mc(lv, 'Concordância', f'Complete com <i>{vb}</i> no pretérito.', f"{exp} se {pr} ___ {t}.", [c['pret'][2], c['pret'][5], c['pret'][0]], f,
                 f"O verbo concorda com a coisa (‘{t.split(' en ')[0]}’), não com a pessoa → <b>{f}</b>." + (f" <i>{c['pret'][0]}</i> seria ‘eu …’ de propósito." if vb != 'ocurrir' else ''), [vid, 'u:acidental'], 'AC2')
            n = len(exp.split(' '))
            if R.random() < .5:
                B.err(4, f"{exp} {pr} se {f} {t}.", [n, n + 1], f"{exp} se {pr} {f} {t}.",
                      f"Ordem fixa: o <b>se</b> vem sempre primeiro → se {pr}. ‘{pr.capitalize()} se’ é comum na fala popular, mas está errado.", [vid, 'u:acidental'], 'AC3')
    if tr:
        for s, i, pr, aexp in PERS:
            for t, num in th[:3]:
                f = c['pret'][2] if num == 'S' else c['pret'][5]
                ans = [f"Se {pr} {f} {t}.", f"{aexp} se {pr} {f} {t}."]
                B.inp(3, 'Transformar', 'Reescreva como algo que aconteceu <b>sem querer</b>.', f"{s} {c['pret'][i]} {t} (sin querer).", ans,
                      f"<i>{s} {c['pret'][i]}…</i> = fui eu (ação voluntária). <b>Se {pr} {f}…</b> = aconteceu sem querer, tira a culpa de quem fez.", [vid, 'u:acidental'], 'AC4')
    B.mc(4, 'Identificar', 'Qual é o uso do <i>se</i>?', f"Se me {c['pret'][2]} {S[0]}.", [LABEL['u:acidental'], LABEL['u:pasivo'], LABEL['u:lele'], LABEL['u:reflexivo']],
         LABEL['u:acidental'], "Tem <b>me</b> logo depois do <i>se</i> e algo aconteceu sem querer → <b>acidental</b> (passo 2 do roteiro).", [vid, 'u:acidental'], 'AC5')

# ------------------------------------------------------------------ 9. se = le/les
LELE = [('dar', '', [('el libro', 'lo'), ('la llave', 'la'), ('los documentos', 'los'), ('las entradas', 'las')]),
        ('enviar', 'í', [('la carta', 'la'), ('el paquete', 'lo'), ('las fotos', 'las')]),
        ('comprar', '', [('el regalo', 'lo'), ('los juguetes', 'los'), ('la bicicleta', 'la')]),
        ('explicar', '', [('el problema', 'lo'), ('la lección', 'la'), ('los ejercicios', 'los')]),
        ('regalar', '', [('el perfume', 'lo'), ('las flores', 'las')]), ('prestar', '', [('el coche', 'lo'), ('los apuntes', 'los')]),
        ('contar', 'ue', [('la historia', 'la'), ('el secreto', 'lo')]), ('devolver', 'ue', [('el dinero', 'lo'), ('las llaves', 'las')]),
        ('mandar', '', [('el mensaje', 'lo'), ('las fotos', 'las')]), ('decir', '', [('la verdad', 'la'), ('el precio', 'lo')]),
        ('enseñar', '', [('las fotos', 'las'), ('el piso', 'lo')]), ('pedir', 'i', [('la cuenta', 'la'), ('los apuntes', 'los')])]
REC = [('a Juan', 'le'), ('a María', 'le'), ('a mis padres', 'les'), ('a las niñas', 'les'), ('a usted', 'le'), ('a ustedes', 'les'), ('a su jefe', 'le')]
LSUBJ = [('Yo', 0), ('Tú', 1), ('Mi madre', 2), ('Nosotros', 3)]
for vb, cls, objs in LELE:
    c = cj(vb, cls)
    for s, i in LSUBJ:
        for np, od in objs:
            rec, pr = R.choice(REC)
            f = c['pret'][i]
            B.inp(2, 'Substituir', 'Substitua os <b>dois</b> objetos destacados por pronomes.', f"{s} {pr} {f} [[{np}]] [[{rec}]].",
                  [f"{s} se {od} {f}.", f"{s} se {od} {f} {rec}."] + ([f"Se {od} {f}."] if s in ('Yo', 'Tú', 'Nosotros') else []),
                  f"{pr} + {od} não existe: <b>le/les vira se</b> diante de lo/la/los/las → se {od} {f}.", 'u:lele', 'LE1')
            B.err(2, f"{s} {pr} {od} {f} {rec}.", [len(s.split(' '))], f"{s} se {od} {f} {rec}.",
                  f"O espanhol não permite ‘{pr} {od}’: diante de {od}, <b>{pr} → se</b>.", 'u:lele', 'LE2')
            B.mc(3, 'Completar', 'Complete com os dois pronomes.', f"—¿Y {np}? —Ya ___ {f} {rec}.", [f"se {od}", f"{pr} {od}", f"{od} se", f"se {pr}"], f"se {od}",
                 f"OD ‘{np}’ → {od}; OI ‘{rec}’ → {pr} → <b>se</b>. Ordem: se + {od}.", 'u:lele', 'LE3')
for s, opts, x in [
    ("‘Se lo di’ pode significar que dei isso:", ["a ele, a ela, a você (usted) ou a eles", "só a ele", "a mim mesmo", "a nós"], "Como <i>se</i> não indica gênero nem número, pode ser a él, a ella, a usted, a ellos, a ellas, a ustedes."),
    ("Para deixar claro que dei a ela:", ["Se lo di a ella.", "Le lo di.", "Se la di.", "Lo se di a ella."], "Acrescenta-se <b>a ella</b> para desfazer a ambiguidade do <i>se</i>."),
    ("Na norma culta, ‘Ya se los dije’ (dizendo ‘isso’ a vocês) deve ser:", ["Ya se lo dije.", "Ya les lo dije.", "Ya se los dije (é o padrão).", "Ya los se dije."], "O plural de <i>vocês</i> não passa para o OD: <i>lo</i> = isso (singular). ‘Se los’ é muito comum na América, mas a norma culta mantém <b>se lo</b>."),
]:
    B.mc(5 if 'norma' in s else 3, 'Se = le/les', s, '', opts, opts[0], x, 'u:lele', 'LE4')

# ------------------------------------------------------------------ 1/2. reflexivo e recíproco
BODY = [('lavar', '', 'las manos', 'mis manos|tus manos|sus manos'), ('cepillar', '', 'los dientes', 'mis dientes|tus dientes|sus dientes'),
        ('secar', '', 'el pelo', 'mi pelo|tu pelo|su pelo'), ('pintar', '', 'las uñas', 'mis uñas|tus uñas|sus uñas'),
        ('poner', '', 'los zapatos', 'mis zapatos|tus zapatos|sus zapatos'), ('quitar', '', 'el abrigo', 'mi abrigo|tu abrigo|su abrigo'),
        ('cortar', '', 'el pelo', 'mi pelo|tu pelo|su pelo'), ('depilar', '', 'las cejas', 'mis cejas|tus cejas|sus cejas'), ('afeitar', '', 'la barba', 'mi barba|tu barba|su barba')]
for vb, cls, art, poss in BODY:
    c = cj(vb, cls)
    P3 = poss.split('|')
    for s, i, pi in [('Yo', 0, 0), ('Tú', 1, 1), ('Juan' if vb == 'afeitar' else 'Ana', 2, 2), ('Mis hijos', 5, 2)]:
        good = f"{s} {REF[i]} {c['pres'][i]} {art}."
        B.err(1 if vb in ('lavar', 'cepillar', 'poner', 'quitar') else 2, f"{s} {REF[i]} {c['pres'][i]} {P3[pi]}.", [len(s.split(' ')) + 2], good,
              f"Com parte do corpo ou roupa, o espanhol usa <b>se + artigo</b>, não possessivo: {REF[i]} {c['pres'][i]} <b>{art.split(' ')[0]}</b> {art.split(' ', 1)[1]}.", 'u:reflexivo', 'RF1')
        B.mc(1, 'Completar', 'Complete com o pronome reflexivo.', f"{s} ___ {c['pres'][i]} {art}.", REF[:5], REF[i],
             f"Reflexivo: a ação volta para quem faz. ‘{s}’ → <b>{REF[i]}</b>.", 'u:reflexivo', 'RF2', shuffle=False)

OTHER = {'lavar': 'el coche', 'cepillar': 'al perro', 'secar': 'los platos', 'pintar': 'la pared', 'poner': 'la mesa', 'quitar': 'la mesa',
         'cortar': 'el pan', 'afeitar': 'al abuelo'}
for vb, cls, art, poss in BODY:
    if vb not in OTHER:
        continue
    c = cj(vb, cls)
    for s, i in [('Yo', 0), ('Tú', 1), ('Mi padre', 2), ('Nosotros', 3), ('Mis hijos', 5)]:
        B.mc(1, 'Com ou sem se', 'Complete com o pronome — ou nada, se a ação recai sobre outra coisa.', f"{s} ___ {c['pres'][i]} {OTHER[vb]}.", [REF[i], '— (nada)'], '— (nada)',
             f"A ação recai sobre <b>outra coisa</b> ({OTHER[vb]}) → sem reflexivo.", 'u:reflexivo', 'RF3', shuffle=False)
        B.mc(1, 'Com ou sem se', 'Complete com o pronome — ou nada, se a ação recai sobre outra coisa.', f"{s} ___ {c['pres'][i]} {art}.", [REF[i], '— (nada)'], REF[i],
             f"A ação recai sobre a própria pessoa ({art}) → reflexivo <b>{REF[i]}</b>.", 'u:reflexivo', 'RF3', shuffle=False)

REFL_EX = ["Se lava las manos.", "Me miro al espejo.", "Nos vestimos rápido.", "Ana se peina delante del espejo.", "Mi padre se afeita cada mañana.",
           "Te secas el pelo con la toalla.", "Los niños se lavan los dientes.", "Se maquilla para salir.", "Me pongo los zapatos.", "Juan se ducha por la mañana.",
           "Nos sentamos junto a la ventana.", "Me acuesto a medianoche."]
RECIP = [e for e in PRON if e['grp'] == 'rec']
RECIP_EX = [cap(e['ex']) + '.' for e in RECIP] + ["Se abrazan.", "Juan y Ana se escriben cada día.", "Mis padres se quieren mucho."]
PRON_EX = [cap(e['ex']).split(' / ')[0].rstrip('.') + '.' for e in PRON if e['grp'] in ('so', 'sen') and e['ex'] and 'sensitive' not in e['flags']
           and not e['ex'].startswith(('el ', 'pórtate', 'fíjate', 'yo ')) and ' se ' in ' ' + e['ex'] + ' ' and 'me ' not in e['ex']]
PRON_BASIC = ["Se arrepiente de todo.", "No se atreve.", "Se queja mucho.", "Se va.", "Se duerme en el sofá.", "Se acuerda de todo.", "Se pone triste.", "Se volvió loco.", "Se enteró ayer.", "Se da cuenta de todo."]
PRON_EX += ["Se arrepiente de todo.", "No se atreve.", "Se queja mucho.", "Se va.", "Se duerme en el sofá.", "Se acuerda de todo.", "Se pone triste.", "Se volvió loco."]
ENF_EX = ["Se comió toda la pizza.", "Se leyó el libro en un día.", "Se bebió dos litros de agua.", "Se sabe la canción.", "Se gastó todo el sueldo.",
          "Se vio la serie entera.", "Se fumó un paquete entero.", "Se tragó la mentira.", "Se aprendió el poema de memoria.", "Se tomó un café."]
PAS_EX = ["Se venden casas.", "Se alquila apartamento.", "Se habla español.", "Se necesitan camareros.", "Se construyeron tres puentes.", "Se aceptan tarjetas.",
          "Se arreglan zapatos.", "Se publicaron los resultados."]
IMP_EX = ["Se vive bien aquí.", "Se come muy bien en Perú.", "¿Cómo se dice “saudade” en español?", "Se trabaja mucho en esta empresa.", "Se busca a los culpables.",
          "Se contrata a profesores.", "Se duerme bien en este hotel.", "Se cena tarde en España."]
LELE_EX = ["Se lo di.", "Se la envié.", "Se los compré.", "Se lo das.", "Se las devolví ayer.", "Se lo expliqué a ella."]
ACC_EX = ["Se me cayó el vaso.", "Se nos olvidaron las llaves.", "Se le rompió el móvil.", "Se te quemó la comida.", "Se me pasó tu cumpleaños.", "Se les acabó el dinero."]
ESP_EX = ["La puerta se abrió.", "El hielo se derritió.", "La vela se apagó.", "El vaso se rompió.", "La ropa se secó.", "El barco se hundió.", "La sopa se enfrió."]
CLASS = [('u:reflexivo', REFL_EX), ('u:reciproco', RECIP_EX), ('u:pronominal', PRON_EX), ('u:enfase', ENF_EX), ('u:pasivo', PAS_EX), ('u:impersonal', IMP_EX),
         ('u:lele', LELE_EX), ('u:acidental', ACC_EX), ('u:espontaneo', ESP_EX)]
EXPL = {
    'u:reflexivo': "Cabe <i>a sí mismo</i>: a pessoa faz a ação e ela mesma recebe → <b>reflexivo</b>.",
    'u:reciproco': "Cabe <i>el uno al otro</i>: duas ou mais pessoas fazem a ação uma na outra → <b>recíproco</b>.",
    'u:pronominal': "<i>A sí mismo</i> não funciona e o verbo exige (ou muda de sentido com) o pronome → <b>pronominal</b>.",
    'u:enfase': "Dá para tirar o <i>se</i> e o sentido continua, só mais fraco (‘tudo, até o fim’) → <b>ênfase</b>.",
    'u:pasivo': "Uma coisa sofre a ação, não se diz quem a fez, e o verbo concorda com ela → <b>passivo</b>.",
    'u:impersonal': "Não há sujeito e o verbo fica sempre no singular (‘a gente’) → <b>impessoal</b>.",
    'u:lele': "O <i>se</i> vem antes de lo/la/los/las e substitui le/les → <b>no lugar de le/les</b>.",
    'u:acidental': "Tem me/te/le… logo depois do <i>se</i> e algo aconteceu sem querer → <b>acidental</b>.",
    'u:espontaneo': "Algo mudou de estado sozinho, sem causador → <b>mudança espontânea</b>.",
}
BASIC3 = ['u:reflexivo', 'u:reciproco', 'u:pronominal']
for uid, exs in CLASS:
    for s in exs:
        if uid in BASIC3 and (uid != 'u:pronominal' or s in PRON_BASIC):
            B.mc(1, 'Identificar', 'Qual é o uso do <i>se</i>?', s, [LABEL[u] for u in BASIC3], LABEL[uid], EXPL[uid], uid, 'CL1', shuffle=False)
        others = R.sample([u for u in USE_IDS if u != uid], 3)
        B.mc(4, 'Identificar', 'Qual é o uso do <i>se</i>?', s, [LABEL[uid]] + [LABEL[u] for u in others], LABEL[uid], EXPL[uid], uid, 'CL2')
        allopts = [LABEL[u] for u in USE_IDS]
        B.mc(6, 'Identificar', 'Qual é o uso do <i>se</i>? (todas as opções)', s, allopts, LABEL[uid], EXPL[uid], uid, 'CL3', shuffle=False)

CONF = {'u:pasivo': ['u:impersonal', 'u:espontaneo'], 'u:impersonal': ['u:pasivo', 'u:pronominal'], 'u:espontaneo': ['u:reflexivo', 'u:pronominal', 'u:acidental'],
        'u:reflexivo': ['u:reciproco', 'u:pronominal', 'u:espontaneo'], 'u:reciproco': ['u:reflexivo', 'u:pronominal'], 'u:pronominal': ['u:reflexivo', 'u:enfase', 'u:espontaneo'],
        'u:enfase': ['u:pronominal', 'u:reflexivo'], 'u:acidental': ['u:espontaneo', 'u:lele', 'u:pasivo'], 'u:lele': ['u:reflexivo', 'u:acidental']}
for uid, exs in CLASS:
    for s in exs:
        B.mc(5, 'Identificar', 'Qual é o uso do <i>se</i>? (opções parecidas)', s, [LABEL[uid]] + [LABEL[u] for u in CONF[uid]], LABEL[uid], EXPL[uid], uid, 'CL4')

# passivo com perífrase (nível 6)
PERI = [('ir a', 'va a', 'van a'), ('deber', 'debe', 'deben'), ('poder', 'puede', 'pueden'), ('empezar a', 'empezó a', 'empezaron a'), ('tener que', 'tiene que', 'tienen que')]
for vb, cls, S, P, ctx in PASSIVE:
    for nouns, num in ((S, 'S'), (P, 'P')):
        n = R.choice(nouns)
        nm, s3, s6 = R.choice(PERI)
        f = s3 if num == 'S' else s6
        B.mc(6, 'Passivo', f'Complete com <i>{nm.split(" ")[0]}</i>.', f"Se ___ {vb} {n} {R.choice(ctx)}.", [s3, s6], f,
             f"Na perífrase, o verbo auxiliar também concorda com o sujeito paciente ‘{n}’ → <b>se {f} {vb}</b>.", 'u:pasivo', 'PE', shuffle=False)

# impessoal com verbo pronominal: uno (nível 6)
for e in PRON:
    if e['grp'] not in ('rot', 'emo') or e['tier'] != 1 or not e['tails'] or 'od' in e['flags']:
        continue
    c = cj(e['verb'], e['cls'])
    t = e['tails'][0]
    f = c['pres'][2]
    B.mc(6, 'Impessoal', 'Forma impessoal (“a gente…”) com verbo pronominal:', f"Aquí ___ {t}.", [f"uno se {f}", f"se se {f}", f"uno {f}", f"se {c['pres'][3]}"], f"uno se {f}",
         f"Não existe ‘se se’: com verbo pronominal (<i>{e['verb']}se</i>), o impessoal se faz com <b>uno se {f}</b>.", 'u:impersonal', 'UNO')

# testes a sí mismo / el uno al otro
for s, ans, x, uid in [
    ("Juan y Ana se escriben cada día ___.", "el uno al otro", "Recíproco: cabe <b>el uno al otro</b> (ou <i>mutuamente</i>).", 'u:reciproco'),
    ("Ana se mira ___ en el espejo.", "a sí misma", "Reflexivo: cabe <b>a sí misma</b>.", 'u:reflexivo'),
    ("Los novios se miran ___ (cada um olha para o outro).", "el uno al otro", "Para deixar claro o recíproco: <b>el uno al otro</b>.", 'u:reciproco'),
    ("Los niños se miran ___ en el espejo (cada um a si).", "a sí mismos", "Para deixar claro o reflexivo: <b>a sí mismos</b>.", 'u:reflexivo'),
    ("Nos ayudamos ___.", "mutuamente", "Recíproco: <b>mutuamente</b> = el uno al otro.", 'u:reciproco'),
    ("Mi abuelo habla solo: se habla ___.", "a sí mismo", "Reflexivo: <b>a sí mismo</b>.", 'u:reflexivo'),
]:
    opts = ["el uno al otro", "a sí mismos", "a sí misma", "a sí mismo", "mutuamente"]
    opts = [ans] + R.sample([o for o in opts if o != ans], 2)
    B.mc(2, 'Reflexivo × recíproco', 'Complete para deixar o sentido claro.', s, opts, ans, x, uid, 'RR')
B.mc(4, 'Reflexivo × recíproco', '“Los novios se miran” pode ser:', '', ["Reflexivo ou recíproco: depende do contexto", "Só recíproco", "Só reflexivo", "Passivo"],
     "Reflexivo ou recíproco: depende do contexto", "<i>Se miran</i> é ambíguo: cada um se olha (reflexivo) ou olham um para o outro (recíproco). Desfaz-se com <i>a sí mismos</i> ou <i>el uno al otro</i>.", ['u:reflexivo', 'u:reciproco'], 'RR')
for e in RECIP:
    c = cj(e['verb'], e['cls'])
    for s, i in [('Nosotros', 3), ('Juan y Ana', 5), ('Vosotros', 4), ('Mis padres', 5)]:
        t = e['tails'][0]
        B.mc(2, 'Completar', 'Complete (sentido recíproco).', f"{s} ___ {c['pres'][i]} {t}.", REF[:5], REF[i],
             f"Recíproco só aparece no plural: nos, os, se. ‘{s}’ → <b>{REF[i]}</b>.", 'u:reciproco', 'RC')
    B.mc(2, 'Completar', 'Recíproco: qual sujeito é possível?', f"___ {e['ex'].split(' ', 1)[1] if e['ex'].startswith(('nos', 'se')) else e['ex']}.",
         ['Mis amigos y yo' if e['ex'].startswith('nos') else 'Juan y Ana', 'Yo', 'Mi hermano', 'Tú'], 'Mis amigos y yo' if e['ex'].startswith('nos') else 'Juan y Ana',
         "O recíproco exige duas ou mais pessoas (plural).", 'u:reciproco', 'RC2')

# ------------------------------------------------------------------ 3. pronominal / 6. ênfase
for e in PRON:
    if e['grp'] not in ('so', 'sen') or not e['tails'] or 'special' in e['flags'] or 'sensitive' in e['flags'] or e['tier'] == 3:
        continue
    c = cj(e['verb'], e['cls'])
    t = e['tails'][0]
    B.mc(3, 'Pronominal', 'Faça o teste: “a sí mismo” cabe na frase?', f"Ana se {c['pres'][2]} {t}.",
         ["Não: é um verbo pronominal", "Sim: é reflexivo", "Sim: é recíproco", "Não: é passivo"], "Não: é um verbo pronominal",
         f"<i>Ana se {c['pres'][2]} a sí misma</i> não faz sentido: o pronome faz parte do verbo <b>{e['verb']}se</b>." + (f" Sem ele, <i>{e['base']}</i> = {e['base_pt']}." if e.get('base') else ''), 'u:pronominal', 'PR1')
for e in PRON:
    if e['grp'] != 'enf' or e['verb'] in ('esperar', 'subir', 'saber', 'conocer'):
        continue
    c = cj(e['verb'], e['cls'])
    q = e['tails'][0]
    B.mc(4, 'Ênfase', 'O que acontece se tirarmos o <i>se</i>?', f"Mi hermano se {c['pret'][2]} {q}.",
         ["Continua correta, só perde a ideia de ‘tudo, até o fim’", "Fica errada", "Muda de sentido", "Vira passiva"],
         "Continua correta, só perde a ideia de ‘tudo, até o fim’", f"Se de ênfase: <i>Mi hermano {c['pret'][2]} {q}</i> continua certo, só fica mais fraco.", 'u:enfase', 'EN1')
    for b in e.get('bare', [])[:1]:
        B.mc(5, 'Ênfase', 'Qual frase soa <b>estranha</b>?', '', [f"Se {c['pret'][2]} {b}.", f"Se {c['pret'][2]} {q}.", f"{cap(c['pret'][2])} {b}.", f"{cap(c['pret'][2])} {q}."],
             f"Se {c['pret'][2]} {b}.", f"O se de ênfase pede objeto definido ou quantificado ({q}); com ‘{b}’ soa estranho.", 'u:enfase', 'EN2')

# ------------------------------------------------------------------ se / sé / si / sí
SESI = [
    ("No ___ dónde está.", "sé", "<b>sé</b> = eu sei (saber)."), ("___ llueve, no voy.", "Si", "Condicional: o ‘se’ do português é <b>si</b> em espanhol."),
    ("—¿Vienes? —___, claro.", "Sí", "<b>sí</b> = sim."), ("Solo piensa en ___ mismo.", "sí", "<b>sí mismo</b> = si mesmo (com acento)."),
    ("___ amable con tu hermana.", "Sé", "<b>sé</b> também é o imperativo de <i>ser</i> (seja)."), ("Ella ___ lava las manos.", "se", "Pronome reflexivo: <b>se</b>."),
    ("No sé ___ vendrá.", "si", "<b>si</b> = se (dúvida, pergunta indireta)."), ("Ya lo ___: no hace falta que me lo digas.", "sé", "<b>sé</b> = eu sei."),
    ("Aquí ___ vive muy bien.", "se", "Se impessoal: <b>se</b>."), ("___ me cayó el vaso.", "Se", "Se acidental: <b>se</b>."),
    ("Dijo que ___, que vendría.", "sí", "<b>sí</b> = sim."), ("Me pregunto ___ tendrá razón.", "si", "Pergunta indireta → <b>si</b>."),
    ("___ tienes tiempo, llámame.", "Si", "Condicional → <b>si</b>."), ("Habla mucho de ___ misma.", "sí", "<b>sí misma</b> = si mesma."),
    ("No ___ nada de él.", "sé", "<b>sé</b> = eu sei."), ("___ lo di ayer.", "Se", "Se no lugar de le: <b>se</b> lo di."),
    ("___ venden pisos.", "Se", "Se passivo: <b>se</b>."), ("___ fuerte: todo va a salir bien.", "Sé", "Imperativo de <i>ser</i>: <b>sé</b> fuerte."),
    ("Eso ___ que no lo hago.", "sí", "Ênfase afirmativa: <b>eso sí</b> (isso sim)."), ("¿Y ___ no viene?", "si", "‘E se não vier?’ → <b>si</b> (condicional)."),
]
for s, ans, x in SESI:
    B.mc(1 if ans.lower() in ('si', 'sí', 'se') and len(s) < 26 else 2, 'Se, sé, si, sí', 'Complete com se, sé, si ou sí.', s,
         ['se', 'sé', 'si', 'sí'] if ans[0].islower() else ['Se', 'Sé', 'Si', 'Sí'], ans, x, 'u:sesi', 'SS', shuffle=False)
for s, bad, fix, x in [
    ("Se llueve, no voy.", [0], "Si llueve, no voy.", "Armadilha do português: o ‘se’ condicional é <b>si</b> em espanhol."),
    ("Yo no se nada de eso.", [2], "Yo no sé nada de eso.", "‘Eu sei’ = <b>sé</b>, com acento."),
    ("Se tienes hambre, come algo.", [0], "Si tienes hambre, come algo.", "Condicional → <b>si</b>."),
    ("Solo piensa en si mismo.", [3], "Solo piensa en sí mismo.", "‘Si mesmo’ = <b>sí mismo</b>, com acento."),
    ("No sé se vendrá mañana.", [2], "No sé si vendrá mañana.", "Pergunta indireta (se vem ou não) → <b>si</b>."),
    ("—¿Te gusta? —Si, mucho.", [3], "—¿Te gusta? —Sí, mucho.", "‘Sim’ = <b>sí</b>, com acento."),
    ("Ella sé peina rápido.", [1], "Ella se peina rápido.", "Pronome reflexivo: <b>se</b>, sem acento."),
    ("Si vende casa en la playa.", [0], "Se vende casa en la playa.", "Passivo: <b>se</b> (pronome)."),
]:
    B.err(2, s, bad, fix, x, 'u:sesi', 'SS2')

# ------------------------------------------------------------------ casos avançados (curados)
HAND = [
    (5, 'Passivo', 'Complete.', "Se ___ fumar y comer en la sala.", ["prohíbe", "prohíben"], "prohíbe", "Infinitivos como sujeito → <b>singular</b>, mesmo que sejam dois.", 'u:pasivo'),
    (5, 'Passivo', 'Complete.', "Se ___ las motos en el centro.", ["prohíben", "prohíbe"], "prohíben", "Sujeito plural (las motos) → <b>se prohíben</b>.", 'u:pasivo'),
    (5, 'Impessoal', 'Complete.', "Se ___ que va a llover.", ["dice", "dicen"], "dice", "Uma oração (que va a llover) funciona como sujeito singular → <b>se dice</b>.", 'u:impersonal'),
    (5, 'Impessoal', 'Complete.', "Se ___ que habrá huelga.", ["rumorea", "rumorean"], "rumorea", "Oração como sujeito → singular.", 'u:impersonal'),
    (5, 'Passivo', 'Complete.', "Se ___ silencio.", ["ruega", "ruegan"], "ruega", "<b>Se ruega silencio</b> (pede-se silêncio): concorda com ‘silencio’.", 'u:pasivo'),
    (5, 'Passivo', 'Complete.', "Se ___ a los pasajeros que no fumen.", ["ruega", "ruegan"], "ruega", "Com <i>a</i> + pessoas → impessoal, singular.", 'u:impersonal'),
    (5, 'Passivo', 'Complete.', "Se ___ camareros con experiencia.", ["necesitan", "necesita"], "necesitan", "Pessoas indeterminadas sem <i>a</i> → passivo, concorda: <b>se necesitan camareros</b>.", 'u:pasivo'),
    (5, 'Impessoal', 'Complete.', "Se ___ a los ancianos en esta cultura.", ["respeta", "respetan"], "respeta", "Pessoas determinadas com <i>a</i> → impessoal singular.", 'u:impersonal'),
    (6, 'Impessoal', 'Qual é a forma impessoal correta de “no campo a gente se levanta cedo”?', '', ["En el campo uno se levanta temprano.", "En el campo se se levanta temprano.", "En el campo se levantamos temprano.", "En el campo uno levanta temprano."],
     "En el campo uno se levanta temprano.", "Com verbo pronominal não dá para usar o se impessoal (‘se se’ não existe): usa-se <b>uno</b> + se.", 'u:impersonal'),
    (6, 'Impessoal', 'Complete (impessoal com verbo pronominal).', "En este pueblo ___ se aburre mucho.", ["uno", "se", "— (nada)"], "uno", "Para o impessoal de <i>aburrirse</i>: <b>uno se aburre</b>.", 'u:impersonal'),
    (6, 'Impessoal', 'Complete (impessoal com verbo pronominal).', "Con el tiempo, ___ se acostumbra a todo.", ["uno", "se", "— (nada)"], "uno", "<b>Uno se acostumbra</b>: impessoal de verbo pronominal.", 'u:impersonal'),
    (6, 'Passivo', '“Las casas fueron vendidas” em passiva com se:', '', ["Se vendieron las casas.", "Se vendió las casas.", "Se vendieron a las casas.", "Las casas se vendió."],
     "Se vendieron las casas.", "Pasiva refleja: <b>se + verbo concordando</b> com a coisa (plural).", 'u:pasivo'),
    (6, 'Passivo', '“El puente fue construido en 2010” em passiva com se:', '', ["Se construyó el puente en 2010.", "Se construyeron el puente en 2010.", "Se construyó al puente en 2010.", "El puente se construyeron en 2010."],
     "Se construyó el puente en 2010.", "Singular: <b>se construyó</b>.", 'u:pasivo'),
    (6, 'Roteiro', 'Pelo roteiro de identificação, qual é o primeiro teste?', '', ["Vem antes de lo/la/los/las e substitui le/les?", "Cabe ‘a sí mismo’?", "Dá para tirar o se?", "Algo mudou sozinho?"],
     "Vem antes de lo/la/los/las e substitui le/les?", "O roteiro começa pelo caso mais fácil de ver: <b>se lo / se la</b> (uso 9).", ['u:lele']),
    (6, 'Roteiro', '“Se me olvidó la cita”: qual passo do roteiro identifica o uso?', '', ["Tem me/te/le… logo depois e algo aconteceu sem querer", "Cabe ‘a sí mismo’", "O verbo fica sempre no singular sem sujeito", "Uma coisa sofre a ação"],
     "Tem me/te/le… logo depois e algo aconteceu sem querer", "Passo 2 → <b>acidental</b>.", ['u:acidental']),
    (6, 'Roteiro', '“Se despertó con el ruido”: qual uso é mais adequado?', '', ["Mudança espontânea / pronominal (despertarse)", "Passivo", "Impessoal", "No lugar de le"],
     "Mudança espontânea / pronominal (despertarse)", "O documento lista <i>se despertó</i> entre as mudanças espontâneas: ninguém aparece como causador. Também é um verbo de rotina pronominal.", ['u:espontaneo', 'u:pronominal']),
    (6, 'Passivo × impessoal', 'Qual frase é <b>passiva</b>?', '', ["Se alquilan pisos.", "Se vive bien.", "Se contrata a profesores.", "Se trabaja mucho."],
     "Se alquilan pisos.", "Passivo: há uma coisa (pisos) que concorda com o verbo.", ['u:pasivo', 'u:impersonal']),
    (6, 'Passivo × impessoal', 'Qual frase é <b>impessoal</b>?', '', ["Se busca a los culpables.", "Se venden coches.", "Se necesitan camareros.", "Se construyeron puentes."],
     "Se busca a los culpables.", "Impessoal: pessoas determinadas com <i>a</i>, verbo no singular.", ['u:pasivo', 'u:impersonal']),
    (6, 'Combinações', 'Complete.', "A Juan ___ olvidaron las llaves.", ["se le", "le se", "se lo", "lo se"], "se le", "Acidental: <b>se le</b> (se sempre primeiro).", ['u:acidental']),
    (6, 'Combinações', 'Complete.', "___ vio salir del banco a las tres. (impessoal, a ele)", ["Se le", "Le se", "Se se", "Se lo le"], "Se le",
     "Impessoal com pessoa: <b>se le vio</b> (forma majoritária; em partes da América, <i>se lo vio</i>).", ['u:impersonal']),
    (6, 'Combinações', 'Qual frase está correta?', '', ["Se me rompió el móvil.", "Me se rompió el móvil.", "Se me rompí el móvil.", "Se rompió me el móvil."],
     "Se me rompió el móvil.", "Ordem fixa: <b>se + me</b> + verbo concordando com a coisa.", ['u:acidental']),
    (6, 'Combinações', 'Em “Se lo di”, o <i>se</i> é:', '', ["Substituto de le/les", "Reflexivo", "Passivo", "Impessoal"], "Substituto de le/les",
     "Aqui o se não tem nada de reflexivo: só substitui <i>le</i> antes de <i>lo</i>.", ['u:lele']),
]
for lv, k, q, s, opts, ans, x, v in HAND:
    B.mc(lv, k, q, s, opts, ans, x, v, 'hand')

# ------------------------------------------------------------------ seleção
ids = [u[0] for u in USES] + [v['id'] for v in VERBS]
chosen, cnt = select(B.items, ids, minc=6, targets={1: 160, 2: 210, 3: 210, 4: 180, 5: 160, 6: 140}, cap_per_entry=400, seed=5, gen_cap=0.3, always_gens=('hand', 'SS', 'SS2', 'RR', 'LE4', 'EN2'))
out = finalize(chosen, seed=9)
outdir = sys.argv[1] if len(sys.argv) > 1 else '.'
json.dump(out, open(os.path.join(outdir, 'usos-se.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
fc = Counter(v for q in out for v in q['v'])
gloss = [dict(id=u[0], v=u[1], cat='Os usos do se', kind='uso', pt=u[2], ex=u[3], note=u[4], base='', base_pt='', n=fc.get(u[0], 0)) for u in USES]
gloss += [dict(id=v['id'], v=v['name'], cat=v['cat'], kind='verbo', pt=v['pt'], ex=v['ex'], note='', base='', base_pt='', n=fc.get(v['id'], 0)) for v in VERBS]
json.dump(gloss, open(os.path.join(outdir, 'usos-se-verbos.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('candidatas:', len(B.items), '| escolhidas:', len(out), '| por nível:', dict(sorted(Counter(q['lv'] for q in out).items())), file=sys.stderr)
print('tipos:', dict(Counter(q['k'] for q in out).most_common()), file=sys.stderr)
print('cobertura (usos):', {u[1]: fc.get(u[0], 0) for u in USES}, file=sys.stderr)
print('mín. por verbo citado:', min(fc.get(v['id'], 0) for v in VERBS), file=sys.stderr)
