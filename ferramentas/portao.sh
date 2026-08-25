#!/usr/bin/env bash
#* O PORTAO (§12·4). Roda as 7 pernas e sai 0 SOMENTE se as sete passarem.
#! REGRA QUE MANDA AQUI (§12·4b): o que o portao MEDE, o portao TRAVA. Numero que ele
#!   imprime e nao entra no veredito nao e perna, e enfeite. Foi assim que a v0.4 falhou:
#!   imprimia os ciclos — o alvo declarado da corrida — e dava "PORTAO VERDE" com o ciclo
#!   reintroduzido. Aqui a P6 REPROVA.
set -uo pipefail
cd "$(dirname "$0")/.."
falhas=0
perna() { echo; echo "──────── $1"; shift; "$@" || { falhas=$((falhas+1)); echo "   ^ REPROVOU"; }; }

if [ "${1:-}" = "--conduta" ]; then
  #* PERNA P7 isolada: prova de vida do protocolo de leitura (§12·4c).
  p="${2:?uso: portao.sh --conduta <slug>}"; e=0
  echo "P7 CONDUTA — orientando em '$p' pelo caminho barato:"
  echo "  1. linha do projeto no INDEX:"
  grep -q "projetos/$p/projeto" INDEX.md && echo "     ok" || { echo "     FALTA"; e=1; }
  echo "  2. projeto.md e o caminho do codigo:"
  cam=$(awk 'NR>1{if($0=="---")exit; if(/^codigo:/){sub(/^codigo:[[:space:]]*/,"");print;exit}}' "projetos/$p/projeto.md" 2>/dev/null)
  if [ -z "$cam" ]; then echo "     SEM campo codigo:"; e=1
  elif [ "$cam" = "(nao existe ainda)" ] || [ "$cam" = "(nao aplicavel)" ]; then echo "     '$cam' — declarado, aceito"
  elif [ -e "$cam" ]; then echo "     '$cam' EXISTE"
  else echo "     '$cam' NAO EXISTE — ponteiro morto"; e=1; fi
  echo "  3. agora.md tem proximo passo:"
  grep -qi 'proximo passo\|próximo passo' "projetos/$p/agora.md" 2>/dev/null && echo "     ok" || { echo "     FALTA"; e=1; }
  echo "  4. decisoes vigentes:"
  n=$(ferramentas/vigentes.sh "$p" 2>/dev/null | sed -n '/== VIGENTES ==/,/== JA NAO/p' | grep -c '\.md$' || true)
  [ "${n:-0}" -gt 0 ] && echo "     $n vigentes" || { echo "     ZERO vigentes"; e=1; }
  echo "  5. sessao mais recente:"
  u=$(ls -1 "projetos/$p/sessoes/"*.md 2>/dev/null | sort | tail -1)
  [ -n "$u" ] && echo "     $(basename "$u")" || { echo "     NENHUMA"; e=1; }
  [ "$e" -eq 0 ] && { echo "P7 OK"; exit 0; } || { echo "P7 FALHOU"; exit 1; }
fi

echo "═══ PORTAO — segundo cerebro ═══"
perna "P1 · frontmatter valido em 100% das notas"        ferramentas/frontmatter.sh
perna "P2 · todo wikilink resolve"                        ferramentas/ligacoes.sh

perna "P3 · indice gerado, reproduzivel e igual ao disco" bash -c '
  ferramentas/indice.sh --stdout > /tmp/.p3a.$$; ferramentas/indice.sh --stdout > /tmp/.p3b.$$
  r=0
  cmp -s /tmp/.p3a.$$ /tmp/.p3b.$$ || { echo "NAO REPRODUZIVEL: duas geracoes diferem"; r=1; }
  cmp -s /tmp/.p3a.$$ INDEX.md    || { echo "INDEX.md no disco DIFERE do gerado (editado a mao?)"; r=1; }
  rm -f /tmp/.p3a.$$ /tmp/.p3b.$$
  [ $r -eq 0 ] && echo "P3 OK — geracao estavel e igual ao disco"; exit $r'

