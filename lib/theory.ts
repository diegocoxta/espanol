/** Fichas de teoria por nível (HTML estático, conteúdo próprio). */
export const THEORY: Record<number, string> = {
0:`<p>Escolha um nível acima para ver a ficha de teoria correspondente. No modo <b>Tudo</b>, as questões dos seis níveis aparecem juntas — use <b>Aleatório</b> para uma revisão geral.</p>
<div class="tbl"><table><tr><th></th><th>Objeto direto (OD)</th><th>Objeto indireto (OI)</th></tr>
<tr><td>yo</td><td>me</td><td>me</td></tr><tr><td>tú</td><td>te</td><td>te</td></tr>
<tr><td>él / ella / usted</td><td>lo / la</td><td>le (→ se antes de lo/la)</td></tr>
<tr><td>nosotros</td><td>nos</td><td>nos</td></tr><tr><td>vosotros</td><td>os</td><td>os</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>los / las</td><td>les (→ se)</td></tr></table></div>`,
1:`<h3>O que é o objeto direto</h3><p>É o que recebe a ação diretamente e responde a <i>o quê?</i>: <span class="es">María compra <b>el pan</b></span> → compra o quê? → el pan.</p>
<div class="tbl"><table><tr><th></th><th>Singular</th><th>Plural</th></tr><tr><td>Masculino</td><td><span class="es">lo</span> — el pan → lo</td><td><span class="es">los</span> — los libros → los</td></tr><tr><td>Feminino</td><td><span class="es">la</span> — la carta → la</td><td><span class="es">las</span> — las flores → las</td></tr></table></div>
<h3>Posição</h3><ul><li>Com verbo conjugado, o pronome vem <b>antes</b>: <span class="es">María lo compra.</span></li><li>Na negativa: <i>no</i> + pronome + verbo: <span class="es">No lo compro.</span></li></ul>
<h3>Cuidado com o gênero</h3><ul><li><span class="es">el agua, el aula, el hacha, el águila</span> são <b>femininos</b> (o <i>el</i> só aparece por causa do <i>a</i> tônico) → <b>la</b>.</li><li><span class="es">el problema, el tema, el sistema, el idioma, el mapa, el día</span> são masculinos → <b>lo</b>.</li><li><span class="es">la mano, la foto, la moto, la radio</span> são femininos → <b>la</b>.</li></ul>`,
2:`<h3>OD de pessoa e o “a” pessoal</h3><p>Pessoas determinadas como OD levam <i>a</i>, mas continuam sendo OD: <span class="es">Invito a María → La invito.</span> Homem e mulher juntos → masculino plural: <span class="es">a Pedro y a Ana → los</span>.</p>
<ul><li>Leva <i>a</i>: pessoas conhecidas, <i>alguien, nadie</i>, animais de estimação. <i>a + el = al</i>.</li><li>Sem <i>a</i>: coisas, lugares, pessoas indeterminadas (<span class="es">Busco un camarero que hable inglés</span>), com <i>tener</i> e <i>hay</i>.</li></ul>
<h3>Me, te, nos, os</h3><p>Têm a mesma forma como OD e OI. Atenção à mudança de pessoa no diálogo: <span class="es">—¿Me llamas? —Sí, te llamo.</span></p>
<h3>Objeto indireto</h3><p>Responde a <i>a quem? / para quem?</i>. Na 3ª pessoa: <b>le</b> (singular) e <b>les</b> (plural), sem distinção de gênero. É normal duplicar: <span class="es">Le doy el libro a Juan.</span></p>
<h3>Verbos como gustar</h3><p>A coisa que agrada é o <b>sujeito</b>; a pessoa é OI: <span class="es">A Juan le gustan los perros</span> (concorda com <i>los perros</i>).</p>`,
3:`<h3>Dois pronomes juntos</h3><p>Ordem fixa: <b>OI + OD</b>. <span class="es">Me lo das · Te la compro · Nos los envían · Os las traigo.</span></p>
<h3>A regra do “se”</h3><p><i>le</i> ou <i>les</i> diante de <i>lo, la, los, las</i> vira <b>se</b>. Nunca existe <span class="es">*le lo</span> nem <span class="es">*les las</span>.</p>
<div class="tbl"><table><tr><th>Frase</th><th>Pronomes</th></tr><tr><td class="es">Le doy el libro a Juan.</td><td class="es">Se lo doy.</td></tr><tr><td class="es">Les mando las fotos a mis padres.</td><td class="es">Se las mando.</td></tr><tr><td class="es">Juan me devuelve la llave.</td><td class="es">Juan me la devuelve.</td></tr></table></div>
<p>Como <i>se</i> não indica gênero nem número, pode-se desfazer a ambiguidade: <span class="es">Se lo di <b>a ella</b>.</span></p>`,
4:`<h3>Onde colocar o pronome</h3><div class="tbl"><table><tr><th>Forma verbal</th><th>Posição</th><th>Exemplo</th></tr>
<tr><td>Verbo conjugado</td><td>antes</td><td class="es">Lo compro.</td></tr>
<tr><td>Perífrase com infinitivo</td><td>antes do conjugado <b>ou</b> colado ao infinitivo</td><td class="es">Lo voy a comprar / Voy a comprarlo.</td></tr>
<tr><td>Estar + gerúndio</td><td>antes <b>ou</b> colado ao gerúndio</td><td class="es">Lo estoy leyendo / Estoy leyéndolo.</td></tr>
<tr><td>Imperativo afirmativo</td><td>depois, colado</td><td class="es">Cómpralo. Dáselo.</td></tr>
<tr><td>Imperativo negativo</td><td>antes</td><td class="es">No lo compres. No se lo des.</td></tr></table></div>
<h3>Acentuação</h3><ul><li>Gerúndio + pronome: sempre acento — <span class="es">comprándolo, diciéndoselo</span>.</li><li>Infinitivo + 1 pronome: sem acento — <span class="es">comprarlo</span>; + 2: com acento — <span class="es">comprárselo</span>.</li><li>Imperativo de várias sílabas + pronome: acento — <span class="es">cómpralo, explícamelo</span>. Monossílabo + 1: sem acento — <span class="es">dalo, dime, hazlo</span>; + 2: com acento — <span class="es">dámelo, dísela</span>.</li></ul>
<h3>Duplicação obrigatória</h3><p>Se o OD definido ou o OI vão para o início da frase, o pronome é obrigatório: <span class="es">El coche lo vendí ayer. A mis padres les escribí.</span></p>`,
5:`<h3>Gustar e afins</h3><p><i>gustar, encantar, interesar, molestar, preocupar, doler, faltar, quedar, apetecer, importar</i>: pessoa = OI (pronome obrigatório), coisa = sujeito (o verbo concorda com ela).</p>
<h3>“Se” de ação involuntária</h3><p><span class="es">Se me cayó el vaso · Se nos olvidaron las llaves.</span> Ordem fixa: <b>se</b> + pronome. <span class="es">*Me se</span> é vulgarismo.</p>
<h3>Reflexivo + OD e dativo possessivo</h3><p><span class="es">Me pongo el abrigo → Me lo pongo · Póntelo.</span> Com partes do corpo e pertences, usa-se artigo e o dono vai como OI: <span class="es">Le lavé la cara al niño.</span></p>
<h3>Lo neutro</h3><p>Retoma uma ideia ou oração inteira: <span class="es">—¿Sabes que se casa? —Sí, lo sé.</span></p>
<h3>Leísmo, laísmo, loísmo</h3><div class="tbl"><table><tr><th>Uso</th><th>Exemplo</th><th>Norma (RAE)</th></tr>
<tr><td>le = OD de homem (singular)</td><td class="es">A Juan le vi.</td><td>admitido; recomenda-se <i>lo</i></td></tr>
<tr><td>les = OD de homens (plural)</td><td class="es">A mis primos les vi.</td><td>desaconselhado</td></tr>
<tr><td>le = OD de mulher</td><td class="es">A María le vi.</td><td>incorreto (exceto com <i>usted</i> por cortesia)</td></tr>
<tr><td>le = OD de coisa ou animal</td><td class="es">El libro le dejé.</td><td>incorreto</td></tr>
<tr><td>la/lo como OI (laísmo/loísmo)</td><td class="es">La dije la verdad.</td><td>incorreto → <i>le</i></td></tr></table></div>
<h3>Regência que engana</h3><p>OD de pessoa: <i>llamar, ayudar, esperar, escuchar, invitar</i>. OI de pessoa: <i>pagar, robar, preguntar, pedir, decir</i> (algo <b>a</b> alguém).</p>`,
6:`<h3>Lo atributo</h3><p>Com <i>ser, estar, parecer</i>, o pronome é sempre <b>lo</b>, invariável: <span class="es">—¿Están cansadas? —Sí, lo están.</span></p>
<h3>Subida de clíticos</h3><ul><li>Os pronomes formam um bloco: sobem juntos ou ficam juntos — <span class="es">Se lo quiero decir / Quiero decírselo</span>, nunca <span class="es">*Se quiero decirlo</span>.</li><li>Sobem com auxiliares e perífrases (ir a, poder, querer, tener que, acabar de, volver a…). Preposições como <i>en</i> bloqueiam: <span class="es">Insisto en hacerlo</span>.</li><li>Tempos compostos: antes de <i>haber</i> — <span class="es">Lo he visto</span>.</li></ul>
<h3>Imperativos especiais</h3><ul><li><i>Nosotros</i>: cai o -s diante de <i>se</i> e <i>nos</i> — <span class="es">digámoselo, sentémonos, vámonos</span>.</li><li><i>Vosotros</i>: cai o -d diante de <i>os</i> — <span class="es">sentaos</span>; mantém-se nos demais — <span class="es">dadlo, dádselo</span>.</li><li><i>Usted</i>: <span class="es">dígaselo, déselo</span>; com um só pronome, <i>dé</i> perde o acento — <span class="es">delo, deme</span>.</li></ul>
<h3>Ordem dos clíticos</h3><p><b>se</b> › <b>te / os</b> › <b>me / nos</b> › <b>le / lo / la…</b> — <span class="es">Se te cayó · No te me pongas así.</span></p>
<h3>Dativos sem argumento</h3><p>Ético (<span class="es">Mi hijo no me come</span>), aspectual (<span class="es">Se comió toda la pizza</span>), possessivo (<span class="es">Le robaron el coche</span>).</p>
<h3>Causativos e percepção</h3><p>Sem OD próprio do infinitivo, o causado é OD: <span class="es">Los hice reír</span>. Com OD próprio, vira OI: <span class="es">Les hice leer el libro → Se lo hice leer.</span></p>`
};
