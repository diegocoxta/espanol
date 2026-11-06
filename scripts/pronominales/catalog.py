# -*- coding: utf-8 -*-
"""Catálogo completo dos verbos dos três materiais de referência.

GUSTAR: verbos e expressões em que a coisa é o sujeito e a pessoa vai no pronome.
PRON:   verbos pronominais/reflexivos/recíprocos/de ênfase (o verbo concorda com a pessoa).

Flags de GUSTAR:
  safe  → 'le/les' é a única forma normativa na 3ª pessoa (pode virar questão de escolher o pronome)
  psy   → verbo psicológico: na 3ª pessoa alterna le/lo-la; só usamos 1ª/2ª pessoa onde a escolha importa
  tr    → transitivo: na 3ª pessoa a pessoa é OD (lo/la) e o adjetivo concorda com ela
  se    → construção com 'se' (se me antoja, se me ocurrió…)
"""

# --------------------------------------------------------------------------- GUSTAR
GUSTAR = []

def g(name, head, cat, pt, S, Pl, ex, extra='', cls='', flags='', note='', tier=2):
    GUSTAR.append(dict(id='g:' + name, name=name, head=head, cat=cat, pt=pt, S=S, P=Pl, ex=ex,
                       extra=extra, cls=cls, flags=flags, note=note, tier=tier, kind='gustar'))

C1 = 'Gostar, interesse e atração'
g('gustar', 'gustar', C1, 'gostar', ['el mar', 'el café', 'bailar'], ['los gatos', 'las películas de terror'], 'me gusta el mar', flags='safe', tier=1)
g('encantar', 'encantar', C1, 'adorar', ['bailar', 'el cine'], ['los conciertos', 'las playas del norte'], 'me encanta bailar', flags='safe', tier=1)
g('fascinar', 'fascinar', C1, 'fascinar', ['la historia', 'el mar'], ['los dinosaurios', 'las ciudades antiguas'], 'me fascina la historia', flags='psy', tier=1)
g('apasionar', 'apasionar', C1, 'apaixonar', ['la música', 'el fútbol'], ['los libros de viajes', 'las motos'], 'me apasiona la música', flags='psy')
g('entusiasmar', 'entusiasmar', C1, 'entusiasmar', ['el proyecto', 'la idea de mudarnos'], ['los nuevos retos', 'las fiestas'], 'me entusiasma el proyecto', flags='psy')
g('chiflar', 'chiflar', C1, 'ser louco por', ['el chocolate', 'viajar'], ['los gatos', 'las series coreanas'], 'me chiflan los gatos', flags='safe', note='coloquial', tier=3)
g('flipar', 'flipar', C1, 'adorar, pirar', ['esa banda', 'el skate'], ['los videojuegos', 'las motos'], 'me flipa esa banda', flags='safe', note='coloquial, Espanha', tier=3)
g('agradar', 'agradar', C1, 'agradar', ['tu actitud', 'la propuesta'], ['los cambios', 'las sorpresas'], 'me agrada tu actitud', flags='safe')
g('desagradar', 'desagradar', C1, 'desagradar', ['el calor', 'la mentira'], ['las prisas', 'los ruidos fuertes'], 'me desagrada el calor', flags='safe')
g('disgustar', 'disgustar', C1, 'desagradar', ['la mentira', 'su actitud'], ['las injusticias', 'los gritos'], 'me disgusta la mentira', flags='safe', note='falso amigo: não é “desgostar” no sentido de entristecer')
g('atraer', 'atraer', C1, 'atrair', ['la idea', 'el riesgo'], ['los deportes extremos', 'las ciudades grandes'], 'me atrae la idea', flags='psy')
g('interesar', 'interesar', C1, 'interessar', ['la política', 'aprender idiomas'], ['las noticias', 'los documentales'], 'me interesa la política', flags='safe', tier=1)
g('importar', 'importar', C1, 'importar', ['el dinero', 'la opinión de los demás'], ['los detalles', 'las formas'], 'no me importa', flags='safe', tier=1)
g('intrigar', 'intrigar', C1, 'intrigar', ['ese final', 'su silencio'], ['los misterios', 'las desapariciones'], 'me intriga ese final', flags='psy')
g('llamar la atención', 'llamar', C1, 'chamar a atenção', ['su voz', 'ese cuadro'], ['sus ojos', 'los colores'], 'me llama la atención su voz', extra='la atención', flags='safe')
g('tentar', 'tentar', C1, 'tentar', ['ese postre', 'la idea de dejarlo todo'], ['los dulces', 'las ofertas'], 'me tienta ese postre', cls='ie', flags='psy')
g('seducir', 'seducir', C1, 'seduzir', ['la idea de viajar', 'el peligro'], ['los viajes largos', 'las promesas'], 'me seduce la idea de viajar', flags='psy', tier=3)
g('enloquecer', 'enloquecer', C1, 'enlouquecer (de gosto)', ['el chocolate', 'ese perfume'], ['los zapatos', 'las motos'], 'me enloquece el chocolate', flags='psy', tier=3)
g('volver loco', 'volver', C1, 'deixar louco', ['esa canción', 'el chocolate'], ['los dulces', 'las series de misterio'], 'me vuelve loco esa canción', extra='loco', cls='ue', flags='tr adj', tier=3)

C2 = 'Emoções positivas'
for nm, pt, S, Pl, ex, cls in [
    ('alegrar', 'alegrar', ['verte', 'la noticia'], ['tus visitas', 'las buenas noticias'], 'me alegra verte', ''),
    ('divertir', 'divertir', ['ese programa', 'jugar con los niños'], ['sus chistes', 'las comedias'], 'me divierte ese programa', 'ie-i'),
    ('emocionar', 'emocionar', ['esa película', 'la música en directo'], ['las bodas', 'los reencuentros'], 'me emociona esa película', ''),
    ('ilusionar', 'animar, empolgar', ['el viaje', 'la idea de verte'], ['los nuevos proyectos', 'las vacaciones'], 'me ilusiona el viaje', ''),
    ('animar', 'animar', ['saber eso', 'el buen tiempo'], ['tus mensajes', 'las fiestas'], 'me anima saber eso', ''),
    ('motivar', 'motivar', ['el reto', 'aprender cosas nuevas'], ['los desafíos', 'las metas claras'], 'me motiva el reto', ''),
    ('inspirar', 'inspirar', ['su historia', 'el mar'], ['los grandes artistas', 'las montañas'], 'me inspira su historia', ''),
    ('conmover', 'comover', ['su gesto', 'esa carta'], ['las historias reales', 'los pequeños detalles'], 'me conmueve su gesto', 'ue'),
    ('enternecer', 'enternecer', ['ver a los niños', 'su torpeza'], ['los cachorros', 'las fotos de bebé'], 'me enternece ver a los niños', ''),
    ('impresionar', 'impressionar', ['su talento', 'el tamaño del edificio'], ['los rascacielos', 'las cataratas'], 'me impresiona su talento', ''),
    ('maravillar', 'maravilhar', ['el paisaje', 'su voz'], ['los fuegos artificiales', 'las auroras'], 'me maravilla el paisaje', ''),
    ('asombrar', 'assombrar, surpreender', ['su memoria', 'la rapidez del cambio'], ['sus conocimientos', 'las cifras'], 'me asombra su memoria', ''),
    ('sorprender', 'surpreender', ['la noticia', 'su respuesta'], ['los resultados', 'las coincidencias'], 'me sorprende la noticia', ''),
    ('satisfacer', 'satisfazer', ['el resultado', 'tu explicación'], ['los resultados', 'las condiciones'], 'me satisface el resultado', ''),
    ('complacer', 'agradar', ['anunciar el ganador', 'su respuesta'], ['sus avances', 'las mejoras'], 'me complace anunciar...', ''),
    ('halagar', 'lisonjear', ['tu comentario', 'su invitación'], ['tus palabras', 'los elogios'], 'me halaga tu comentario', ''),
    ('tranquilizar', 'tranquilizar', ['saberlo', 'tu voz'], ['tus palabras', 'las noticias del médico'], 'me tranquiliza saberlo', ''),
    ('relajar', 'relaxar', ['el mar', 'leer antes de dormir'], ['los baños calientes', 'las caminatas'], 'me relaja el mar', ''),
    ('reconfortar', 'reconfortar', ['tu apoyo', 'una sopa caliente'], ['tus palabras', 'los abrazos'], 'me reconforta tu apoyo', ''),
    ('enorgullecer', 'dar orgulho', ['tu trabajo', 'el premio de mi hija'], ['tus logros', 'los resultados del equipo'], 'me enorgullece tu trabajo', ''),
    ('entretener', 'entreter', ['leer', 'ese juego'], ['los crucigramas', 'las series policíacas'], 'me entretiene leer', ''),
]:
    g(nm, nm, C2, pt, S, Pl, ex, cls=cls, flags='psy')