perna "P4 · nada proibido entrou (§8·S1)" bash -c '
  r=0; m() { echo "   $1"; r=1; }
  s=$(git ls-files | grep -Ei "\.(ab1|abi|scf|fasta|fastq|fa|afa|seq|phy|nex)$" || true)
  [ -n "$s" ] && m "SEQUENCIA RASTREADA: $(wc -l <<<"$s") arquivo(s)"
  b=$(git ls-files | grep -Ei "\.(zip|pdf|docx|odt|xlsx|parquet|pkl|pyc|so|exe|jpe?g|mov|mp4)$" || true)
  [ -n "$b" ] && m "BINARIO RASTREADO: $(wc -l <<<"$b")"
  #! Escopado a "fora de ferramentas/": ver a excecao no .gitignore.
  p=$(git ls-files | grep -Ei "\.(py|ts|cs|ipynb)$" | grep -v "^ferramentas/" || true)
  [ -n "$p" ] && m "CODIGO DE OUTRO PROJETO: $(wc -l <<<"$p")"
  c=$(git grep -lE "(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|ssh-rsa AAAA|BEGIN [A-Z ]*PRIVATE KEY|xox[baprs]-)" -- "*.md" ":(exclude)docs/" 2>/dev/null || true)
  [ -n "$c" ] && m "CREDENCIAL: $c"
  x=$(git grep -lE "[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}" -- "*.md" ":(exclude)docs/" 2>/dev/null || true)
  [ -n "$x" ] && m "CPF: $x"
  t=$(git grep -lE "\(?[0-9]{2}\)? ?9[0-9]{4}-[0-9]{4}" -- "*.md" ":(exclude)docs/" 2>/dev/null || true)
  [ -n "$t" ] && m "TELEFONE: $t"
  g=$(git grep -lE "\bRG\b.{0,20}[0-9]{2}[.-]?[0-9]{3}" -- "*.md" ":(exclude)docs/" 2>/dev/null || true)
  [ -n "$g" ] && m "NUMERO DE IDENTIDADE: $g"
  #! Le a MESMA lista que o redator (ferramentas/ips-permitidos.txt). Ver o cabecalho dela.
  i=$(git grep -hoE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" -- "*.md" ":(exclude)docs/" 2>/dev/null \
      | grep -vEf <(grep -v "^#" ferramentas/ips-permitidos.txt | grep -v "^$") | sort -u || true)
  [ -n "$i" ] && m "IP ROTEAVEL: $(wc -l <<<"$i") distinto(s)"
  #! docs/ fica FORA das varreduras de padrao acima, e a razao e estrutural: docs/portao.md
  #!   contem os PROPRIOS regexes desta perna dentro de um bloco de codigo, entao ela casa
  #!   consigo mesma. Um portao que reprova a propria documentacao e um medidor que mente.
  #! O BURACO QUE ISSO ABRE e fechado aqui: docs/ e um conjunto FECHADO de 4 arquivos. Nao
  #!   da para esconder nota nova ali dentro.
  esperado="diario.md fluxo.md fluxo.png fluxo.svg portao.md"
  achado=$(ls -1 docs/ 2>/dev/null | sort | tr "\n" " " | sed "s/ $//")
  [ "$achado" = "$esperado" ] && : || m "docs/ mudou de conjunto: esperado [$esperado], achado [$achado]"
  [ $r -eq 0 ] && echo "P4 OK — nenhuma sequencia, binario, codigo, credencial ou PII rastreada"; exit $r'

perna "P5 · teto de tamanho na camada que se le SEMPRE" bash -c '
  r=0
  for f in projetos/*/agora.md meta/agora.md; do
    [ -e "$f" ] || continue; n=$(wc -l < "$f")
    [ "$n" -gt 25 ] && { echo "   $f: $n linhas (teto 25)"; r=1; }
  done
  for f in projetos/*/projeto.md meta/projeto.md; do
    [ -e "$f" ] || continue; n=$(wc -l < "$f")
    [ "$n" -gt 30 ] && { echo "   $f: $n linhas (teto 30)"; r=1; }
  done
  np=$(ls -d projetos/*/ 2>/dev/null | wc -l); ni=$(wc -l < INDEX.md)
  [ "$ni" -gt $((np + 12)) ] && { echo "   INDEX.md: $ni linhas (teto $((np+12)))"; r=1; }
  [ $r -eq 0 ] && echo "P5 OK — nenhum estouro de teto"; exit $r'

perna "P6 · ALVO DA CORRIDA: orientar em <= 3.000 tokens" bash -c '
  r=0; pior=0; pnome=""
  for d in projetos/*/; do
    p=$(basename "$d"); [ -f "$d/projeto.md" ] || continue
    #! O caminho barato e INDEX + projeto + agora, e NAO inclui a sessao. A sessao saiu
    #!   porque agora.md passou a carregar o estado — era ela que estourava o orcamento
    #!   (design-de-sistemas: 5.080 tokens, com uma sessao fundida de 283 linhas). Manter a
    #!   sessao no caminho seria pagar duas vezes pela mesma informacao.
    b=$(cat INDEX.md "$d/projeto.md" "$d/agora.md" 2>/dev/null | wc -c)
    t=$(( b * 10 / 36 ))
    printf "   %-26s %6d tokens\n" "$p" "$t"
    [ "$t" -gt "$pior" ] && { pior=$t; pnome=$p; }
    [ "$t" -gt 3000 ] && { echo "      ^ ESTOUROU o teto de 3.000"; r=1; }
  done
  echo "   pior caso: $pnome = $pior tokens (hoje, no cerebro anterior: 58.594)"
  [ $r -eq 0 ] && echo "P6 OK — todos dentro do orcamento"; exit $r'

perna "P7 · conduta: o protocolo de leitura responde (§12·4c)" bash -c '
  #! TODO projeto tem o `codigo:` conferido, nao so um. O defeito F5 — 23 notas apontando
  #!   para uma maquina Windows que nao existe mais — era do REPOSITORIO, nao de um projeto.
  #!   Uma perna que amostra um projeto so deixaria 13 ponteiros sem ninguem perguntando.
  r=0
  for d in projetos/*/; do
    p=$(basename "$d"); [ -f "$d/projeto.md" ] || continue
    cam=$(awk "NR>1{if(\$0==\"---\")exit; if(/^codigo:/){sub(/^codigo:[[:space:]]*/,\"\");print;exit}}" "$d/projeto.md")
    case "$cam" in
      "(nao existe ainda)"|"(nao aplicavel)"|"(nao localizado)")
        printf "   %-26s %s — declarado, aceito\n" "$p" "$cam" ;;
      "") printf "   %-26s SEM campo codigo:\n" "$p"; r=1 ;;
      *) if [ -e "$cam" ]; then printf "   %-26s existe\n" "$p"
         else printf "   %-26s PONTEIRO MORTO: %s\n" "$p" "$cam"; r=1; fi ;;
    esac
  done
  #* E a prova de vida completa no projeto mais documentado.
  maior=$(for d in projetos/*/; do echo "$(ls $d/decisoes/*.md 2>/dev/null | wc -l) $(basename $d)"; done | sort -rn | head -1 | cut -d" " -f2)
  echo "   --- prova de vida completa em: $maior"
  ferramentas/portao.sh --conduta "$maior" | sed "s/^/   /" || r=1
  exit $r'

echo; echo "═══════════════════════════════════"
[ "$falhas" -eq 0 ] && { echo "PORTAO VERDE — 7/7 pernas"; exit 0; }
echo "PORTAO VERMELHO — $falhas de 7 pernas reprovaram"; exit 1
