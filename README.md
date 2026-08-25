# Segundo Cerebro — Gustavo Goncalves Freitas (LHV/UFRRJ)

Memoria, decisoes e progresso dos projetos. **Markdown puro, e so isso.** Legivel por
humano no terminal, por maquina pelo frontmatter, e no Obsidian pelos wikilinks.

## Como se le, em tres passos


1. INDEX.md                        uma linha por projeto     (~20 linhas, GERADO)
2. projetos/<slug>/projeto.md      identidade                (teto 30 linhas)
   projetos/<slug>/agora.md        onde parei                (teto 25 linhas)
3. projetos/<slug>/sessoes/…       a sessao mais recente



Para saber o que ainda vale num projeto: `ferramentas/vigentes.sh <slug>`.

## O que NUNCA entra aqui

| classe | por que |

1. **sequencia** (`.ab1`, `.fasta`, `.fa`, …) | nem uma. Sao dados reais de terceiros, nao publicados |
2. **binario** (zip, pdf, docx, xlsx, imagem) | este repo e texto. O binario mora no disco, com o caminho anotado na nota |
3. **codigo de outro projeto** | o cerebro DOCUMENTA projeto; nao HOSPEDA projeto |
4. **documento pessoal** | a nota cujo dano, se vazasse, cai sobre uma PESSOA e nao sobre um projeto |
5. **credencial, IP roteavel, numero de documento** | redigidos no lugar: a nota entra, o valor vira marcador |
6. **Pastas e projetos | repositorio puramente pessoal com objetivo de manter o contexto das sessoes



## A forma de uma nota

Toda nota carrega o mesmo frontmatter — `tipo`, `projeto`, `data`, `status`, `tags`.
`decisao` se revoga; `sessao` nasce `historico`, porque fato datado nao se revoga.

**Decisao revogada nao se apaga.** Ela e o unico lugar onde o *porque nao* esta escrito,
e um log append-only sem os revogados vira lista de ordens sem motivo.

## O portao

```
ferramentas/portao.sh
```

Sete pernas, e sai 0 so com as sete verdes. O que elas medem e por que existem esta em
[`docs/portao.md`](docs/portao.md); a planta do repositorio, em [`docs/fluxo.md`](docs/fluxo.md).

## Estrutura

```
INDEX.md                       gerado por ferramentas/indice.sh — nao editar a mao
meta/                          o cerebro falando de si mesmo (lei, decisoes, sessoes)
projetos/<slug>/
  projeto.md                   identidade: produto atual, aliases, onde o codigo vive
  sobre.md                     o texto longo, quando existe
  agora.md                     onde parei e o proximo passo
  tarefas.md                   o backlog, fora do caminho de leitura barata
  decisoes/NNNN-verbo-objeto.md   append-only
  sessoes/AAAA-MM-DD.md        append-only, uma por dia por projeto
  referencias.md               fonte externa citavel
transversal/                   o que cruza mais de um projeto
moldes/                        um molde por tipo de nota
ferramentas/                   o CLI deste repo — o unico codigo que mora aqui
docs/                          a planta, o portao e o diario do agente
```