C3 = 'Emoções negativas'
for nm, pt, S, Pl, ex, cls, fl in [
    ('molestar', 'incomodar', ['el ruido', 'madrugar'], ['los mosquitos', 'las mentiras'], 'me molesta el ruido', '', 'psy'),
    ('fastidiar', 'chatear', ['esperar', 'el ruido'], ['las colas', 'los atascos'], 'me fastidia esperar', '', 'psy'),
    ('irritar', 'irritar', ['su tono', 'la injusticia'], ['las mentiras', 'los gritos'], 'me irrita su tono', '', 'psy'),
    ('enfadar', 'irritar, zangar', ['la injusticia', 'perder'], ['las mentiras', 'los retrasos'], 'me enfada la injusticia', '', 'psy'),
    ('enojar', 'irritar, zangar', ['la injusticia', 'esperar tanto'], ['las mentiras', 'los abusos'], 'me enoja que mientan', '', 'psy'),
    ('cabrear', 'deixar furioso', ['perder', 'la espera'], ['las injusticias', 'los atascos'], 'me cabrea perder', '', 'psy'),
    ('indignar', 'indignar', ['la corrupción', 'su actitud'], ['los abusos', 'las desigualdades'], 'me indigna la corrupción', '', 'psy'),
    ('ofender', 'ofender', ['ese chiste', 'su comentario'], ['sus bromas', 'las críticas injustas'], 'me ofende ese chiste', '', 'psy'),
    ('preocupar', 'preocupar', ['el examen', 'la salud de la abuela'], ['los precios', 'las notas'], 'me preocupa el examen', '', 'psy'),
    ('inquietar', 'inquietar', ['el silencio', 'su ausencia'], ['los ruidos de noche', 'las noticias'], 'me inquieta el silencio', '', 'psy'),
    ('angustiar', 'angustiar', ['la espera', 'no saber nada'], ['las deudas', 'los hospitales'], 'me angustia la espera', '', 'psy'),
    ('agobiar', 'sufocar, sobrecarregar', ['el tráfico', 'tanto trabajo'], ['las multitudes', 'los plazos'], 'me agobia el tráfico', '', 'psy'),
    ('estresar', 'estressar', ['el trabajo', 'conducir en la ciudad'], ['los exámenes', 'las mudanzas'], 'me estresa el trabajo', '', 'psy'),
    ('desesperar', 'desesperar', ['la lentitud', 'esperar'], ['las colas', 'los trámites'], 'me desespera la lentitud', '', 'psy'),
    ('asustar', 'assustar', ['la oscuridad', 'volar'], ['las arañas', 'los truenos'], 'me asustan las arañas', '', 'psy'),
    ('espantar', 'espantar, horrorizar', ['la violencia', 'la idea'], ['las arañas', 'los ratones'], 'me espanta la violencia', '', 'psy'),
    ('aterrar', 'aterrorizar', ['volar', 'la idea de perderte'], ['las alturas', 'los tiburones'], 'me aterra volar', '', 'psy'),
    ('horrorizar', 'horrorizar', ['la guerra', 'la crueldad'], ['las guerras', 'los accidentes'], 'me horroriza la guerra', '', 'psy'),
    ('entristecer', 'entristecer', ['la noticia', 'la lluvia'], ['las despedidas', 'los domingos por la tarde'], 'me entristece la noticia', '', 'psy'),
    ('apenar', 'entristecer', ['tu situación', 'su soledad'], ['las despedidas', 'sus problemas'], 'me apena tu situación', '', 'psy'),
    ('deprimir', 'deprimir', ['el invierno', 'la lluvia'], ['los días grises', 'las malas noticias'], 'me deprime el invierno', '', 'psy'),
    ('doler (emocional)', 'magoar', ['lo que dijiste', 'su indiferencia'], ['sus palabras', 'las mentiras'], 'me duele lo que dijiste', 'ue', 'safe'),
    ('decepcionar', 'decepcionar', ['su actitud', 'el final'], ['los políticos', 'las promesas incumplidas'], 'me decepciona su actitud', '', 'psy'),
    ('defraudar', 'decepcionar', ['el final', 'su respuesta'], ['los resultados', 'las promesas'], 'me defraudó el final', '', 'psy'),
    ('frustrar', 'frustrar', ['no entender', 'perder'], ['los errores tontos', 'las esperas'], 'me frustra no entender', '', 'psy'),
    ('avergonzar', 'envergonhar', ['hablar en público', 'su comportamiento'], ['sus gritos', 'las fotos de niño'], 'me avergüenza hablar en público', 'üe', 'psy'),
    ('humillar', 'humilhar', ['su desprecio', 'perder así'], ['sus burlas', 'las críticas en público'], 'me humilla su desprecio', '', 'tr'),
    ('aburrir', 'entediar', ['esa serie', 'esperar'], ['las reuniones', 'los discursos largos'], 'me aburre esa serie', '', 'psy'),
    ('cansar', 'cansar', ['repetirlo', 'el viaje'], ['las reuniones largas', 'los viajes'], 'me cansa repetirlo', '', 'psy'),
    ('hartar', 'encher o saco', ['tu queja', 'tanta burocracia'], ['tus quejas', 'las excusas'], 'me harta tu queja', '', 'psy'),
    ('repugnar', 'repugnar', ['ese olor', 'la mentira'], ['las cucarachas', 'los olores fuertes'], 'me repugna ese olor', '', 'safe'),
    ('asquear', 'dar nojo', ['la hipocresía', 'ese olor'], ['las cucarachas', 'los mentirosos'], 'me asquea la hipocresía', '', 'psy'),
    ('chocar', 'chocar', ['su respuesta', 'la noticia'], ['sus palabras', 'las imágenes'], 'me chocó su respuesta', '', 'safe'),
    ('escandalizar', 'escandalizar', ['el precio', 'su descaro'], ['los precios', 'sus declaraciones'], 'me escandaliza el precio', '', 'psy'),
    ('extrañar', 'achar estranho', ['su silencio', 'que no llame'], ['sus ausencias', 'los cambios'], 'me extraña que no llame', '', 'safe'),
    ('perturbar', 'perturbar', ['esa imagen', 'el silencio'], ['esas imágenes', 'los recuerdos'], 'me perturba esa imagen', '', 'psy'),
    ('obsesionar', 'obcecar', ['el orden', 'la limpieza'], ['los detalles', 'las cifras'], 'me obsesiona el orden', '', 'psy'),
    ('pesar', 'pesar, lamentar', ['haberlo dicho', 'no haberla visitado'], ['los años', 'sus palabras'], 'me pesa haberlo dicho', '', 'safe'),
]:
    g(nm, nm.split(' ')[0], C3, pt, S, Pl, ex, cls=cls, flags=fl,
      tier=1 if nm in ('molestar', 'preocupar', 'aburrir') else 2)
g('dar asco', 'dar', C3, 'dar nojo', ['la leche cortada', 'ese olor'], ['las cucarachas', 'los gusanos'], 'me da asco la leche cortada', extra='asco', flags='safe')

C4 = 'Corpo e sensações'
for nm, head, extra, pt, S, Pl, ex, cls in [
    ('doler', 'doler', '', 'doer', ['la cabeza', 'la espalda'], ['los pies', 'las muelas'], 'me duele la cabeza', 'ue'),
    ('picar', 'picar', '', 'coçar, arder', ['la nariz', 'la garganta'], ['los ojos', 'las piernas'], 'me pica la nariz', ''),
    ('arder', 'arder', '', 'arder', ['la herida', 'la garganta'], ['los ojos', 'las mejillas'], 'me arden los ojos', ''),
    ('escocer', 'escocer', '', 'arder (ferida)', ['la herida', 'la piel'], ['los ojos', 'las rodillas'], 'me escuece la herida', 'ue'),
    ('sangrar', 'sangrar', '', 'sangrar', ['la nariz', 'el dedo'], ['las encías', 'los nudillos'], 'me sangra la nariz', ''),
    ('temblar', 'temblar', '', 'tremer', ['la voz', 'la pierna'], ['las manos', 'las rodillas'], 'me tiemblan las manos', 'ie'),
    ('sudar', 'sudar', '', 'suar', ['la frente', 'la espalda'], ['las manos', 'los pies'], 'me sudan las manos', ''),
    ('zumbar', 'zumbar', '', 'zumbir', ['el oído', 'la cabeza'], ['los oídos'], 'me zumban los oídos', ''),
    ('crujir', 'crujir', '', 'estalar', ['la rodilla', 'la espalda'], ['las rodillas', 'los huesos'], 'me crujen las rodillas', ''),
    ('sonar (las tripas)', 'sonar', '', 'roncar (a barriga)', ['el estómago'], ['las tripas'], 'me suenan las tripas', 'ue'),
    ('dar sueño', 'dar', 'sueño', 'dar sono', ['leer en la cama', 'el calor'], ['las películas lentas', 'los viajes en tren'], 'me da sueño leer en la cama', ''),
    ('dar hambre', 'dar', 'hambre', 'dar fome', ['el olor', 'nadar'], ['los olores de la cocina', 'las caminatas'], 'me da hambre el olor', ''),
    ('dar sed', 'dar', 'sed', 'dar sede', ['la sal', 'el calor'], ['las patatas fritas', 'los embutidos'], 'me da sed la sal', ''),
    ('dar frío', 'dar', 'frío', 'dar frio', ['el aire acondicionado', 'el viento'], ['los días nublados', 'las casas viejas'], 'me da frío el aire', ''),
    ('dar calor', 'dar', 'calor', 'dar calor', ['el jersey', 'la lana'], ['los abrigos', 'las mantas'], 'me da calor el jersey', ''),
    ('dar alergia', 'dar', 'alergia', 'dar alergia', ['el polvo', 'el polen'], ['los gatos', 'las nueces'], 'me da alergia el polvo', ''),
    ('dar náuseas', 'dar', 'náuseas', 'dar enjoo', ['el olor a gasolina', 'viajar en barco'], ['los barcos', 'las curvas'], 'me dan náuseas los barcos', ''),
    ('sentar bien / mal (comida)', 'sentar', 'mal', 'cair bem / mal (comida)', ['la leche', 'el café'], ['los fritos', 'las comidas pesadas'], 'me sienta mal la leche', 'ie'),
]:
    g(nm, head, C4, pt, S, Pl, ex, extra=extra, cls=cls, flags='safe', tier=1 if nm == 'doler' else 2)

