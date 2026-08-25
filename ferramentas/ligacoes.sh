#!/usr/bin/env bash
#* PERNA P2 do portao: confere que todo [[wikilink]] resolve para uma nota que existe.
#! POR QUE SUBSTITUI "verificacao de tipo" (§12·4a): markdown nao tem tipo. O que ele tem
#!   e integridade referencial, e ela e a navegacao inteira — o cerebro anterior tinha 1.823
#!   wikilinks e ZERO links markdown. Sem esta perna, um rename de pasta passa verde e o
#!   grafo quebra em silencio (foi o que aconteceu com bancada -> Terminus: 88 links).
set -uo pipefail
cd "$(dirname "$0")/.."

find . -name '*.md' -not -path './.git/*' -not -path './moldes/*' -not -path './docs/*' | sed 's|^\./||' | sort > /tmp/.cv2_notas.$$
grep -rhoE '\[\[[^]|#]+' --include='*.md' . --exclude-dir=.git --exclude-dir=moldes --exclude-dir=docs \
  | sed 's/^\[\[//' | sed 's|[[:space:]]*$||' | sort -u > /tmp/.cv2_alvos.$$

q=0; ok=0
while IFS= read -r alvo; do
  [ -z "$alvo" ] && continue
  base="${alvo##*/}"
  if grep -qxF "$alvo.md" /tmp/.cv2_notas.$$ || grep -qF "/$base.md" /tmp/.cv2_notas.$$ || grep -qxF "$base.md" /tmp/.cv2_notas.$$; then
    ok=$((ok+1))
  else
    q=$((q+1)); echo "QUEBRADO: [[$alvo]]"
    grep -rlF "[[$alvo]]" --include='*.md' . --exclude-dir=.git --exclude-dir=moldes --exclude-dir=docs | sed 's/^/    citado em: /'
  fi
done < /tmp/.cv2_alvos.$$
rm -f /tmp/.cv2_notas.$$ /tmp/.cv2_alvos.$$

if [ "$q" -eq 0 ]; then echo "P2 OK — 0 quebrados de $ok alvos distintos"; exit 0; fi
echo "P2 FALHOU — $q alvo(s) quebrado(s) de $((ok+q))"; exit 1
