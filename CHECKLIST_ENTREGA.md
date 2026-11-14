# Checklist de entrega — Citizen Assist AI (GS 2026.2)

**Prazo:** 19/11/2026, 23h59 (portal da FIAP) · **Hoje:** 14/11/2026
**Equipe:** Bruno (RM 569619), Eduardo (RM 569897), Gustavo (RM 573651)

Cronograma sugerido:

| Data | O que fazer | Quem |
|---|---|---|
| 14/11 (sáb) | Passo 0 (commit) e Passo 1 (conferência manual); recrutar 5 pessoas | Todos |
| 15–16/11 | Passo 2 (teste com usuários, planilhas e relatório) | 2 aplicam, 1 tabula |
| 17/11 | Passo 3 (gravar vídeo técnico PCP) | Todos falam |
| 18/11 | Passo 4 (gravar pitch SERS) | 1 narra, 2 apoiam |
| 19/11 | Passo 5 (revisão, push e entrega do `.txt`) | 1 entrega |

---

## Passo 0 — Subir o estado atual (30 min)

```bash
cd /Users/brunocoutinho/Documents/GlobalSoluctions/Jun
python3 -m unittest discover -s testes -t .     # espera: 148 testes, OK
node mobile/teste-logica.js                     # espera: 78 verificações
git add -A
git commit -m "Alinha base e classes ao enunciado de PCP; documenta público, ODS, pontuação e limitações"
git push origin main
```

- [ ] Repositório abre em https://github.com/C0utinhoxx/citizen-assist-ai **sem login** (janela anônima)
- [ ] `data/base_conhecimento.json` aparece no GitHub (não foi ignorado)
- [ ] Nenhum `.env`, chave de API ou dado pessoal no commit

---

## Passo 1 — Conferência manual da amostra (30–45 min)

Arquivo: [`avaliacao/conferencia_manual.md`](avaliacao/conferencia_manual.md) (9 casos já pré-preenchidos).

- [ ] Um integrante lê cada caso e marca correto/incorreto **conferindo nas fichas**
- [ ] Assina e data no fim do arquivo
- [ ] Troca o status “PENDENTE” por “CONCLUÍDA em __/__/____”
- [ ] Se achar erro, anota no documento e corrige o agente; roda o Golden Dataset de novo

---

## Passo 2 — Teste com pessoas externas (15–16/11)

**Regra:** ≥3 pessoas e ≥10 atendimentos (PCP) + 5 pessoas e 3 tarefas (IA). Não registre nomes nem dados pessoais. Use códigos P01…P05.
Roteiro: [`testes_usuarios/protocolo_rapido.md`](testes_usuarios/protocolo_rapido.md).

### 2.1 Por participante (15–20 min)

1. Abra o **agente de fichas** e aplique as 6 tarefas do protocolo:
   ```bash
   python3 main_agente.py
   ```
2. Abra o **catálogo** e faça 2–3 perguntas na opção **9** (isso gera os indicadores do PCP):
   ```bash
   python3 main.py
   ```
   Sugestão de perguntas: `Como faço o cartão do SUS?`, `Quero a carteirinha do posto`, `Como renovo a CNH?`.
   Ao sair na opção **0**, responda a **nota de facilidade de 1 a 5**.

### 2.2 Registrar

- [ ] `testes_usuarios/planilha.csv` preenchida (uma linha por tarefa; sem dados pessoais)
- [ ] `testes_usuarios/questionario.csv` preenchido (5 perguntas por participante)
- [ ] `testes_usuarios/relatorio.md` preenchido com os totais e as médias
- [ ] Indicadores do PCP copiados da opção **11** e/ou de `data/atendimentos.csv`: % encontrada, % ajudou, tempo médio, tentativas, facilidade, dúvidas sem solução
- [ ] **Uma melhoria concreta** feita por causa do teste (ex.: nova palavra-chave no JSON) e registrada no README

> Dica para a melhoria: se alguém usou uma palavra que não estava na base (ex.: “carteirinha”), adicione em `palavras_chave` da orientação certa, rode de novo e mostre que agora é encontrada.

---

## Passo 3 — Vídeo técnico do PCP (5–8 min, até 17/11)

**Formato:** tela com código legível + programa rodando. Todos os integrantes falam. Sem voz de IA. YouTube **não listado**. Passar de 8 min não é avaliado.

