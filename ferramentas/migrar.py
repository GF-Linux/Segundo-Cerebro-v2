#!/usr/bin/env python3
#? MIGRADOR — de `segundo-cerebro` (FONTE, so leitura) para este repositorio  2026-08-25
#!
#! 1. Ele e DECLARATIVO e IDEMPOTENTE: apaga o destino e reescreve do zero a cada corrida.
#!    Isso e o que torna a migracao auditavel — a cabeca pode rodar de novo e conferir que
#!    da o mesmo, em vez de acreditar num relatorio meu (§7·D1, arnes commitado).
#! 2. Ele NUNCA escreve na fonte. A fonte e aberta em modo leitura, e o unico caminho de
#!    escrita e DESTINO.
#! 3. Ele nao APAGA conhecimento. Nota nenhuma e descartada: o que sai e codigo, binario,
#!    dado de terceiro, documento pessoal e ponteiro morto. Decisao revogada ENTRA — e o
#!    unico lugar onde o "porque nao" esta escrito.
import re, shutil, sys
from pathlib import Path
from collections import defaultdict

FONTE   = Path('/home/Jared/projetos/segundo-cerebro')
DESTINO = Path('/home/Jared/projetos/segundo-cerebro-v2')

#! D3: a pasta so muda de nome AGORA. Daqui em diante o slug e estavel e o produto vive no
#!   campo `produto:`/`aliases:` — e a regra que impede o terceiro rename. O produto trocou
#!   de nome duas vezes em dois meses e a pasta ficou para tras nas duas.
SLUG = {'bancada': 'terminus', 'dna-contingency': 'easycontig'}

#! D2: documento pessoal e a nota cujo dano cai sobre uma PESSOA, nao sobre um projeto.
#!   `estagio-ecs` e matricula, carga horaria e TCE assinado: vida academica, nao projeto.
FORA = {'estagio-ecs'}

#! Onde o codigo vive HOJE, conferido com test -e nesta maquina. O campo alimenta a perna
#!   P7, que faz `test -e`: ponteiro morto REPROVA o portao. Era o defeito F5 — 23 notas
#!   apontando para uma maquina Windows que nao existe mais, e nada perguntando.
CODIGO = {
    'easycontig':            '/home/Jared/projetos/nucleo-easycontig',
    'terminus':              '/home/Jared/projetos/Terminus',
    'parasite-classifier':   '/home/Jared/projetos/parasite-classifier',
    'jared-agent':           '/home/Jared/projetos/jared-agent',
    'jared-auditor':         '/home/Jared/projetos/jared-auditor',
    'jared-lente':           '/home/Jared/projetos/jared-lente',
    'oficina':               '/home/Jared/projetos/oficina',
    'atlas-3d-morfometrico': '(nao existe ainda)',
    'design-de-sistemas':    '(nao aplicavel)',
    'llm-local':             '(nao aplicavel)',
    'riw-videos':            '(nao aplicavel)',
    'formacao-python':       '(nao localizado)',
    'dna-bank':              '(nao localizado)',
    'design':                '(nao localizado)',
}
RESUMO = {
    'easycontig': 'montagem de contigs e consenso de cromatogramas Sanger, offline',
    'terminus': 'a casca de terminal cujo motor e o Neovim, para o laboratorio',
    'parasite-classifier': 'classificacao de parasitos por imagem — invencao com patente',
    'jared-agent': 'o executor que faz nascer e manter projeto sob o PADRAO',
    'jared-auditor': 'o auditor que le artefato, nunca narrativa',
    'jared-lente': 'a lente para assistir o agente executando',
    'oficina': 'aplicacao C#/Avalonia de bancada',
    'atlas-3d-morfometrico': 'modelos 3D fieis de estruturas que so existem em corte 2D',
    'design-de-sistemas': 'skill de system design replicada em todo projeto novo',
    'llm-local': 'modelo de linguagem rodando na propria maquina',
    'riw-videos': 'edicao dos videos institucionais do Rio Innovation Week',
    'formacao-python': 'a formacao tecnica do autor: Python, C#, bioinformatica, metodo',
    'dna-bank': 'banco brasileiro de sequencias — deposito e indice nacional',
    'design': 'identidade visual e pecas da UFRRJ',
}