C5 = 'Quantidade, necessidade e conveniência'
for nm, head, extra, pt, S, Pl, ex, cls, fl in [
    ('faltar', 'faltar', '', 'faltar', ['tiempo', 'dinero'], ['dos sillas', 'ideas'], 'me falta tiempo', '', 'safe'),
    ('sobrar', 'sobrar', '', 'sobrar', ['comida', 'dinero'], ['dos entradas', 'sillas'], 'me sobra comida', '', 'safe'),
    ('quedar (restar)', 'quedar', '', 'restar', ['poco dinero', 'una semana'], ['dos días', 'tres exámenes'], 'me quedan dos días', '', 'safe'),
    ('bastar', 'bastar', '', 'bastar', ['tu palabra', 'un café'], ['dos horas', 'tres días'], 'me basta con eso', '', 'safe'),
    ('alcanzar', 'alcanzar', '', 'ser suficiente', ['el dinero', 'el tiempo'], ['los ahorros', 'las sillas'], 'no me alcanza el dinero', '', 'safe'),
    ('hacer falta', 'hacer', 'falta', 'fazer falta, precisar', ['dormir', 'un abrigo'], ['unas vacaciones', 'dos sillas más'], 'me hace falta dormir', '', 'safe'),
    ('urgir', 'urgir', '', 'ser urgente', ['hablar contigo', 'el informe'], ['los cambios', 'las reformas'], 'me urge hablar contigo', '', 'safe'),
    ('convenir', 'convenir', '', 'convir', ['salir temprano', 'el horario de mañana'], ['los cambios', 'las rebajas'], 'me conviene salir temprano', '', 'safe'),
    ('servir', 'servir', '', 'servir', ['esta llave', 'el paraguas roto'], ['estas llaves', 'los consejos'], 'no me sirve esta llave', 'i', 'safe'),
    ('funcionar', 'funcionar', '', 'funcionar', ['el wifi', 'el móvil'], ['los frenos', 'las luces'], 'no me funciona el wifi', '', 'safe'),
    ('costar', 'costar', '', 'custar, ser difícil', ['madrugar', 'el inglés'], ['las matemáticas', 'los cambios'], 'me cuesta madrugar', 'ue', 'safe'),
    ('resultar (fácil/difícil)', 'resultar', '', 'ser (fácil/difícil)', ['fácil el inglés', 'difícil madrugar'], ['fáciles los idiomas', 'difíciles las matemáticas'], 'me resulta fácil el inglés', '', 'safe'),
    ('tocar', 'tocar', '', 'ser a vez de', ['pagar', 'conducir'], ['los turnos de noche', 'las tareas difíciles'], 'me toca a mí', '', 'safe'),
    ('corresponder', 'corresponder', '', 'caber, competir', ['decidir', 'esa tarea'], ['estas decisiones', 'esos gastos'], 'no me corresponde decidir', '', 'safe'),
    ('pertenecer', 'pertenecer', '', 'pertencer', ['esta casa', 'el coche'], ['estas tierras', 'los libros'], 'esto no me pertenece', '', 'safe'),
    ('incumbir', 'incumbir', '', 'ser da conta de', ['eso', 'ese asunto'], ['esos asuntos', 'las decisiones del equipo'], 'eso no me incumbe', '', 'safe'),
    ('afectar', 'afectar', '', 'afetar', ['el cambio de horario', 'el calor'], ['los cambios', 'las críticas'], 'me afecta el cambio de horario', '', 'tr'),
    ('perjudicar', 'perjudicar', '', 'prejudicar', ['la decisión', 'el humo'], ['los recortes', 'las nuevas normas'], 'me perjudica la decisión', '', 'tr'),
    ('beneficiar', 'beneficiar', '', 'beneficiar', ['el descuento', 'la nueva ley'], ['los descuentos', 'las ayudas'], 'me beneficia el descuento', '', 'tr'),
]:
    g(nm, head, C5, pt, S, Pl, ex, extra=extra, cls=cls, flags=fl, tier=1 if nm in ('faltar', 'sobrar', 'quedar (restar)') else 2)

C6 = 'Opinião, avaliação e vontade'
for nm, head, extra, pt, S, Pl, ex, cls, fl, note, tier in [
    ('parecer', 'parecer', '', 'achar, parecer', ['bien la idea', 'caro el hotel'], ['caros los precios', 'interesantes las clases'], 'me parece bien', '', 'safe', '', 1),
    ('caer bien / mal', 'caer', 'bien', 'simpatizar ou não', ['tu hermano', 'el jefe'], ['tus amigos', 'los vecinos'], 'ese tipo me cae mal', '', 'safe', '', 1),
    ('caer gordo', 'caer', 'gordo', 'não ir com a cara', ['su jefe', 'ese presentador'], [], 'me cae gordo su jefe', '', 'safe', 'coloquial', 3),
    ('apetecer', 'apetecer', '', 'dar vontade', ['un helado', 'salir esta noche'], ['unas tapas', 'unas vacaciones'], 'me apetece un helado', '', 'safe', '', 1),
    ('antojarse', 'antojar', '', 'dar vontade de repente', ['un café', 'ir a la playa'], ['unas fresas', 'unos tacos'], 'se me antoja un café', '', 'safe se', '', 2),
    ('provocar', 'provocar', '', 'dar vontade', ['una cerveza', 'salir'], ['unas empanadas', 'unos tacos'], 'me provoca una cerveza', '', 'safe', 'Colômbia, Peru', 3),
    ('sonar (familiar)', 'sonar', '', 'soar, parecer familiar', ['tu cara', 'ese nombre'], ['esas caras', 'sus apellidos'], 'me suena tu cara', 'ue', 'safe', '', 2),
    ('sonar bien / mal', 'sonar', 'bien', 'soar bem / mal', ['el plan', 'la idea'], ['tus planes', 'esas propuestas'], 'me suena bien el plan', 'ue', 'safe', '', 2),
    ('ocurrir (ideia)', 'ocurrir', '', 'ocorrer (ideia)', ['una idea', 'algo mejor'], ['varias ideas', 'dos soluciones'], 'se me ocurrió una idea', '', 'safe se', '', 2),
    ('olvidar (involuntário)', 'olvidar', '', 'esquecer', ['la llave', 'su cumpleaños'], ['las llaves', 'los deberes'], 'se me olvidó la llave', '', 'safe se', '', 2),
    ('pasar', 'pasar', '', 'acontecer', ['algo raro', 'eso'], ['cosas raras', 'esas cosas'], '¿qué te pasa?', '', 'safe', '', 1),
    ('suceder', 'suceder', '', 'acontecer', ['eso', 'lo mismo'], ['esas cosas', 'cosas raras'], 'me sucede a menudo', '', 'safe', '', 2),
    ('dar igual', 'dar', 'igual', 'tanto faz', ['eso', 'el color'], ['las críticas', 'sus opiniones'], 'me da igual', '', 'safe', '', 1),
    ('dar lo mismo', 'dar', 'lo mismo', 'dar no mesmo', ['el color', 'ir hoy o mañana'], ['los detalles', 'las críticas'], 'me da lo mismo', '', 'safe', '', 2),
    ('dar exactamente igual', 'dar', 'exactamente igual', 'não fazer diferença', ['lo que digan', 'eso'], ['sus opiniones', 'los rumores'], 'me da exactamente igual', '', 'safe', '', 2),
    ('dar pena', 'dar', 'pena', 'dar pena; vergonha (Am. Lat.)', ['pedirlo', 'ese perro'], ['los animales abandonados', 'esas historias'], 'me da pena pedirlo', '', 'safe', '', 2),
    ('dar vergüenza', 'dar', 'vergüenza', 'dar vergonha', ['cantar', 'hablar en público'], ['sus gritos', 'las fotos de niño'], 'me da vergüenza cantar', '', 'safe', '', 2),
    ('dar rabia', 'dar', 'rabia', 'dar raiva', ['perder', 'la injusticia'], ['las mentiras', 'los abusos'], 'me da rabia perder', '', 'safe', '', 2),
    ('dar envidia', 'dar', 'envidia', 'dar inveja', ['tu viaje', 'su suerte'], ['tus vacaciones', 'sus fotos'], 'me da envidia tu viaje', '', 'safe', '', 2),
    ('dar lástima', 'dar', 'lástima', 'dar dó', ['el perro', 'su situación'], ['los animales abandonados', 'esas personas'], 'me da lástima el perro', '', 'safe', '', 2),
    ('dar flojera / pereza', 'dar', 'pereza', 'dar preguiça', ['salir', 'madrugar'], ['las reuniones', 'los lunes'], 'me da pereza salir', '', 'safe', 'flojera: México', 2),
    ('dar curiosidad', 'dar', 'curiosidad', 'dar curiosidade', ['el final', 'su pasado'], ['sus viajes', 'las culturas antiguas'], 'me da curiosidad el final', '', 'safe', '', 2),
    ('dar risa', 'dar', 'risa', 'dar vontade de rir', ['su acento', 'ese vídeo'], ['sus chistes', 'las fotos de antes'], 'me da risa su acento', '', 'safe', '', 2),
    ('dar miedo', 'dar', 'miedo', 'dar medo', ['la oscuridad', 'volar'], ['las arañas', 'los perros grandes'], 'me da miedo la oscuridad', '', 'safe', '', 1),
]:
    g(nm, head, C6, pt, S, Pl, ex, extra=extra, cls=cls, flags=fl, note=note, tier=tier)
