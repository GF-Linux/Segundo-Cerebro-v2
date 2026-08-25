#!/usr/bin/env bash
#* PERNA P3 do portao: GERA o INDEX.md a partir do frontmatter. Uma linha por PROJETO.
#! POR QUE GERADO E NAO ESCRITO: o cerebro anterior mandava "adicionar uma linha em INDEX.md
#!   para cada nota nova". O passo era manual, o INDEX chegou a 402 linhas e mesmo assim
#!   perdeu 50 das 341 notas. Indice a mao sempre desvia — nao por desleixo, mas porque o
#!   passo mora fora da acao que ele registra. Gerado, o desvio e impossivel.
#! POR QUE UMA LINHA POR PROJETO E NAO POR NOTA: o INDEX e lido em TODA sessao (P6). Um
#!   indice que cresce com o corpus e uma conta que so sobe. Por projeto, ele cresce com o
#!   numero de projetos — que muda em meses, nao em horas.
set -uo pipefail
cd "$(dirname "$0")/.."

campo() { awk -v c="$2" 'NR>1{if($0=="---")exit; if($0 ~ "^"c":"){sub("^"c":[[:space:]]*","");print;exit}}' "$1"; }

gerar() {
  cat <<'CAB'
#* Indice GERADO por `ferramentas/indice.sh`. Nao editar a mao — o portao (P3) reprova o desvio.

# INDEX — um projeto por linha

| projeto | o que e | onde o codigo vive | notas |
|---|---|---|---|
CAB
  for d in projetos/*/; do
    [ -f "$d/projeto.md" ] || continue
    slug=$(basename "$d")
    printf '| [[projetos/%s/projeto]] | %s | `%s` | %s dec · %s ses |\n' \
      "$slug" "$(campo "$d/projeto.md" resumo)" "$(campo "$d/projeto.md" codigo)" \
      "$(ls "$d"decisoes/*.md 2>/dev/null | wc -l)" "$(ls "$d"sessoes/*.md 2>/dev/null | wc -l)"
  done
  printf '\n**meta** — o cerebro falando de si mesmo: [[meta/projeto]] · [[meta/lei]] · [[meta/agora]]\n'
  printf '**transversal** — o que cruza projeto: %s notas em `transversal/`\n' "$(ls transversal/*.md 2>/dev/null | wc -l)"
}

if [ "${1:-}" = "--stdout" ]; then gerar; else gerar > INDEX.md; echo "INDEX.md gerado"; fi