#! REDACAO NO LUGAR (D2): a nota entra, o VALOR vira marcador. Apagar a nota do RG apagaria
#!   junto a decisao sobre o deposito de patente. O valor e descartavel; o registro do
#!   porque, nao. Nenhum valor real e impresso por este script, nem em log.
IP_OK = re.compile(r'^(0\.0\.0\.0|127\.0\.0\.1|1\.2\.3\.4|10\.9\.9\.9|255\.\d+\.\d+\.\d+'
                   r'|172\.18\.0\.\d+|192\.0\.2\.\d+|198\.51\.100\.\d+|203\.0\.113\.\d+)$')
RE_IP  = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
RE_RG  = re.compile(r'(\bRG\b[^0-9\n]{0,24})(`?\d{2}[.\-]?\d{3}[.\-]?\d{3}[-\dXx]*`?)')
RE_CPF = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
RE_TEL = re.compile(r'\(?\b\d{2}\)? ?9\d{4}-\d{4}\b')

def redigir(t, contador):
    def _ip(m):
        if IP_OK.match(m.group(0)): return m.group(0)
        contador['ip'] += 1; return '`[IP-REDIGIDO]`'
    t = RE_IP.sub(_ip, t)
    def _rg(m):
        contador['rg'] += 1; return m.group(1) + '`[RG-REDIGIDO]`'
    t = RE_RG.sub(_rg, t)
    def _c(m):
        contador['cpf'] += 1; return '`[CPF-REDIGIDO]`'
    t = RE_CPF.sub(_c, t)
    def _t(m):
        contador['tel'] += 1; return '`[TELEFONE-REDIGIDO]`'
    t = RE_TEL.sub(_t, t)
    return t

def sem_frontmatter(t):
    if not t.startswith('---\n'): return None, t
    fim = t.find('\n---\n', 4)
    if fim == -1: return None, t
    return t[4:fim], t[fim+5:]

def campo(fm, nome, pad=''):
    if not fm: return pad
    m = re.search(rf'^{nome}:[ \t]*(.*)$', fm, re.M)
    if not m: return pad
    #! Corta o comentario do molde colado no campo — 19 decisoes tinham esse residuo, e a
    #!   perna P1 reprova quem o carrega.
    return re.sub(r'\s*#.*$', '', m.group(1)).strip() or pad

#! O vocabulario de `status` e FECHADO de proposito: e ele que torna o log filtravel por
#!   maquina. Duas decisoes da fonte usavam variantes livres. Normalizadas — o texto original
#!   do status vai para o corpo, entao a nuance nao se perde.
NORMALIZA_STATUS = {
    'substituida-por-0003': 'revisada-por [[0003-ide-propria-revertendo-a-0001]]',
    'revertida (migração feita em 2026-08-20)': 'revogada',
}

def frontmatter(tipo, projeto, data, status, tags='[]', extra=None):
    l = ['---', f'tipo: {tipo}', f'projeto: {projeto}', f'data: {data}',
         f'status: {status}', f'tags: {tags}']
    if extra: l += extra
    return '\n'.join(l) + '\n---\n'