g('dar ganas', 'dar', C6, 'dar vontade', ['esta canción', 'el sol'], ['estas canciones', 'sus chistes'], 'me dan ganas de llorar', extra='ganas de bailar', flags='safe', tier=2)
GUSTAR[-1]['custom'] = True  # sentenças próprias (ver gen: 'dar ganas')

C7 = 'Expressões com ir, quedar, sentar e hacer'
for nm, head, extra, pt, S, Pl, ex, cls, fl in [
    ('ir bien / mal', 'ir', 'bien', 'ir bem / mal', ['el trabajo', 'el negocio'], ['los estudios', 'las cosas'], 'me va bien en el trabajo', '', 'safe'),
    ('quedar bien / mal (roupa)', 'quedar', 'bien', 'ficar bem / mal (roupa)', ['la camisa', 'ese color'], ['los pantalones', 'las gafas'], 'te queda bien la camisa', '', 'safe'),
    ('quedar grande / pequeño', 'quedar', '', 'ficar grande / pequeno', ['grande el pantalón', 'pequeña la chaqueta'], ['pequeñas las botas', 'grandes los zapatos'], 'me queda grande el pantalón', '', 'safe'),
    ('quedar lejos / cerca', 'quedar', '', 'ficar longe / perto', ['lejos la oficina', 'cerca el colegio'], ['lejos las tiendas', 'cerca los bancos'], 'me queda lejos la oficina', '', 'safe'),
    ('sentar bien / mal (roupa)', 'sentar', 'bien', 'cair bem / mal', ['el azul', 'ese vestido'], ['los colores claros', 'las faldas largas'], 'te sienta bien el azul', 'ie', 'safe'),
    ('sentar bien / mal (atitude)', 'sentar', 'mal', 'cair bem / mal', ['su comentario', 'la broma'], ['sus palabras', 'las críticas'], 'me sentó mal su comentario', 'ie', 'safe'),
    ('hacer gracia', 'hacer', 'gracia', 'achar graça', ['su forma de hablar', 'ese chiste'], ['sus chistes', 'las ocurrencias del niño'], 'me hace gracia su forma de hablar', '', 'safe'),
    ('hacer ilusión', 'hacer', 'ilusión', 'deixar animado', ['verte', 'el viaje'], ['las fiestas', 'los regalos sorpresa'], 'me hace ilusión verte', '', 'safe'),
    ('hacer daño', 'hacer', 'daño', 'machucar, fazer mal', ['el zapato izquierdo', 'la luz fuerte'], ['los zapatos', 'las gafas'], 'me hacen daño los zapatos', '', 'safe'),
    ('hacer feliz', 'hacer', 'feliz', 'fazer feliz', ['cocinar', 'tu visita'], ['tus mensajes', 'las cosas sencillas'], 'me hace feliz cocinar', '', 'tr adj'),
    ('traer recuerdos', 'traer', 'recuerdos', 'trazer lembranças', ['esa canción', 'este olor'], ['estas fotos', 'esos lugares'], 'me trae recuerdos esa canción', '', 'safe'),
    ('traer sin cuidado', 'traer', 'sin cuidado', 'não importar nem um pouco', ['lo que digan', 'su opinión'], ['sus críticas', 'los rumores'], 'me trae sin cuidado', '', 'safe'),
    ('tener sin cuidado', 'tener', 'sin cuidado', 'não importar', ['lo que digan', 'su opinión'], ['las críticas', 'los rumores'], 'me tiene sin cuidado lo que digan', '', 'tr'),
    ('tener harto', 'tener', 'harto', 'deixar de saco cheio', ['el ruido', 'tanta burocracia'], ['sus quejas', 'los atascos'], 'me tiene harto el ruido', '', 'tr adj'),
    ('poner nervioso', 'poner', 'nervioso', 'deixar nervoso', ['esperar', 'el examen'], ['los aviones', 'las entrevistas'], 'me pone nervioso esperar', '', 'tr adj'),
    ('poner triste / contento', 'poner', 'triste', 'deixar triste / contente', ['la lluvia', 'su carta'], ['los domingos', 'las despedidas'], 'me pone triste la lluvia', '', 'tr adj'),
    ('poner de mal humor', 'poner', 'de mal humor', 'deixar de mau humor', ['el tráfico', 'madrugar'], ['los lunes', 'las colas'], 'me pone de mal humor el tráfico', '', 'tr'),
    ('sacar de quicio', 'sacar', 'de quicio', 'tirar do sério', ['su actitud', 'el ruido'], ['sus excusas', 'los retrasos'], 'me saca de quicio su actitud', '', 'tr'),
    ('caer en gracia', 'caer', 'en gracia', 'cair nas graças', ['el niño', 'su sinceridad'], ['sus bromas', 'los nuevos vecinos'], 'me cayó en gracia el niño', '', 'safe'),
]:
    g(nm, head, C7, pt, S, Pl, ex, extra=extra, cls=cls, flags=fl, tier=2)
g('ir (¿cómo te va?)', 'ir', C7, 'estar indo', ['todo', 'el trabajo'], ['las cosas', 'los estudios'], '¿cómo te va?', flags='safe', tier=1)
GUSTAR[-1]['custom'] = True
g('darse bien / mal', 'dar', C6, 'ser bom / ruim em algo', ['cocinar', 'el inglés'], ['las matemáticas', 'los idiomas'], 'se me da bien cocinar', extra='bien', flags='safe se', tier=2)

# --------------------------------------------------------------------------- PRONOMINAIS
PRON = []

def p(name, cls, grp, cat, pt, tails, prep='', aff=None, neg=None, ex='', subj=None, flags='', base=None, base_pt='', base_ex='', tier=2, inf=None):
    infv = inf or (name.split(' ')[0])
    verb = infv[:-2] if infv.endswith('se') else infv
    PRON.append(dict(id='p:' + name, name=name, verb=verb, cls=cls, grp=grp, cat=cat, pt=pt, tails=tails, prep=prep,
                     aff=aff, neg=neg, ex=ex, subj=subj, flags=flags, base=base, base_pt=base_pt, base_ex=base_ex,
                     tier=tier, kind='pron'))