Roteiro obrigatório (um bloco por integrante):

| # | Bloco | O que mostrar |
|---|---|---|
| 1 | Equipe, público e problema (30 s) | idosos + documentos/serviços |
| 2 | JSON | abrir `data/base_conhecimento.json`, explicar um registro, dicionários e tuplas do `buscar()` |
| 3 | Classes | `Orientacao`, `BaseConhecimento`, `Assistente`, `self` e composição (assistente → base → orientações) |
| 4 | Busca | `normalizar()` e `pontuar()` calculando “Como faço o cartão do SUS?” = 3+3+1 = 7 → ALTA |
| 5 | Execução | pergunta encontrada, não encontrada, entrada inválida, CPF bloqueado e navegação por categoria |
| 6 | Alteração ao vivo | pergunta “Onde pego a carteirinha do posto?” **não encontra**; adicionar `"carteirinha"` nas palavras-chave do id 1; rodar de novo → **3 pontos, MÉDIA** |
| 7 | Arquivos | `historico.json`, `atendimentos.csv` e indicadores do teste |
| 8 | Decisão e limitação | decisão: busca por regras (explicável, offline) em vez de embeddings; limitação: só responde o que está na base |

Depois:
- [ ] Upload **não listado**, duração ≤ 8 min
- [ ] Link colado em `pitch/link_video.txt` **e** em `entrega_portal.txt`
- [ ] Commit da alteração ao vivo no JSON (`git add data/base_conhecimento.json`)

---

## Passo 4 — Pitch SERS (≤3 min, até 18/11)

Roteiro pronto: [`pitch/roteiro.md`](pitch/roteiro.md). Descrição/comentário: [`pitch/descricao_youtube.md`](pitch/descricao_youtube.md).

- [ ] Vídeo **não listado**, no máximo 3 min, narração humana
- [ ] Deixa claro a proposta e o tema da GS
- [ ] Comentário fixado: **individual, dupla ou trio + nomes e RMs**
- [ ] Somente **um** integrante entrega
- [ ] Link colado em `pitch/link_video.txt`

---

## Passo 5 — Fechamento e entrega (19/11, antes das 23h59)

### 5.1 Revisão final

```bash
cd /Users/brunocoutinho/Documents/GlobalSoluctions/Jun
python3 -m unittest discover -s testes -t .
node mobile/teste-logica.js
python3 -m avaliacao.executar --modo ambos --juiz deterministico --agente extrativo
python3 main.py        # testar 9 (pergunta), 10 (categorias), 11 (indicadores), 0 (sair)
```

- [ ] 148 testes OK · 78 verificações mobile OK · melhorado 26/26
- [ ] README: integrantes+RMs, público, problema, ODS, execução, pontuação, integrações, fontes, teste com usuários, limitações e **link do vídeo**
- [ ] `entrega_portal.txt` com os 5 campos preenchidos (sem placeholder)
- [ ] Links dos vídeos testados em janela anônima

### 5.2 Publicar

```bash
git add -A
git commit -m "Entrega final: testes com usuarios, videos e indicadores"
git push origin main
```

### 5.3 Portal FIAP

Entregar **apenas** `entrega_portal.txt` em Entregas de Trabalho, até **19/11 23h59**:

```text
Nome do assistente: Citizen Assist AI
Público atendido: pessoas idosas (60+) e familiares/cuidadores
Integrantes e RM: Bruno Riquelme Coutinho Pereira (569619); Eduardo Bigoli Portela (569897); Gustavo Fondato de Souza (573651)
Link do repositório GitHub: https://github.com/C0utinhoxx/citizen-assist-ai
Link do vídeo técnico no YouTube: <link não listado>
```

- [ ] Arquivo `.txt` enviado (só um integrante)
- [ ] Print/comprovante do envio salvo no grupo
- [ ] Repositório e vídeos ainda acessíveis na data da correção

---

## Se algo der errado

| Problema | Solução |
|---|---|
| Teste não deu 148 | rode `python3 -m unittest discover -s testes -t . -v` e veja o módulo que falhou |
| JSON corrompido | `git checkout -- data/base_conhecimento.json` |
| Vídeo passou do tempo | corte o bloco 2 ou 7; o que importa é demonstrar, não explicar tudo |
| Portal fechou | envie por e-mail ao professor **antes** do prazo, com o mesmo `.txt` |
