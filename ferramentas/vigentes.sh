#!/usr/bin/env bash
#* Lista as decisoes de um projeto separadas por status, lendo o frontmatter.
#! POR QUE ISTO E UMA FERRAMENTA E NAO UM HABITO: no cerebro anterior, abrir
#!   `dna-contingency/decisoes/` mostrava 70 nomes iguais. Quinze ja nao valiam, e a unica
#!   coisa que dizia isso era o frontmatter, dentro de cada arquivo. Descobrir custava 70
#!   aberturas. Aqui custa um comando.
set -uo pipefail
cd "$(dirname "$0")/.."
p="${1:-}"
[ -z "$p" ] && { echo "uso: ferramentas/vigentes.sh <slug-do-projeto>"; exit 2; }
d="projetos/$p/decisoes"
[ -d "$d" ] || { echo "sem pasta de decisoes: $d"; exit 2; }

echo "== VIGENTES =="
for f in "$d"/*.md; do
  [ -e "$f" ] || continue
  st=$(awk 'NR>1{if($0=="---")exit; if(/^status:/){sub(/^status:[[:space:]]*/,"");print;exit}}' "$f")
  [ "$st" = "vigente" ] && printf "  %s\n" "$(basename "$f")"
done
echo "== JA NAO VALEM (ficam: explicam o porque nao) =="
for f in "$d"/*.md; do
  [ -e "$f" ] || continue
  st=$(awk 'NR>1{if($0=="---")exit; if(/^status:/){sub(/^status:[[:space:]]*/,"");print;exit}}' "$f")
  [ "$st" != "vigente" ] && printf "  %-62s %s\n" "$(basename "$f")" "$st"
done