K1 = 'Só existem com pronome'
for a in [
    ('arrepentirse', 'ie-i', 'arrepender-se', ['de nada', 'de esa decisión', 'de haberlo dicho'], 'de', None, 'de nada', 'me arrepiento de nada', 1),
    ('quejarse', '', 'queixar-se', ['de todo', 'del ruido', 'del servicio'], 'de', 'al encargado', 'tanto', 'se queja de todo', 1),
    ('atreverse', '', 'atrever-se', ['a saltar', 'a hablar en público', 'a decir la verdad'], 'a', 'a intentarlo', 'a tocarlo', 'no me atrevo a saltar', 1),
    ('jactarse', '', 'gabar-se', ['de ser rico', 'de sus contactos', 'de no estudiar nunca'], 'de', None, 'de eso', 'se jacta de ser rico', 3),
    ('vanagloriarse', '', 'vangloriar-se', ['de sus logros', 'de su fortuna', 'de su éxito'], 'de', None, None, 'se vanagloria de sus logros', 3),
    ('abstenerse', '', 'abster-se', ['de opinar', 'de votar', 'de comer carne'], 'de', 'de opinar', None, 'me abstengo de opinar', 2),
    ('adueñarse', '', 'apoderar-se', ['de la casa', 'del negocio familiar', 'de la situación'], 'de', None, None, 'se adueñó de la casa', 3),
    ('apropiarse', '', 'apropriar-se', ['de la idea', 'del dinero', 'de los méritos ajenos'], 'de', None, None, 'se apropió de la idea', 2),
    ('apoderarse', '', 'apoderar-se', ['del poder', 'de la ciudad', 'de las joyas'], 'de', None, None, 'el miedo se apoderó de mí', 3),
    ('dignarse', '', 'dignar-se', ['a contestar', 'a saludar', 'a mirarnos'], 'a', None, None, 'ni se dignó a contestar', 3),
    ('desmayarse', '', 'desmaiar', ['del calor', 'en el metro', 'al ver la sangre'], '', None, None, 'me desmayé del calor', 2),
    ('percatarse', '', 'perceber', ['del error', 'de su ausencia', 'del peligro'], 'de', None, None, 'no me percaté del error', 3),
    ('fugarse', '', 'fugir', ['de la cárcel', 'de casa', 'con su novio'], 'de', None, None, 'se fugó de la cárcel', 2),
    ('inmiscuirse', '', 'intrometer-se', ['en eso', 'en asuntos ajenos', 'en la vida de los demás'], 'en', None, 'en eso', 'no te inmiscuyas en eso', 3),
    ('ensimismarse', '', 'absorver-se', ['leyendo', 'en sus pensamientos', 'mirando el mar'], '', None, None, 'se ensimisma leyendo', 3),
    ('obstinarse', '', 'obstinar-se', ['en tener razón', 'en hacerlo solo', 'en no pedir ayuda'], 'en', None, None, 'se obstina en tener razón', 3),
    ('empecinarse', '', 'teimar', ['en ir', 'en llevar la contraria', 'en repetirlo'], 'en', None, None, 'se empecinó en ir', 3),
    ('esforzarse', 'ue', 'esforçar-se', ['por mejorar', 'por entenderlo', 'por llegar a tiempo'], 'por', 'un poco más', None, 'me esfuerzo por mejorar', 2),
    ('resignarse', '', 'resignar-se', ['a perder', 'a su suerte', 'a esperar'], 'a', None, None, 'me resigné a perder', 2),
    ('rebelarse', '', 'rebelar-se', ['contra el jefe', 'contra las normas', 'contra la injusticia'], 'contra', None, None, 'se rebeló contra el jefe', 2),
    ('desentenderse', 'ie', 'lavar as mãos', ['del problema', 'de sus hijos', 'de las cuentas'], 'de', None, 'del problema', 'se desentendió del problema', 3),
    ('enterarse', '', 'ficar sabendo', ['de la noticia', 'de todo', 'de los chismes del barrio'], 'de', 'bien de los horarios', None, 'me enteré ayer', 1),
    ('darse cuenta', '', 'perceber, dar-se conta', ['cuenta del error', 'cuenta de todo', 'cuenta tarde'], 'de', 'cuenta de que es tarde', None, 'me di cuenta tarde', 1),
    ('acurrucarse', '', 'aconchegar-se', ['en el sofá', 'junto a la chimenea', 'bajo la manta'], '', None, None, 'el gato se acurrucó', 3),
    ('agacharse', '', 'agachar-se', ['para recogerlo', 'detrás del coche', 'para pasar por la puerta'], '', 'un poco', None, 'me agaché para recogerlo', 2),
    ('arrodillarse', '', 'ajoelhar-se', ['ante el altar', 'para rezar', 'en el suelo'], '', None, None, 'se arrodilló ante el altar', 2),
    ('desperezarse', '', 'espreguiçar-se', ['al despertar', 'en la cama', 'después de la siesta'], '', None, None, 'me desperecé al despertar', 3),
    ('fiarse', 'í', 'confiar', ['de él', 'de los desconocidos', 'de las promesas'], 'de', None, 'de nadie', 'no me fío de él', 2),
    ('burlarse', '', 'zombar', ['de sus compañeros', 'de los políticos', 'de todo'], 'de', None, 'de él', 'se burlan de mí', 2),
]:
    name, cls, pt, tails, prep, aff, neg, ex, tier = a
    p(name, cls, 'so', K1, pt, tails, prep, aff, neg, ex, tier=tier,
      inf='darse' if name == 'darse cuenta' else None)
p('suicidarse', '', 'so', K1, 'suicidar-se', [], '', None, None, 'el personaje se suicida', flags='sensitive', tier=3)

K2 = 'Mudam de sentido com o pronome'
for a in [
    ('irse', '', 'ir embora', ['a casa', 'de la fiesta temprano', 'sin decir nada'], 'ya', 'todavía', 'me voy a casa', 'ir', 'ir', '—¡A cenar! —¡Ya voy!', 1),
    ('marcharse', '', 'ir embora', ['sin avisar', 'de la reunión', 'a otro país'], 'de aquí', 'todavía', 'se marchó sin avisar', 'marchar', 'marchar; funcionar', 'el negocio marcha bien', 2),
    ('dormirse', 'ue-u', 'pegar no sono', ['en el sofá', 'viendo la tele', 'en el autobús'], 'ya', 'en clase', 'me dormí en el sofá', 'dormir', 'dormir', 'duermo ocho horas', 1),
    ('quedarse', '', 'ficar', ['en casa', 'en un hotel del centro', 'sin palabras'], 'aquí', 'en casa', 'me quedé en casa', 'quedar', 'combinar, restar', 'quedé con Ana a las ocho', 1),
    ('acordarse', 'ue', 'lembrar', ['de tu cumpleaños', 'de aquel viaje', 'de todo'], 'de llamar a la abuela', None, 'no me acuerdo', 'acordar', 'combinar, acordar', 'acordaron un precio', 1),
    ('llevarse', '', 'levar embora; dar-se (bem/mal)', ['bien con su suegra', 'mal con los vecinos', 'todo el dinero'], 'el abrigo', 'mi paraguas', 'me llevo bien con él', 'llevar', 'levar', 'siempre llevo paraguas', 2),
    ('parecerse', '', 'parecer-se com', ['a su abuela', 'a un actor famoso', 'a su hermano mayor'], None, None, 'me parezco a mi padre', 'parecer', 'parecer', 'pareces cansado', 1),
    ('negarse', 'ie', 'recusar-se', ['a firmar', 'a contestar', 'a pagar la multa'], None, 'a intentarlo', 'me niego a firmar', 'negar', 'negar', 'negó las acusaciones', 2),
    ('despedirse', 'i', 'despedir-se', ['de todos', 'de sus amigos en la estación', 'con un abrazo'], 'de la abuela', None, 'me despedí de todos', 'despedir', 'demitir', 'la empresa despidió a diez empleados', 1),
    ('volverse', 'ue', 'tornar-se, virar-se', ['hacia la ventana', 'de repente hacia la puerta', 'más exigente con los años'], None, None, 'se volvió loco', 'volver', 'voltar', 'vuelvo a casa a las seis', 2),
    ('hacerse', '', 'tornar-se, fingir', ['rico con el negocio', 'el tonto cuando le conviene', 'vegetariano el año pasado'], None, 'el tonto', 'se hizo rico / se hace el tonto', 'hacer', 'fazer', 'hago la cena', 2),
    ('ponerse', '', 'ficar (estado); vestir', ['la chaqueta', 'de mal humor', 'a llorar con esa película'], 'el abrigo', 'así', 'me puse la chaqueta', 'poner', 'colocar', 'pongo las llaves en la mesa', 1),
    ('encontrarse', 'ue', 'sentir-se; encontrar alguém', ['mal hoy', 'con Pedro en el súper', 'mejor después de la siesta'], None, None, 'me encuentro mal', 'encontrar', 'achar', 'no encuentro mis gafas', 1),
    ('fijarse', '', 'reparar', ['en los detalles', 'en todo', 'en esa señal'], 'en eso', None, 'fíjate en eso', 'fijar', 'fixar', 'fijamos la fecha', 2),
    ('probarse', 'ue', 'provar (roupa)', ['el vestido', 'los zapatos nuevos', 'la chaqueta en la tienda'], 'esta camisa', None, 'me probé el vestido', 'probar', 'provar (comida)', 'prueba la paella', 1),
    ('meterse', '', 'entrar; intrometer-se', ['en el agua', 'en problemas', 'en la vida de los demás'], None, 'donde no te llaman', 'no te metas', 'meter', 'colocar dentro', 'metí la ropa en la maleta', 2),
    ('llamarse', '', 'chamar-se', [], None, None, 'me llamo Diego', 'llamar', 'chamar', 'llamo a mi madre', 1),
    ('ocuparse', '', 'cuidar de', ['de la cena', 'de los niños', 'de las cuentas'], 'de esto', None, 'yo me ocupo de eso', 'ocupar', 'ocupar', 'el sofá ocupa mucho espacio', 2),
    ('caerse', '', 'levar um tombo', ['en la calle', 'de la bici', 'por las escaleras'], None, None, 'me caí en la calle', 'caer', 'cair (figurado)', 'caí en la trampa', 1),
    ('salirse', '', 'vazar; sair de algo', ['del grupo de WhatsApp', 'de la carretera', 'del tema'], None, None, 'se salió el agua', 'salir', 'sair', 'salgo de casa a las ocho', 2),
    ('morirse', 'ue-u', 'morrer (coloq., ênfase)', ['de hambre', 'de risa', 'de ganas de verte'], None, None, 'me muero de hambre', 'morir', 'morrer', 'Cervantes murió en 1616', 2),
    ('comportarse', '', 'comportar-se', ['bien en clase', 'como un niño', 'con educación'], 'bien', None, 'pórtate bien', 'comportar', 'implicar', 'el cambio comporta riesgos', 2),
    ('portarse', '', 'comportar-se', ['mal en la fiesta', 'bien con los abuelos', 'como un adulto'], 'bien', 'mal', 'se portó mal', 'portar', 'portar', 'los soldados portaban armas', 2),
    ('aprovecharse', '', 'aproveitar-se', ['de su bondad', 'de la situación', 'de los turistas'], None, 'de nadie', 'se aprovechó de mí', 'aprovechar', 'aproveitar', 'aprovechamos el sol', 2),
    ('olvidarse', '', 'esquecer', ['de llamar', 'de la reunión', 'de todo'], 'de eso', 'de las llaves', 'me olvidé de llamar', 'olvidar', 'esquecer', 'olvidé su nombre', 1),
    ('darse', '', 'acontecer; dar-se bem', ['por vencido', 'un baño en el mar', 'un golpe en la rodilla'], 'prisa', 'por vencido', 'se me da bien cocinar', 'dar', 'dar', 'le di un regalo', 2),
    ('echarse', '', 'deitar-se; começar a', ['a llorar', 'a reír', 'una siesta'], 'una siesta', None, 'se echó a llorar', 'echar', 'jogar', 'eché la carta al buzón', 2),
    ('tirarse', '', 'atirar-se', ['a la piscina', 'al agua', 'en paracaídas'], None, 'al agua', 'se tiró a la piscina', 'tirar', 'jogar', 'tiré la basura', 2),
    ('plantearse', '', 'considerar', ['cambiar de trabajo', 'estudiar otra carrera', 'vender la casa'], None, None, 'me planteo cambiar de trabajo', 'plantear', 'propor', 'planteó una pregunta', 3),
    ('pasarse', '', 'exagerar; passar do ponto', ['con la sal', 'de la raya', 'tres pueblos'], None, 'con el azúcar', 'te pasaste', 'pasar', 'passar', 'pasamos las vacaciones en la playa', 2),
    ('perderse', 'ie', 'perder-se', ['en la ciudad', 'en el bosque', 'por el camino'], None, 'por ahí', 'me perdí en la ciudad', 'perder', 'perder', 'perdí el autobús', 1),
    ('decidirse', '', 'decidir-se', ['por fin', 'a cambiar de trabajo', 'por el rojo'], 'de una vez', None, 'por fin me decidí', 'decidir', 'decidir', 'el jurado decidió el ganador', 2),
    ('creerse', '', 'achar-se', ['muy listo', 'el mejor del equipo', 'superior a los demás'], None, None, 'se cree muy listo', 'creer', 'acreditar', 'no creo en fantasmas', 2),
    ('mudarse', '', 'mudar de casa', ['a Madrid', 'de piso', 'cerca del trabajo'], None, None, 'me mudé a Madrid', 'mudar', 'mudar (pele, pena)', 'la serpiente muda la piel', 1),
    ('conducirse', '', 'comportar-se', ['con respeto', 'con prudencia', 'con elegancia'], None, None, 'se condujo con respeto', 'conducir', 'dirigir', 'conduzco un camión', 3),
    ('deshacerse', '', 'livrar-se', ['de los muebles viejos', 'de la ropa usada', 'del coche'], 'de eso', None, 'me deshice de los muebles', 'deshacer', 'desfazer', 'deshice la maleta', 2),
    ('tratarse de', '', 'tratar-se de', [], None, None, 'se trata de un error', 'tratar', 'tratar', 'esta novela trata de la guerra', 2),
    ('callarse', '', 'calar-se', ['de repente', 'cuando entró el profesor', 'por miedo'], 'un momento', 'ahora', 'me callé', 'callar', 'calar (ocultar)', 'calló el nombre de su fuente', 1),
]:
    name, cls, pt, tails, aff, neg, ex, base, bpt, bex, tier = a
    fl = ''
    if name in ('volverse', 'hacerse', 'creerse'):
        fl = 'masc sg'
    if name in ('llamarse', 'tratarse de'):
        fl = 'special'
    p(name, cls, 'sen', K2, pt, tails, '', aff, neg, ex, flags=fl, base=base, base_pt=bpt, base_ex=bex, tier=tier,
      inf=('tratarse' if name == 'tratarse de' else None))
