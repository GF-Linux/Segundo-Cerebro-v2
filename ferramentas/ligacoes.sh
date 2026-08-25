#!/usr/bin/env bash
#* PERNA P2 do portao: confere que todo [[wikilink]] resolve para uma nota que existe.
#! POR QUE SUBSTITUI "verificacao de tipo" (§12·4a): markdown nao tem tipo. O que ele tem
#!   e integridade referencial, e ela e a navegacao inteira — o cerebro anterior tinha 1.823
#!   wikilinks e ZERO links markdown. Sem esta perna, um rename de pasta passa verde e o
#!   grafo quebra em silencio (foi o que aconteceu com bancada -> Terminus: 88 links).
set -uo pipefail
cd "$(dirname "$0")/.."

find . -name '*.md' -not -path './.git/*' -not -path './moldes/*' -not -path './docs/*' | sed 's|^\./||' | sort > /tmp/.cv2_notas.$$
#! Wikilink dentro de CRASE nao e link — e a sintaxe sendo explicada. A `meta/lei.md`
#!   documenta o formato do proprio repositorio e escreve `[[nome-do-arquivo]]` como
#!   exemplo; cobrar destino dele seria o portao reprovar a documentacao do portao.
#!   Bloco de codigo (```) cai pela mesma razao.
while IFS= read -r arq; do
  awk '/^```/{d=!d; next} !d{print}' "$arq" | sed 's/`[^`]*`//g'
done < <(find . -name '*.md' -not -path './.git/*' -not -path './moldes/*' -not -path './docs/*') \
  | grep -oE '\[\[[^]|#]+' | sed 's/^\[\[//' | sed 's|[[:space:]]*$||' | sort -u > /tmp/.cv2_alvos.$$


#! Lista de EXCECAO auditavel: alvos que ja estavam quebrados na FONTE. Conserta-los exigiria
#!   INVENTAR o destino, e a lei manda recusar antes de fabricar. Sao reportados como
#!   herdados e nao reprovam — mas qualquer alvo FORA da lista reprova, entao "herdado" nao
#!   vira porta dos fundos. Os dados moram em ferramentas/ (que o migrador NAO
#!   reconstroi); a nota legivel em meta/ e gerada a partir deles.
cut -f1 ferramentas/ligacoes-herdadas.txt 2>/dev/null \
  | grep -v '^#' | sort -u > /tmp/.cv2_herd.$$ || : > /tmp/.cv2_herd.$$

q=0; ok=0; herd=0
while IFS= read -r alvo; do
  [ -z "$alvo" ] && continue
  base="${alvo##*/}"
  if grep -qxF "$alvo.md" /tmp/.cv2_notas.$$ || grep -qF "/$base.md" /tmp/.cv2_notas.$$ || grep -qxF "$base.md" /tmp/.cv2_notas.$$; then
    ok=$((ok+1))
  elif grep -qxF -- "$alvo" /tmp/.cv2_herd.$$; then
    herd=$((herd+1))
  else
    q=$((q+1)); echo "QUEBRADO: [[$alvo]]"
    grep -rlF "[[$alvo]]" --include='*.md' . --exclude-dir=.git --exclude-dir=moldes --exclude-dir=docs | sed 's/^/    citado em: /'
  fi
done < /tmp/.cv2_alvos.$$
rm -f /tmp/.cv2_notas.$$ /tmp/.cv2_alvos.$$ /tmp/.cv2_herd.$$

if [ "$q" -eq 0 ]; then
  echo "P2 OK — 0 quebrados NOVOS de $((ok+herd)) alvos ($herd herdados, ver meta/ligacoes-herdadas)"
  exit 0
fi
echo "P2 FALHOU — $q alvo(s) quebrado(s) NOVO(S), fora dos $herd herdados"; exit 1