def reescrever_links(t):
    #! Reescreve o grafo inteiro numa passada: 241 wikilinks presos ao nome velho da pasta,
    #!   mais `_overview` -> `projeto` e `status` -> `agora`. Sem isto, o rename do D3
    #!   quebraria a navegacao — que E o cerebro: 1.823 wikilinks e zero links markdown.
    def _l(m):
        alvo = m.group(1)
        for velho, novo in SLUG.items():
            alvo = re.sub(rf'(^|/){velho}(/|$)', rf'\g<1>{novo}\g<2>', alvo)
        alvo = re.sub(r'(^|/)_overview$', r'\g<1>projeto', alvo)
        alvo = re.sub(r'(^|/)status(\.md)?$', r'\g<1>agora', alvo)
        #! EU quebrei estes dois, e o portao me pegou:
        #! (a) fundir as sessoes do mesmo dia (D4) apagou `2026-07-05c` e companhia — 10 links
        #!     apontavam para o sufixo que deixou de existir.
        #!   O sufixo nao e so uma letra: ha `2026-08-23-v0370.md` ao lado de `2026-08-23.md`.
        alvo = re.sub(r'(sessoes/\d{4}-\d{2}-\d{2})[-a-z0-9]*$', r'\1', alvo)
        #! (c) as notas de raiz do projeto foram para minuscula (RETOMAR-v320 -> retomar-v320),
        #!     e o link tinha de acompanhar.
        alvo = re.sub(r'^(projetos/[^/]+)/([^/]+)$',
                      lambda k: f'{k.group(1)}/{k.group(2).lower()}'
                                if k.group(2) not in ('projeto','agora','tarefas','sobre','referencias')
                                else f'{k.group(1)}/{k.group(2)}', alvo)
        #! (b) achatar as subpastas (achados/, comparativo-v0003/) mudou o caminho da nota.
        alvo = re.sub(r'(projetos/[^/]+)/(?!decisoes/|sessoes/)([^/]+)/([^/]+)$',
                      lambda k: f'{k.group(1)}/' + re.sub(r'[^a-z0-9.-]+', '-',
                                f'{k.group(2)}-{k.group(3)}'.lower()), alvo)
        return '[[' + alvo + (m.group(2) or '') + ']]'
    return re.sub(r'\[\[([^\]|#]+)([|#][^\]]*)?\]\]', _l, t)

RE_DATA_TIT = re.compile(r'(\d{4}-\d{2}-\d{2})|\((\d{2})/(\d{2})\)')

def data_do_titulo(linha):
    m = RE_DATA_TIT.search(linha)
    if not m: return None
    if m.group(1): return m.group(1)
    return f'2026-{m.group(3)}-{m.group(2)}'

def partir_status(txt):
    #? Decompoe o status.md em (blocos datados, resto sem data).
    #! POR QUE: `status.md` acumulou EPISODIOS DATADOS num arquivo cujo molde pedia
    #!   "Estado geral (1 frase)". O easycontig empilhou 13 blocos `_Atualizado em:` e
    #!   chegou a 804 linhas; o atlas explodiu uma sessao de 2026-08-03 em 10 secoes e nao
    #!   tem sessao NENHUMA — toda a historia dele esta presa ali.
    #! A regra e uniforme: secao COM data e episodio e vai para a sessao daquela data;
    #!   o que sobra SEM data e o status de verdade.
    datados, resto, atual, dt = defaultdict(list), [], None, None
    for linha in txt.split('\n'):
        if linha.startswith('_Atualizado em:'):
            d = data_do_titulo(linha)
            #! A linha-marcador ENTRA no bloco. Ela carrega o qualificador — "(noite)",
            #!   "(tarde)", "(sessao c)" — que e a unica coisa que distingue dois blocos do
            #!   MESMO dia depois que eles se fundem numa sessao so.
            if d: dt, atual = d, 'datado'; datados[dt].append(linha); continue
        if re.match(r'^#{2,3} ', linha):
            d = data_do_titulo(linha)
            if d: dt, atual = d, 'datado'; datados[dt].append(linha); continue
            atual, dt = 'resto', None
        (datados[dt] if atual == 'datado' and dt else resto).append(linha)
    return datados, resto