# preposições dos 'sen'
for e in PRON:
    if e['name'] in ('acordarse', 'olvidarse', 'ocuparse', 'deshacerse', 'despedirse', 'aprovecharse'):
        e['prep'] = 'de'
    if e['name'] in ('negarse', 'parecerse'):
        e['prep'] = 'a'
    if e['name'] == 'fijarse':
        e['prep'] = 'en'

K3 = 'Rotina e cuidado pessoal'
for a in [
    ('despertarse', 'ie', 'acordar', ['a las siete', 'con el despertador', 'de mal humor'], 'ya', 'tan temprano', 'me despierto a las 7', '', 1),
    ('levantarse', '', 'levantar-se', ['temprano', 'a las siete', 'tarde los domingos'], 'temprano', 'tan tarde', 'me levanto temprano', '', 1),
    ('ducharse', '', 'tomar banho (chuveiro)', ['por la mañana', 'con agua fría', 'después del gimnasio'], 'rápido', 'con agua fría', 'me ducho por la mañana', '', 1),
    ('bañarse', '', 'tomar banho; banhar-se', ['en el río', 'en el mar', 'en la piscina'], 'en la piscina', 'en el río', 'nos bañamos en el río', '', 1),
    ('lavarse', '', 'lavar-se', ['las manos', 'la cara con agua fría', 'el pelo cada día'], 'las manos', 'con agua fría', 'me lavo las manos', 'od', 1),
    ('cepillarse', '', 'escovar', ['los dientes', 'el pelo', 'los dientes después de comer'], 'los dientes', None, 'me cepillo los dientes', 'od', 1),
    ('peinarse', '', 'pentear-se', ['rápido', 'delante del espejo', 'con mucho cuidado'], 'un poco', 'así', 'me peino rápido', '', 1),
    ('afeitarse', '', 'barbear-se', ['cada dos días', 'por la mañana', 'con maquinilla'], 'antes de la entrevista', 'la barba', 'me afeito cada dos días', '', 1),
    ('rasurarse', '', 'barbear-se (Am. Lat.)', ['la barba', 'cada mañana', 'antes de salir'], None, None, 'se rasura la barba', 'od', 2),
    ('depilarse', '', 'depilar-se', ['las cejas', 'las piernas', 'en verano'], None, None, 'se depila las cejas', 'od', 2),
    ('maquillarse', '', 'maquiar-se', ['para salir', 'para la boda', 'en el coche'], 'un poco', None, 'se maquilla para salir', '', 1),
    ('pintarse', '', 'pintar-se (unhas, lábios)', ['las uñas', 'los labios', 'las uñas de rojo'], None, None, 'se pinta las uñas', 'od', 2),
    ('secarse', '', 'secar-se', ['el pelo', 'las manos', 'con la toalla'], 'las manos', None, 'me seco el pelo', 'od', 1),
    ('cortarse', '', 'cortar (o cabelo)', ['el pelo', 'las uñas', 'el pelo muy corto'], None, None, 'me corté el pelo', 'od', 1),
    ('vestirse', 'i', 'vestir-se', ['en cinco minutos', 'de negro', 'con ropa cómoda'], 'rápido', 'de negro', 'me visto en cinco minutos', '', 1),
    ('desvestirse', 'i', 'despir-se', ['en el probador', 'antes de dormir', 'rápidamente'], None, None, 'se desvistió', '', 2),
    ('quitarse', '', 'tirar (roupa)', ['el abrigo', 'los zapatos', 'las gafas'], 'el abrigo', 'el jersey', 'quítate el abrigo', 'od', 1),
    ('arreglarse', '', 'arrumar-se', ['para la fiesta', 'para salir', 'en diez minutos'], 'que nos vamos', None, 'me arreglo para la fiesta', '', 1),
    ('abrigarse', '', 'agasalhar-se', ['bien', 'antes de salir', 'con una bufanda'], 'bien, hace frío', None, 'abrígate, hace frío', '', 1),
    ('calzarse', '', 'calçar', ['las botas', 'los zapatos de fiesta', 'las zapatillas'], None, None, 'se calzó las botas', 'od', 2),
    ('mirarse', '', 'olhar-se', ['al espejo', 'en el escaparate', 'en el agua'], None, None, 'me miro al espejo', '', 1),
    ('acostarse', 'ue', 'deitar-se (ir dormir)', ['a medianoche', 'muy tarde', 'temprano entre semana'], 'ya', 'tan tarde', 'me acuesto a medianoche', '', 1),
    ('tumbarse', '', 'deitar-se', ['en la playa', 'en el sofá', 'al sol'], 'un rato', None, 'me tumbé en la playa', '', 2),
    ('echarse una siesta', '', 'tirar um cochilo', ['una siesta', 'una siesta después de comer', 'una siesta en el sofá'], 'una siesta', None, 'me eché una siesta', 'od', 1),
    ('desayunarse', '', 'tomar café da manhã (Am. Lat.)', ['temprano', 'con café y pan', 'en la cocina'], None, None, 'me desayuné temprano', '', 3),
    ('cuidarse', '', 'cuidar-se', ['mucho', 'con la comida', 'del sol'], 'mucho', None, 'cuídate mucho', '', 1),
    ('relajarse', '', 'relaxar', ['leyendo', 'en el spa', 'con música'], 'un poco', None, 'me relajo leyendo', '', 1),
    ('estirarse', '', 'alongar-se', ['antes de correr', 'después del gimnasio', 'al despertar'], 'bien', None, 'me estiro antes de correr', '', 2),
    ('prepararse', '', 'preparar-se', ['para el examen', 'para la entrevista', 'para lo peor'], 'para salir', None, 'me preparo para el examen', '', 1),
]:
    name, cls, pt, tails, aff, neg, ex, fl, tier = a
    p(name, cls, 'rot', K3, pt, tails, 'para' if name == 'prepararse' else '', aff, neg, ex, flags=fl, tier=tier,
      inf='echarse' if name == 'echarse una siesta' else None)
PRON[-1]['prep'] = 'para'

