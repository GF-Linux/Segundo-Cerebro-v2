#!/usr/bin/env bash
#* PERNA P1 do portao: confere que TODA nota tem frontmatter valido e completo.
#! POR QUE ESTA PERNA SUBSTITUI "teste da peca" (§12·4a): este repositorio nao tem funcao
#!   para testar. A unidade aqui e a nota, e o que se pode afirmar dela por maquina e o
#!   schema. O cerebro anterior tinha 51% de cobertura: 209/211 decisoes, mas 6/123 sessoes
#!   e 0/15 status. Metade do corpus nao respondia a consulta nenhuma.
set -uo pipefail
cd "$(dirname "$0")/.."

TIPOS='decisao|sessao|projeto|agora|tarefas|referencias|transversal|meta'
erros=0; total=0

while IFS= read -r f; do
  case "$f" in ./README.md|./INDEX.md|./docs/*|./moldes/*) continue;; esac
  total=$((total+1))
  if [ "$(head -1 "$f")" != "---" ]; then
    echo "SEM FRONTMATTER: $f"; erros=$((erros+1)); continue
  fi
  fm=$(awk 'NR>1{if($0=="---")exit; print}' "$f")
  for campo in tipo projeto data status; do
    grep -qE "^${campo}:[[:space:]]*[^[:space:]]" <<<"$fm" || { echo "FALTA '$campo': $f"; erros=$((erros+1)); }
  done
  grep -qE '^tags:' <<<"$fm" || { echo "FALTA 'tags': $f"; erros=$((erros+1)); }

  tipo=$(grep -E '^tipo:' <<<"$fm" | head -1 | sed 's/^tipo:[[:space:]]*//;s/[[:space:]]*$//')
  grep -qE "^($TIPOS)$" <<<"$tipo" || { echo "TIPO INVALIDO '$tipo': $f"; erros=$((erros+1)); }

  data=$(grep -E '^data:' <<<"$fm" | head -1 | sed 's/^data:[[:space:]]*//;s/[[:space:]]*$//')
  grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' <<<"$data" || { echo "DATA INVALIDA '$data': $f"; erros=$((erros+1)); }

  st=$(grep -E '^status:' <<<"$fm" | head -1 | sed 's/^status:[[:space:]]*//;s/[[:space:]]*$//')
  #! O '#' aqui e defeito medido, nao paranoia: 19 decisoes do cerebro anterior carregavam
  #!   o comentario do molde colado dentro do campo (`vigente  # vigente | revisada-por ...`).
  case "$st" in *'#'*) echo "STATUS COM COMENTARIO DE MOLDE: $f"; erros=$((erros+1));; esac
  case "$st" in
    vigente|revogada|historico) ;;
    revisada-por\ *|revogada-por\ *) ;;
    *) echo "STATUS INVALIDO '$st': $f"; erros=$((erros+1));;
  esac
  #! Fato nao se revoga: sessao nasce e morre 'historico'. E o que autoriza a leitura barata
  #!   a pular sessao sem medo de estar pulando lei.
  if [ "$tipo" = "sessao" ] && [ "$st" != "historico" ]; then
    echo "SESSAO TEM DE SER 'historico', e '$st': $f"; erros=$((erros+1))
  fi
done < <(find . -name '*.md' -not -path './.git/*' | sort)

if [ "$erros" -eq 0 ]; then echo "P1 OK — $total/$total notas com frontmatter valido"; exit 0; fi
echo "P1 FALHOU — $erros problema(s) em $total notas"; exit 1
