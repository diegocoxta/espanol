# Cuaderno de pronombres

Web app em **Next.js 15 + React 19 + TypeScript** com três cadernos de espanhol. Cada um tem seis níveis, do básico ao extremo, além de teoria por nível, correção na hora e progresso salvo no **localStorage** (uma chave por caderno). Não há servidor nem banco de dados.

| Rota | Caderno | Questões | Chave no localStorage |
|---|---|---|---|
| `/` | Objeto direto e indireto | 1.005 | `pronombres-objeto-v1` |
| `/pronominales/` | Verbos com pronome (tipo gustar, pronominais, reflexivos, recíprocos, ênfase) | 2.040 | `verbos-pronominales-v1` |
| `/usos-del-se/` | Os 9 usos do *se* + se/sé/si/sí | 1.022 | `usos-del-se-v1` |

## Rodar e publicar

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # site estático em ./out (Vercel, Netlify, GitHub Pages…)
npm start          # serve ./out localmente
```

## Cobertura dos verbos

O caderno **Verbos com pronome** é gerado a partir de um catálogo (`scripts/pronominales/catalog.py`) com **todos os 362 verbos e expressões** dos três materiais de referência:

- 162 do tipo gustar, nas 7 categorias;
- 200 pronominais: só pronominais, os que mudam de sentido (com o par sem pronome), rotina, emoção, movimento, recíprocos e ênfase.

A seleção garante que **cada item tenha pelo menos 3 questões**, incluindo uma de vocabulário e uma de gramática. A exceção é *suicidarse*, que aparece só em 2 questões e apenas em contexto narrativo.

O glossário da página mostra cada item com sentido, exemplo, par sem pronome e contagem de questões. O botão **Praticar** filtra as questões daquele verbo.

No caderno **Usos do se**, o glossário traz os 9 usos, o item se/sé/si/sí e os verbos citados no material (mudança espontânea e acidental). Cada um tem no mínimo 6 questões.

## Gerar as questões de novo

```bash
npm run test:conj   # testes do conjugador (106 formas e acentos de clíticos)
npm run generate    # regera data/*.json dos três cadernos
```

- `scripts/generate_objeto.py`: caderno 1.
- `scripts/pronominales/conj.py`: conjugador (presente, pretérito, subjuntivo, imperativos, gerúndio). Também une os clíticos com a acentuação correta (*levántate, póntelo, vámonos, vestíos, delo/déselo*).
- `scripts/pronominales/catalog.py`: catálogo de verbos (edite aqui para incluir verbos).
- `scripts/pronominales/gen_pronominales.py` e `gen_se.py`: geradores dos cadernos 2 e 3. Imprimem a cobertura e avisam se algum item ficou com menos de 3 questões.
- `scripts/pronominales/qlib.py`: formato das questões e seleção com cobertura mínima.

## Estrutura

```
app/                    page.tsx (caderno 1), pronominales/, usos-del-se/, layout, globals.css
components/
  ModulePage.tsx        página de um caderno (abas com next/link)
  ModuleNav.tsx         abas entre cadernos
  StudyApp.tsx          níveis, modos, filtros (tipo e verbo), estatísticas
  Glossary.tsx          lista de verbos/usos com busca e “Praticar”
  QuestionCard.tsx, QuestionMap.tsx, ResetButton.tsx, questions/*
lib/
  modules.ts            metadados dos cadernos (níveis, títulos, chaves)
  theory*.ts            fichas de teoria por nível
  useProgress.ts        localStorage por caderno (sincroniza entre abas)
data/                   questões e glossários gerados
```

## Formato das questões (`lib/types.ts`)

| campo | uso |
|---|---|
| `t` | `mc` múltipla escolha · `in` digitar · `err` achar o erro · `ord` ordenar |
| `lv`, `k` | nível (1–6) e tipo de exercício |
| `q`, `s` | enunciado e frase (`[[x]]` = destaque, `___` = lacuna) |
| `o`, `a` | opções e índice certo (`mc`); respostas aceitas (`in`, `ord`); índices das palavras erradas (`err`) |
| `w`, `fix` | palavras da frase (`err`, `ord`) e frase corrigida (`err`) |
| `x` | explicação em HTML simples |
| `v` | ids do glossário que a questão pratica (cadernos 2 e 3) |

Os IDs das questões são sequenciais. Se você regerar um caderno, o progresso salvo dele pode apontar para outras questões. Nesse caso, troque a chave em `lib/modules.ts` (por exemplo, `-v2`).