K4 = 'Emoção e mudança de estado'
for a in [
    ('alegrarse', '', 'alegrar-se', ['de verte', 'de la noticia', 'por su hermana'], 'de', None, None, 'me alegro de verte', 'alegrar', 1),
    ('enojarse', '', 'irritar-se, zangar (Am. Lat.)', ['con su hermano', 'por nada', 'con el árbitro'], '', None, 'conmigo', 'se enojó conmigo', 'enojar', 1),
    ('enfadarse', '', 'irritar-se, zangar (Espanha)', ['con facilidad', 'por tonterías', 'con el camarero'], '', None, 'conmigo', 'no te enfades', 'enfadar', 1),
    ('cabrearse', '', 'ficar furioso (coloq.)', ['mucho', 'por una tontería', 'con el camarero'], '', None, 'por eso', 'se cabreó mucho', 'cabrear', 3),
    ('molestarse', '', 'incomodar-se, ofender-se', ['por el comentario', 'por nada', 'con facilidad'], '', None, 'en venir', 'se molestó por el comentario', 'molestar', 2),
    ('ofenderse', '', 'ofender-se', ['por la broma', 'con facilidad', 'por nada'], '', None, 'por eso', 'no te ofendas', 'ofender', 2),
    ('indignarse', '', 'indignar-se', ['con la noticia', 'por la injusticia', 'ante tanta corrupción'], '', None, None, 'me indigné con la noticia', 'indignar', 2),
    ('preocuparse', '', 'preocupar-se', ['por sus hijos', 'por el examen', 'por todo'], 'por', None, 'por eso', 'no te preocupes', 'preocupar', 1),
    ('inquietarse', '', 'inquietar-se', ['al no verte', 'por el silencio', 'sin motivo'], '', None, None, 'se inquietó al no verte', 'inquietar', 3),
    ('agobiarse', '', 'sentir-se sufocado', ['con tanto trabajo', 'en las multitudes', 'por nada'], '', None, 'por eso', 'me agobio con tanto trabajo', 'agobiar', 2),
    ('estresarse', '', 'estressar-se', ['fácilmente', 'antes de los exámenes', 'con el tráfico'], '', None, None, 'me estreso fácilmente', 'estresar', 2),
    ('desesperarse', '', 'desesperar-se', ['con la lentitud', 'en las colas', 'por nada'], '', None, 'todavía', 'no te desesperes', 'desesperar', 2),
    ('asustarse', '', 'assustar-se', ['con el ruido', 'por nada', 'al ver la sombra'], '', None, 'por eso', 'me asusté con el ruido', 'asustar', 1),
    ('espantarse', '', 'espantar-se', ['con el ruido', 'al ver la serpiente', 'con los truenos'], '', None, None, 'el caballo se espantó', 'espantar', 2),
    ('aburrirse', '', 'entediar-se', ['en casa', 'en las reuniones', 'como una ostra'], '', None, None, 'me aburro en casa', 'aburrir', 1),
    ('cansarse', '', 'cansar-se', ['rápido', 'de esperar', 'de sus excusas'], 'de', None, None, 'me canso rápido', 'cansar', 1),
    ('hartarse', '', 'encher-se, cansar de', ['de esperar', 'de sus quejas', 'de comer pizza'], 'de', None, None, 'me harté de esperar', 'hartar', 2),
    ('sorprenderse', '', 'surpreender-se', ['al verlo', 'con el resultado', 'de su respuesta'], '', None, None, 'me sorprendí al verlo', 'sorprender', 1),
    ('asombrarse', '', 'espantar-se, admirar-se', ['del precio', 'de su memoria', 'ante el paisaje'], 'de', None, None, 'se asombró del precio', 'asombrar', 2),
    ('emocionarse', '', 'emocionar-se', ['en la boda', 'con la película', 'al ver el mar'], '', None, None, 'me emocioné en la boda', 'emocionar', 1),
    ('ilusionarse', '', 'criar expectativa', ['con el viaje', 'demasiado pronto', 'con el nuevo trabajo'], '', None, 'tan pronto', 'no te ilusiones', 'ilusionar', 2),
    ('animarse', '', 'animar-se', ['a venir', 'a bailar', 'con la música'], 'a', 'a venir', None, '¡anímate a venir!', 'animar', 1),
    ('entusiasmarse', '', 'entusiasmar-se', ['con el plan', 'con la idea', 'demasiado'], '', None, None, 'se entusiasmó con el plan', 'entusiasmar', 2),
    ('divertirse', 'ie-i', 'divertir-se', ['mucho', 'en la fiesta', 'con los amigos'], '', 'mucho', None, 'nos divertimos mucho', 'divertir', 1),
    ('calmarse', '', 'acalmar-se', ['un poco', 'después de la discusión', 'con la música'], '', '', None, 'cálmate', None, 1),
    ('tranquilizarse', '', 'tranquilizar-se', ['al oír la noticia', 'poco a poco', 'con su voz'], '', '', None, 'tranquilízate', 'tranquilizar', 1),
    ('entristecerse', '', 'entristecer-se', ['con la noticia', 'en otoño', 'en las despedidas'], '', None, None, 'se entristeció con la noticia', 'entristecer', 2),
    ('deprimirse', '', 'deprimir-se', ['en invierno', 'con la lluvia', 'fácilmente'], '', None, None, 'se deprime en invierno', 'deprimir', 2),
    ('avergonzarse', 'üe', 'envergonhar-se', ['de eso', 'de su pasado', 'de sus errores'], 'de', None, 'de nada', 'me avergüenzo de eso', 'avergonzar', 2),
    ('decepcionarse', '', 'decepcionar-se', ['con el final', 'con el resultado', 'con el gobierno'], '', None, None, 'me decepcioné con el final', 'decepcionar', 2),
    ('frustrarse', '', 'frustrar-se', ['con los errores', 'fácilmente', 'con la burocracia'], '', None, None, 'me frustro cuando no entiendo', 'frustrar', 2),
    ('enamorarse', '', 'apaixonar-se', ['de Buenos Aires', 'a primera vista', 'de su voz'], 'de', None, None, 'me enamoré de Buenos Aires', None, 1),
    ('casarse', '', 'casar-se', ['en mayo', 'por la iglesia', 'en la playa'], 'con', None, None, 'se casaron en mayo', None, 1),
    ('divorciarse', '', 'divorciar-se', ['el año pasado', 'después de diez años', 'sin problemas'], '', None, None, 'se divorciaron el año pasado', None, 2),
    ('sentirse', 'ie-i', 'sentir-se', ['bien', 'mejor hoy', 'fatal'], '', None, None, 'me siento bien', None, 1),
    ('enfermarse', '', 'ficar doente (Am. Lat.)', ['la semana pasada', 'en invierno', 'con frecuencia'], '', None, None, 'me enfermé la semana pasada', None, 2),
    ('resfriarse', 'í', 'resfriar-se', ['con el frío', 'en el viaje', 'cada invierno'], '', None, 'otra vez', 'me resfrié con el frío', None, 2),
    ('emborracharse', '', 'embebedar-se', ['en la fiesta', 'con dos cervezas', 'en la boda'], '', None, None, 'se emborrachó en la fiesta', None, 2),
    ('marearse', '', 'ficar tonto, enjoado', ['en barco', 'en el coche', 'con las curvas'], '', None, None, 'me mareo en barco', None, 2),
    ('acostumbrarse', '', 'acostumar-se', ['al frío', 'a madrugar', 'a la ciudad'], 'a', None, None, 'me acostumbré al frío', None, 1),
    ('equivocarse', '', 'enganar-se, errar', ['de número', 'en el examen', 'de calle'], '', None, 'de calle', 'me equivoqué de número', None, 1),
    ('confundirse', '', 'confundir-se', ['de calle', 'de fecha', 'con los nombres'], '', None, None, 'me confundí de calle', None, 2),
    ('interesarse', '', 'interessar-se', ['por la historia', 'por el arte', 'por el proyecto'], 'por', None, None, 'se interesa por la historia', 'interesar', 2),
    ('convencerse', '', 'convencer-se', ['de que era verdad', 'de su inocencia', 'poco a poco'], 'de', None, None, 'me convencí de que era verdad', None, 2),
]:
    name, cls, pt, tails, prep, aff, neg, ex, dual, tier = a
    p(name, cls, 'emo', K4, pt, tails, prep, aff, neg, ex, tier=tier)
    PRON[-1]['dual'] = dual  # par tipo gustar (me aburre / me aburro)

