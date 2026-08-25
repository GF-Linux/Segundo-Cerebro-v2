---
tipo: meta
projeto: meta
data: 2026-08-25
status: vigente
tags: [pendencias, migracao]
---

<!-- Escrito a pedido do Jared: ler com calma e decidir. Apagar quando as decisões
     estiverem tomadas. O cabeçalho `#?` da primeira versão era a convenção do §4.1,
     que é de ARQUIVO DE CÓDIGO — este repositório exige frontmatter, e a P1 me pegou. -->

# O que esperar de você, e onde ler

## Leia nesta ordem

| # | arquivo | linhas | o que é |
|---|---|:-:|---|
| 1 | `docs/fluxo.md` | 464 | **a planta** — a árvore, o critério de nome, as 4 emendas marcadas `[EMENDA]` |
| 2 | `docs/portao.md` | 251 | **as 7 pernas**, o que cada uma trava e **o que fica descoberto** |
| 3 | `docs/diario.md` | 200 | **o que falhou** — inclusive os cinco números que o executor inventou e desmentiu sozinho |

## O estado, conferido por mim em 25/08

Fonte **intocada** (`05c9b67`, 0 alterações). Novo: ramo `principal`, 8 commits, **sem remoto**,
árvore limpa, **portão 7/7 verde** (rodei). 358 MB → 3,1 MB. Orientar num projeto: 58.594 → 1.347
tokens. **Sequenciamento: 0 no índice, 0 no disco, 0 no histórico.** Conteúdo substantivo
comparado linha a linha: **16.057 linhas, 0 perdidas**.

## As decisões que esperam você

### Ratificação — 4 emendas à planta + 1 mudança de desenho
Cada uma forçada por medição, marcada `[EMENDA]` em `docs/fluxo.md`:
`tarefas.md` (backlog não cabia no teto de 25 do `agora.md`) · `sobre.md` (o texto longo do antigo
`_overview`, que o teto truncava) · `ferramentas/ips-permitidos.txt` (uma lista de exceção, não
duas) · `ferramentas/ligacoes-herdadas.txt` (os 12 links já quebrados **na fonte**).
E a mudança: **o caminho de leitura barata perdeu a sessão** — o `agora.md` passou a **carregar** o
estado em vez de apontar para ela. A correção não foi afrouxar o teto.

### D5 — o nome de `formacao-python`
Proposta: **`formacao`**. Medido: Python está em **32/32** notas, então a palavra no rótulo não
acrescenta; e o rótulo atual não cobre as **10 notas de carreira** nem as **4 de C#**.
*Alternativa que ele não descarta:* partir em `formacao` + `carreira` — mais fiel, mais trabalho.
Os **83 `.py` não ficam** (código não mora na base de conhecimento). Ele recomenda **repo próprio**;
até lá o ponteiro diz `(nao localizado)`, que é honesto.

### D0 e D8 — atos seus, ninguém tocou
**D0:** o v2 assume o nome `segundo-cerebro` e o atual vira `segundo-cerebro-legado`.
**D8:** o atual sai do GitHub depois disso. ⚠️ Apagar/arquivar repositório é ato seu, não do agente.

### Os 12 wikilinks herdados
`meta/ligacoes-herdadas.md` traz cada um com a causa e três opções. Ele **recomenda (b) para dois**:
`0009-memoria-auditavel-da-fern` e `0020-tres-direcoes-de-telao` são decisões que a prosa
**promete** e que nunca existiram — escrevê-las recupera conhecimento perdido. Ele não as escreveu:
seria inventar o alvo.

## ⚠️ Dois avisos que não são decisão, e sim risco

**O leitor derivado.** `meta/lei.md` e várias notas citam `~/Desktop/segundo-cerebro-graph` (o
comando `sc`). Está **fora da cerca do agente e da minha**. Se existir, lê a forma antiga e esta
migração o quebra. **Não concluir que não existe só porque nenhum de nós o achou.**

**A lei velha mandava recriar os defeitos.** A varredura do §12·6 achou que `meta/lei.md` — o
primeiro arquivo que toda sessão lê — instruía a atualizar o `status.md` e *"adicionar uma linha em
`INDEX.md` para cada nota nova"*: exatamente o status sem teto que chegou a 804 linhas e o índice à
mão que perdia 50 de 341 notas. Foi reescrita, e o texto original está íntegro na decisão
`meta/0010`. **Vale ler essa decisão antes de aprovar o resto** — é o achado que mais explica por
que a reforma existe.

## O que está rodando em paralelo (não depende de você agora)
A primeira categoria do mapa de harness — `foundations`, 31 documentos — em
`~/projetos/harness-fundamentos`. A régua é o **Terminus**, e o caso de teste é a **A16**: o portão
dele fica verde com um canal vivo destruído.