def main():
    cont = defaultdict(int)
    for d in ['projetos', 'transversal', 'meta']:
        if (DESTINO/d).exists(): shutil.rmtree(DESTINO/d)
    (DESTINO/'transversal').mkdir(parents=True, exist_ok=True)

    projetos = sorted(p.name for p in (FONTE/'projetos').iterdir()
                      if p.is_dir() and not p.name.startswith('.'))
    for velho in projetos:
        if velho in FORA:
            cont['projetos_fora'] += 1; continue
        novo_slug = SLUG.get(velho, velho)
        novo = novo_slug
        org, dst = FONTE/'projetos'/velho, DESTINO/'projetos'/novo
        (dst/'decisoes').mkdir(parents=True, exist_ok=True)
        (dst/'sessoes').mkdir(parents=True, exist_ok=True)

        # ---- decisoes: append-only, entram TODAS, inclusive as revogadas ----
        for f in sorted((org/'decisoes').glob('*.md')) if (org/'decisoes').exists() else []:
            fm, corpo = sem_frontmatter(f.read_text(encoding='utf-8'))
            st = campo(fm, 'status', 'vigente') or 'vigente'
            if st in NORMALIZA_STATUS:
                orig_st = st; st = NORMALIZA_STATUS[st]
                corpo = (f'<!-- status na fonte: "{orig_st}" — normalizado para o vocabulario '
                         f'fechado do frontmatter. -->\n' + corpo)
                cont['status_normalizado'] += 1
            data = campo(fm, 'data') or '2026-07-01'
            tags = campo(fm, 'tags', '[]')
            saida = frontmatter('decisao', novo, data, reescrever_links(st), tags) + \
                    redigir(reescrever_links(corpo.lstrip('\n')), cont)
            (dst/'decisoes'/f.name).write_text(saida, encoding='utf-8')
            cont['decisoes'] += 1
            if st != 'vigente': cont['decisoes_ja_nao_valem'] += 1

        # ---- sessoes: FUNDIDAS por dia (D4). Nenhuma linha se perde. ----
        porta = defaultdict(list)
        for f in sorted((org/'sessoes').glob('*.md')) if (org/'sessoes').exists() else []:
            d = re.match(r'(\d{4}-\d{2}-\d{2})', f.stem)
            porta[d.group(1) if d else '2026-07-01'].append(f)

        # ---- status.md: episodio datado vai para a sessao do dia ----
        extra_sessao, resto_status = defaultdict(list), []
        if (org/'status.md').exists():
            _, corpo = sem_frontmatter((org/'status.md').read_text(encoding='utf-8'))
            datados, resto_status = partir_status(corpo)
            for d, linhas in datados.items(): extra_sessao[d] = linhas

        for dia in sorted(set(porta) | set(extra_sessao)):
            partes = []
            for f in porta.get(dia, []):
                _, corpo = sem_frontmatter(f.read_text(encoding='utf-8'))
                corpo = corpo.strip('\n')
                if len(porta[dia]) > 1:
                    partes.append(f'<!-- vinha de {f.name} -->\n{corpo}')
                    cont['sessoes_fundidas'] += 1
                else:
                    partes.append(corpo)
            if dia in extra_sessao:
                bloco = '\n'.join(extra_sessao[dia]).strip('\n')
                if bloco:
                    partes.append('## Resumo que estava empilhado no status.md\n\n' + bloco)
                    cont['blocos_de_status_realocados'] += 1
            texto = '\n\n'.join(p for p in partes if p.strip())
            saida = frontmatter('sessao', novo, dia, 'historico') + \
                    redigir(reescrever_links(texto), cont) + '\n'
            (dst/'sessoes'/f'{dia}.md').write_text(saida, encoding='utf-8')
            cont['sessoes'] += 1

        # ---- projeto.md (era _overview.md) ----
        ov = org/'_overview.md'
        corpo_ov = sem_frontmatter(ov.read_text(encoding='utf-8'))[1] if ov.exists() else f'# {novo}\n'
        linhas_ov, vistos = [], 0
        for linha in reescrever_links(corpo_ov).split('\n'):
            #! O caminho do codigo sai do CORPO e passa a viver so no campo `codigo:`, que a
            #!   perna P7 testa. Um caminho em prosa e um ponteiro que ninguem confere.
            if re.match(r'^\*\*Local do c[oó]digo', linha.strip()): continue
            linhas_ov.append(linha); vistos += 1
            if vistos >= 16: break
        #! O TETO NAO SE PAGA COM CONHECIMENTO. A primeira versao cortava o _overview em 16
        #!   linhas para caber no teto de 30 do projeto.md e JOGAVA O RESTO FORA — 118 linhas,
        #!   61 delas so no jared-auditor. A auditoria de perda pegou; a contagem de arquivos
        #!   nao teria pego, porque o arquivo existia.
        #! projeto.md e a CARTEIRA DE IDENTIDADE (curta, no caminho de leitura barata);
        #!   sobre.md e o texto inteiro, verbatim, FORA desse caminho.
        alias = f'[{velho}]' if velho in SLUG else '[]'
        prod  = {'easycontig': 'EasyContig BR', 'terminus': 'Terminus'}.get(novo, novo)
        extra = [f'produto: {prod}', f'aliases: {alias}',
                 f'codigo: {CODIGO.get(novo, "(nao localizado)")}',
                 f'resumo: {RESUMO.get(novo, novo)}']
        cabeca = frontmatter('projeto', novo, '2026-08-25', 'vigente', '[]', extra)
        corpo  = redigir('\n'.join(linhas_ov).strip('\n'), cont)
        inteiro = redigir(reescrever_links(corpo_ov).strip('\n'), cont)
        if len(inteiro.split('\n')) > len(corpo.split('\n')):
            corpo += f'\n\n**O texto completo:** [[projetos/{novo}/sobre]]'
            (dst/'sobre.md').write_text(
                frontmatter('transversal', novo, '2026-08-25', 'vigente') +
                f'# Sobre — {novo}\n\n'
                '<!-- O _overview.md do cerebro anterior, INTEIRO e verbatim. O projeto.md\n'
                '     guarda so a identidade, porque ele e lido em toda sessao (perna P6). -->\n\n'
                + inteiro + '\n', encoding='utf-8')
            cont['sobre'] += 1
        (dst/'projeto.md').write_text(cabeca + corpo + '\n', encoding='utf-8')

        # ---- tarefas.md: TODO o resto do status.md, verbatim. Nada se perde. ----
        resto = '\n'.join(resto_status).strip('\n')
        if resto:
            (dst/'tarefas.md').write_text(
                frontmatter('tarefas', novo, '2026-08-25', 'vigente') +
                f'# Tarefas — {novo}\n\n'
                '<!-- Veio do status.md do cerebro anterior: tudo que NAO carregava data.\n'
                '     O que carregava data virou episodio e foi para a sessao daquele dia. -->\n\n'
                + redigir(reescrever_links(resto), cont) + '\n', encoding='utf-8')
            cont['tarefas'] += 1

        # ---- agora.md: NOVO, curto, com teto de 25 linhas (perna P5) ----
        prox = []
        m = re.search(r'^#{2,3} .*(A fazer|Fazendo|Proximo|Próximo|Retomar).*$', resto, re.M)
        if m:
            for linha in resto[m.end():].split('\n'):
                if re.match(r'^#{2,3} ', linha): break
                #! prox tambem passava ao largo do reescritor de links.
                if re.match(r'^\s*[-*] ', linha): prox.append(reescrever_links(linha.strip()))
                if len(prox) >= 3: break
        if not prox: prox = ['- [ ] (definir na proxima sessao)']
        ult = sorted((dst/'sessoes').glob('*.md'))
        ref = f'[[projetos/{novo}/sessoes/{ult[-1].stem}]]' if ult else '(sem sessao)'
        #! agora.md tem de CARREGAR o estado, nao apontar para ele. A primeira versao dizia
        #!   "ver a sessao mais recente" — o que empurra o custo de volta para a sessao e
        #!   faz o arquivo nao valer o que ocupa. O estado sai do bloco datado mais recente
        #!   do status.md, que e onde ele de fato estava escrito.
        estado = ''
        if extra_sessao:
            ultimo = sorted(extra_sessao)[-1]
            for linha in extra_sessao[ultimo]:
                l = re.sub(r'^[>*_#\s]+', '', linha).strip()
                l = re.sub(r'\*\*|`|➡️|⚠️', '', l).strip()
                #! O corte em 240 partia wikilink no meio e produzia link malformado — o
                #!   riw-videos saiu com um `[[` sem fechamento. O Estado e uma FRASE: tira-se
                #!   o link dela, que tem lugar proprio logo abaixo.
                l = re.sub(r'\[\[[^\]]*\]?\]?', '', l).strip(' ([,;')
                if len(l) > 40: estado = l[:240].rstrip(' ,;([-'); break
        if not estado: estado = f'ver a sessao mais recente, {ref}'
        (dst/'agora.md').write_text(
            frontmatter('agora', novo, '2026-08-25', 'vigente') +
            f'# Agora — {novo}\n\n'
            f'**Estado:** {estado}\n\n'
            f'<!-- vem do bloco datado mais recente do status.md da fonte -->\n\n'
            '## Proximo passo\n' + '\n'.join(prox[:3]) + '\n\n'
            f'## Onde esta o resto\n- backlog completo: [[projetos/{novo}/tarefas]]\n'
            f'- decisoes vigentes: `ferramentas/vigentes.sh {novo}`\n', encoding='utf-8')

        # ---- subpastas que nao sao decisoes/ nem sessoes/ ----
        #! DEFEITO ACHADO NA AUDITORIA DE PERDA: a primeira versao so olhava decisoes/,
        #!   sessoes/ e a raiz do projeto, e deixou 7 notas reais para tras — entre elas
        #!   `achados/skills-injetadas-nao-chamadas`, que e a fonte de um item do §15.4 do
        #!   PADRAO. A auditoria de linha (672 perdidas) foi o que pegou; a contagem de
        #!   arquivos, sozinha, nao teria pego.
        #! Elas sao aplanadas para a raiz do projeto com o nome da subpasta como prefixo:
        #!   a planta aprovada nao tem subpasta livre, e nota de raiz ja e um tipo dela.
        for sub in sorted(d for d in org.iterdir() if d.is_dir()):
            if sub.name in ('decisoes', 'sessoes') or sub.name.startswith('.'): continue
            for f in sorted(sub.rglob('*.md')):
                #! Repo de terceiro vendorizado nao e conhecimento deste cerebro.
                if 'machine-learning-2025-main' in str(f) or '.venv' in str(f): continue
                fm, corpo = sem_frontmatter(f.read_text(encoding='utf-8'))
                nome = re.sub(r'[^a-z0-9.-]+', '-', f'{sub.name}-{f.name}'.lower())
                (dst/nome).write_text(
                    frontmatter('transversal', novo_slug, campo(fm, 'data') or '2026-07-01', 'vigente') +
                    redigir(reescrever_links(corpo.lstrip('\n')), cont) + '\n', encoding='utf-8')
                cont['notas_de_subpasta'] += 1

        # ---- referencias.md e as notas soltas na raiz do projeto ----
        for f in sorted(org.glob('*.md')):
            if f.name in ('_overview.md', 'status.md'): continue
            fm, corpo = sem_frontmatter(f.read_text(encoding='utf-8'))
            tipo = 'referencias' if f.stem == 'referencias' else 'transversal'
            nome = re.sub(r'[^a-z0-9.-]+', '-', f.name.lower())
            (dst/nome).write_text(
                frontmatter(tipo, novo, campo(fm, 'data') or '2026-07-01', 'vigente') +
                redigir(reescrever_links(corpo.lstrip('\n')), cont) + '\n', encoding='utf-8')
            cont['notas_soltas'] += 1

    # ---- transversal/ ----
    for f in sorted((FONTE/'transversal').glob('*.md')):
        fm, corpo = sem_frontmatter(f.read_text(encoding='utf-8'))
        (DESTINO/'transversal'/f.name).write_text(
            frontmatter('transversal', 'transversal', campo(fm, 'data') or '2026-07-01', 'vigente') +
            redigir(reescrever_links(corpo.lstrip('\n')), cont) + '\n', encoding='utf-8')
        cont['transversal'] += 1

    # ---- meta/ ----
    (DESTINO/'meta'/'decisoes').mkdir(parents=True, exist_ok=True)
    (DESTINO/'meta'/'sessoes').mkdir(parents=True, exist_ok=True)
    for sub, tipo in (('decisoes', 'decisao'), ('sessoes', 'sessao')):
        for f in sorted((FONTE/'meta'/sub).glob('*.md')):
            fm, corpo = sem_frontmatter(f.read_text(encoding='utf-8'))
            data = campo(fm, 'data') or (re.match(r'(\d{4}-\d{2}-\d{2})', f.stem).group(1)
                                         if re.match(r'\d{4}-\d{2}-\d{2}', f.stem) else '2026-07-01')
            st = 'historico' if tipo == 'sessao' else (campo(fm, 'status', 'vigente') or 'vigente')
            (DESTINO/'meta'/sub/f.name).write_text(
                frontmatter(tipo, 'meta', data, reescrever_links(st)) +
                redigir(reescrever_links(corpo.lstrip('\n')), cont) + '\n', encoding='utf-8')
            cont['meta'] += 1

    # ---- meta: identidade, lei, agora e tarefas ----
    #! DEFEITO ACHADO NA MESMA AUDITORIA: meta/ so tinha decisoes/ e sessoes/ tratadas, e o
    #!   meta/status.md (26 linhas) ficava para tras. E a `lei` vivia escondida em
    #!   .claude/skills/segundo-cerebro/SKILL.md — config de ferramenta, que nao se versiona.
    #!   O protocolo de leitura e a peca mais importante do repositorio: ele sai da pasta de
    #!   config e vira documento de primeira classe.
    ms = FONTE/'meta'/'status.md'
    corpo_ms = sem_frontmatter(ms.read_text(encoding='utf-8'))[1] if ms.exists() else ''
    datados_m, resto_m = partir_status(corpo_ms)
    (DESTINO/'meta'/'projeto.md').write_text(
        frontmatter('projeto', 'meta', '2026-08-25', 'vigente', '[]',
                    ['produto: segundo cerebro', 'aliases: []',
                     'codigo: /home/Jared/projetos/segundo-cerebro-v2',
                     'resumo: o cerebro falando de si mesmo — formato, protocolo e escopo']) +
        '# meta\n\n**O que e:** este repositorio, visto por dentro: que forma as notas tem,\n'
        'que protocolo se segue ao abrir e ao fechar sessao, e o que nunca entra.\n\n'
        '**Objetivo:** que a forma seja consultavel por maquina e barata de ler por humano.\n\n'
        '**Autoria:** Gustavo Goncalves Freitas (LHV/UFRRJ).\n', encoding='utf-8')
    (DESTINO/'meta'/'agora.md').write_text(
        frontmatter('agora', 'meta', '2026-08-25', 'vigente') +
        '# Agora — meta\n\n'
        '**Estado, em uma frase:** repositorio novo de pe, migrado da fonte, portao verde.\n\n'
        '## Proximo passo\n- [ ] a cabeca ratifica os desvios listados em [[meta/tarefas]]\n\n'
        '## Onde esta o resto\n- backlog: [[meta/tarefas]]\n- a lei deste repo: [[meta/lei]]\n',
        encoding='utf-8')
    #! DEFEITO: `datados_m` era calculado e nunca escrito — os blocos datados do
    #!   meta/status.md caiam no chao. Mesma regra dos projetos: episodio datado vira sessao.
    for d, ls in datados_m.items():
        alvo = DESTINO/'meta'/'sessoes'/f'{d}.md'
        bloco = '## Resumo que estava empilhado no status.md\n\n' + '\n'.join(ls).strip('\n')
        if alvo.exists():
            alvo.write_text(alvo.read_text(encoding='utf-8').rstrip('\n') + '\n\n' +
                            redigir(reescrever_links(bloco), cont) + '\n', encoding='utf-8')
        else:
            alvo.write_text(frontmatter('sessao', 'meta', d, 'historico') +
                            redigir(reescrever_links(bloco), cont) + '\n', encoding='utf-8')
        cont['blocos_de_status_realocados'] += 1
    if resto_m:
        (DESTINO/'meta'/'tarefas.md').write_text(
            frontmatter('tarefas', 'meta', '2026-08-25', 'vigente') +
            '# Tarefas — meta\n\n' + redigir(reescrever_links('\n'.join(resto_m).strip('\n')), cont) + '\n',
            encoding='utf-8')
    skill = FONTE/'.claude'/'skills'/'segundo-cerebro'/'SKILL.md'
    lei = sem_frontmatter(skill.read_text(encoding='utf-8'))[1] if skill.exists() else ''
    (DESTINO/'meta'/'lei.md').write_text(
        frontmatter('meta', 'meta', '2026-08-25', 'vigente') +
        '# A lei deste repositorio\n\n'
        '<!-- Veio de .claude/skills/segundo-cerebro/SKILL.md, que era config de ferramenta e\n'
        '     portanto nao versionavel. O protocolo de leitura nao pode morar num lugar que o\n'
        '     .gitignore exclui. -->\n\n' +
        reescrever_links(lei.lstrip('\n')) + '\n', encoding='utf-8')
    cont['meta'] += 4

    print('── migracao ──')
    for k in sorted(cont): print(f'  {k:34} {cont[k]}')

if __name__ == '__main__':
    sys.exit(main())