K5 = 'Movimento, posição e lugar'
for a in [
    ('sentarse', 'ie', 'sentar-se', ['aquí', 'junto a la ventana', 'en el sofá'], 'aquí', 'en esa silla', 'siéntate aquí', 1, True),
    ('pararse', '', 'parar; ficar de pé (Am. Lat.)', ['en la esquina', 'a descansar', 'de golpe'], None, None, 'se paró el reloj', 2, False),
    ('detenerse', '', 'deter-se, parar', ['en la esquina', 'a mirar el escaparate', 'un momento'], 'aquí', None, 'me detuve en la esquina', 2, True),
    ('acercarse', '', 'aproximar-se', ['a la ventana', 'al fuego', 'a saludar'], '', 'tanto', 'acércate', 1, True),
    ('alejarse', '', 'afastar-se', ['de la orilla', 'del grupo', 'poco a poco'], None, 'de la orilla', 'no te alejes', 1, True),
    ('apartarse', '', 'afastar-se, sair da frente', ['del camino', 'de la puerta', 'a un lado'], 'por favor', None, 'apártate, por favor', 2, True),
    ('moverse', 'ue', 'mover-se', ['mucho en la cama', 'de su sitio', 'con rapidez'], None, '', 'no te muevas', 1, True),
    ('instalarse', '', 'instalar-se', ['en el centro', 'en un piso nuevo', 'en la habitación de invitados'], None, None, 'nos instalamos en el centro', 2, True),
    ('asomarse', '', 'debruçar-se, aparecer', ['a la ventana', 'al balcón', 'por la puerta'], None, 'a la ventana', 'se asomó a la ventana', 2, False),
    ('esconderse', '', 'esconder-se', ['detrás de la puerta', 'debajo de la cama', 'en el armario'], 'aquí', None, 'el gato se escondió', 1, True),
    ('subirse', '', 'subir em', ['al autobús', 'al árbol', 'a la silla'], 'al coche', 'a la mesa', 'me subí al autobús', 1, False),
    ('bajarse', '', 'descer de', ['en la próxima parada', 'del tren', 'del coche'], 'aquí', None, 'me bajo en la próxima', 1, False),
    ('montarse', '', 'montar, entrar (veículo)', ['en el coche', 'en la moto', 'en el tren'], None, None, 'se montó en el coche', 2, False),
    ('lanzarse', '', 'lançar-se', ['en paracaídas', 'al agua', 'a la aventura'], None, None, 'se lanzó en paracaídas', 2, False),
    ('tropezarse', 'ie', 'tropeçar', ['con una piedra', 'en la escalera', 'con la alfombra'], None, None, 'me tropecé con una piedra', 2, False),
    ('resbalarse', '', 'escorregar', ['en el baño', 'en el hielo', 'con la lluvia'], None, None, 'me resbalé en el baño', 2, False),
    ('girarse', '', 'virar-se', ['hacia la puerta', 'de repente', 'al oír su nombre'], None, None, 'se giró hacia la puerta', 2, False),
    ('darse la vuelta', '', 'virar-se', ['la vuelta de repente', 'la vuelta al oír su nombre', 'la vuelta en la cama'], 'la vuelta', None, 'se dio la vuelta', 2, False),
    ('inclinarse', '', 'inclinar-se', ['hacia adelante', 'para saludar', 'sobre la mesa'], None, None, 'se inclinó hacia adelante', 2, False),
    ('apoyarse', '', 'apoiar-se', ['en la pared', 'en el bastón', 'en la barandilla'], 'en mí', None, 'me apoyé en la pared', 2, True),
    ('colgarse', 'ue', 'pendurar-se', ['de la rama', 'del cuello de su padre', 'de la barra'], None, None, 'se colgó de la rama', 3, False),
    ('escaparse', '', 'escapar', ['de casa', 'por la ventana', 'del zoo'], None, None, 'se escapó el perro', 2, False),
    ('dirigirse', '', 'dirigir-se', ['a la salida', 'al público', 'hacia el norte'], None, None, 'me dirijo a la salida', 2, True),
    ('trasladarse', '', 'mudar-se, deslocar-se', ['a Lima', 'a otra oficina', 'en tren'], None, None, 'se trasladó a Lima', 2, False),
    ('adelantarse', '', 'adiantar-se', ['a todos', 'un poco', 'a los acontecimientos'], None, None, 'se adelantó a todos', 2, False),
    ('atrasarse', '', 'atrasar-se', ['por el tráfico', 'con los pagos', 'en los estudios'], None, None, 'me atrasé por el tráfico', 2, False),
    ('retrasarse', '', 'atrasar-se', ['por la lluvia', 'media hora', 'con el proyecto'], None, None, 'el vuelo se retrasó', 2, False),
]:
    name, cls, pt, tails, aff, neg, ex, tier, drop = a
    p(name, cls, 'mov', K5, pt, tails, '', aff, neg, ex, flags='' if drop else 'nodrop', tier=tier,
      inf='darse' if name == 'darse la vuelta' else None)

K6 = 'Recíprocos'
for a in [
    ('abrazarse', '', 'abraçar-se', ['con cariño', 'en el aeropuerto', 'al final del partido'], 'nos abrazamos'),
    ('besarse', '', 'beijar-se', ['en el parque', 'bajo la lluvia', 'en la puerta'], 'se besaron'),
    ('conocerse', '', 'conhecer-se', ['en Lima', 'en la universidad', 'hace años'], 'nos conocimos en Lima'),
    ('verse', '', 'ver-se, encontrar-se', ['mañana', 'los domingos', 'en el bar'], 'nos vemos mañana'),
    ('encontrarse', 'ue', 'encontrar-se', ['en el bar', 'en la plaza', 'por casualidad'], 'nos encontramos en el bar'),
    ('escribirse', '', 'escrever um ao outro', ['cada día', 'por correo', 'cartas'], 'nos escribimos cada día'),
    ('llamarse', '', 'ligar um pro outro', ['luego', 'cada noche', 'por teléfono'], 'nos llamamos luego'),
    ('hablarse', '', 'falar-se', ['todos los días', 'por teléfono', 'muy poco'], 'ya no se hablan'),
    ('saludarse', '', 'cumprimentar-se', ['con la mano', 'con dos besos', 'cada mañana'], 'se saludaron con la mano'),
    ('ayudarse', '', 'ajudar-se', ['mucho', 'con los deberes', 'en todo'], 'nos ayudamos mucho'),
    ('entenderse', 'ie', 'entender-se', ['bien', 'sin palabras', 'en inglés'], 'nos entendemos bien'),
    ('quererse', 'ie', 'amar-se', ['mucho', 'como hermanos', 'desde niños'], 'se quieren mucho'),
    ('odiarse', '', 'odiar-se', ['desde niños', 'a muerte', 'sin motivo'], 'se odian desde niños'),
    ('pelearse', '', 'brigar', ['por dinero', 'por tonterías', 'cada semana'], 'se pelearon por dinero'),
    ('reconciliarse', '', 'reconciliar-se', ['después de la pelea', 'al final', 'en Navidad'], 'se reconciliaron'),
    ('separarse', '', 'separar-se', ['en 2020', 'después de diez años', 'sin problemas'], 'se separaron en 2020'),
    ('despedirse', 'i', 'despedir-se', ['en la estación', 'con un abrazo', 'en la puerta'], 'nos despedimos en la estación'),
    ('mirarse', '', 'olhar-se', ['en silencio', 'a los ojos', 'sin decir nada'], 'se miraron en silencio'),
]:
    name, cls, pt, tails, ex = a
    p(name + ' (recíproco)', cls, 'rec', K6, pt, tails, '', None, None, ex, flags='pl', inf=name)

K7 = 'Ênfase'
EMPH = {}
for a in [
    ('comerse', '', 'comer (tudo)', ['toda la pizza', 'el pastel entero', 'tres platos de pasta'], ['pizza', 'pastel', 'pasta'], 'se comió todo el pastel'),
    ('beberse', '', 'beber (tudo)', ['la botella entera', 'dos litros de agua', 'la cerveza de un trago'], ['agua', 'cerveza', 'vino'], 'me bebí la botella'),
    ('tomarse', '', 'tomar (tudo)', ['un café', 'la sopa entera', 'el jarabe de un trago'], [], 'me tomé un café'),
    ('leerse', '', 'ler (inteiro)', ['el libro en un día', 'toda la saga', 'el periódico entero'], ['libros', 'novelas', 'periódicos'], 'me leí el libro en un día'),
    ('aprenderse', '', 'decorar', ['la canción', 'todos los verbos', 'el poema de memoria'], ['canciones', 'verbos', 'poemas'], 'me aprendí la canción'),
    ('saberse', '', 'saber de cor', ['la letra', 'el temario entero', 'los nombres de todos'], [], 'me sé la letra'),
    ('fumarse', '', 'fumar (inteiro)', ['un paquete entero', 'un puro', 'tres cigarrillos'], ['tabaco', 'puros'], 'se fumó un paquete'),
    ('gastarse', '', 'gastar (tudo)', ['todo el sueldo', 'cien euros en ropa', 'la herencia'], ['dinero'], 'me gasté todo el sueldo'),
    ('ganarse', '', 'ganhar, merecer', ['el premio', 'un buen sueldo', 'el respeto de todos'], [], 'te ganaste el premio'),
    ('verse', '', 'assistir (inteiro)', ['la serie entera', 'tres películas seguidas', 'el partido completo'], ['series', 'películas'], 'me vi la serie entera'),
    ('tragarse', '', 'engolir (também acreditar)', ['la mentira', 'el chicle', 'todo el discurso'], [], 'se tragó la mentira'),
    ('conocerse', '', 'conhecer bem', ['la ciudad', 'todos los atajos', 'el barrio de memoria'], [], 'me conozco la ciudad'),
    ('esperarse', '', 'esperar (um pouco)', ['un momento', 'un poco', 'cinco minutos'], [], 'espérate un momento'),
    ('subirse / bajarse', '', 'subir / descer', ['al coche', 'del autobús', 'a la moto'], [], 'súbete al coche'),
]:
    name, cls, pt, Q, B, ex = a
    p(name + ' (ênfase)', cls, 'enf', K7, pt, Q, '', None, None, ex, inf=('subirse' if name.startswith('subirse') else name))
    PRON[-1]['bare'] = B

ALL = GUSTAR + PRON
ids = [e['id'] for e in ALL]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
