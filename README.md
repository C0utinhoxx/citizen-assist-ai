# Citizen Assist AI

**Equipe:** Bruno Riquelme Coutinho Pereira (RM 569619) · Eduardo Bigoli Portela (RM 569897) · Gustavo Fondato de Souza (RM 573651)  
**Turma:** 1CCPX · **Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai

Solução em **Python** para a **Global Solution 2026.2 — Citizen Tech**. O projeto reúne um catálogo de serviços públicos com estruturas de dados implementadas manualmente, um agente de IA para orientação sobre documentos pessoais e uma versão mobile acessível.

## Visão geral

O Citizen Assist AI ajuda o cidadão a encontrar informações sobre serviços públicos e documentos pessoais. A solução combina:

- catálogo de serviços com **lista encadeada manual**, busca, ordenação e indicadores;
- agente que responde **exclusivamente** com base nas fichas FC-01 a FC-07;
- interface mobile em HTML único, com voz e acessibilidade;
- avaliação automatizada no Golden Dataset, com juiz determinístico e **LLM as a Judge**.

## Status

| Módulo | Status |
|---|---|
| Catálogo de serviços | Concluído e testado |
| Agente de documentos | Concluído; fichas oficiais importadas e avaliação LLM executada |
| Mobile | Concluído e testado |
| Validação humana | Pendente: conferência manual e teste com 5 pessoas |
| Vídeo | Pendente: roteiro pronto, gravação e publicação a fazer |

> **Importante:** os resultados de LLM são reais e foram produzidos com OpenAI `gpt-4o-mini`. Nenhum resultado de teste com pessoas ou de gravação foi inventado. O que ainda não foi executado está marcado como pendente.

## Funcionalidades

### Catálogo de serviços

- Cadastra, consulta, atualiza e exclui serviços em uma **lista encadeada implementada pela equipe**.
- Consulta por ID e pesquisa por título, categoria ou descrição.
- Ordena por título, categoria ou ID com **Selection Sort** próprio.
- Analisa os serviços por categoria e gera indicadores de atendimento.
- Responde perguntas em texto livre com pontuação e confiança.
- Mantém histórico, exporta CSV e protege dados pessoais.
- Persiste o catálogo em JSON.

### Agente de documentos

- Responde sobre RG, CPF, título de eleitor, carteira de trabalho, certidões e CNH.
- Usa **somente** as fichas FC-01 a FC-07 como fonte de verdade.
- Cita a ficha de origem e a data de verificação em toda resposta de escopo.
- Admite desconhecimento quando a ficha não responde.
- Recusa e oculta CPF, RG, CNH, título, telefone, e-mail, endereço e números longos.
- Neutraliza prompt injection e trata a mensagem do usuário como dado, nunca como instrução.
- Não agenda, não consulta sistemas do governo e não é um canal oficial.
- Não grava perguntas em arquivo, banco ou histórico.

### Mobile

A versão mobile completa fica em um único HTML, com lista encadeada, Selection Sort, busca, histórico, indicadores, CSV, voz e acessibilidade. Veja [`mobile/README.md`](mobile/README.md).

## Arquitetura

- **Python 3.9+** no núcleo e no agente.
- **Lista encadeada manual** e **Selection Sort** implementados pela equipe.
- **JSON** para persistência local do catálogo e do histórico.
- **LangGraph** para orquestração do agente, com fallback sequencial quando a biblioteca não está instalada.
- **Provedores compatíveis com OpenAI**: Groq, OpenAI e Ollama local.
- **HTML, CSS e JavaScript** no app mobile, sem framework.

## Como executar

Pré-requisito do núcleo: **Python 3.9 ou superior**, sem dependências externas.

```bash
cd Jun
python3 main.py
```

No menu do catálogo, a opção **13** abre o agente de documentos. O agente também pode ser executado sozinho:

```bash
python3 main_agente.py
```

### LangGraph (opcional)

O fluxo do agente usa **LangGraph** quando a biblioteca está instalada. Sem ela, o mesmo fluxo roda em modo sequencial, com as mesmas regras e respostas.

```bash
python3 -m pip install -r requirements.txt
```

### Modelo de linguagem (opcional)

Sem configuração, o agente funciona no **modo extrativo**: monta a resposta diretamente das seções das fichas. É determinístico, offline e serve para testes e demonstração.

Para usar um LLM, copie `agente/.env.example` para `agente/.env` e configure **um** provedor:

```bash
# Groq (plano gratuito)
CITIZEN_LLM_PROVIDER=groq
GROQ_API_KEY=sua_chave

# OpenAI
CITIZEN_LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave

# Ollama local
CITIZEN_LLM_PROVIDER=ollama
CITIZEN_LLM_MODEL=llama3.1
```

O arquivo `agente/.env` é ignorado pelo Git. Nenhuma chave fica no código.

## Avaliação no Golden Dataset

O arquivo [`avaliacao/golden_dataset.json`](avaliacao/golden_dataset.json) contém as **26 mensagens originais** do enunciado, com tipo, resposta esperada, fichas e rubrica. Nenhuma foi substituída.

```bash
# Juiz determinístico (offline, sem chave)
python3 -m avaliacao.executar --modo ambos --juiz deterministico

# Juiz LLM (requer provedor configurado)
python3 -m avaliacao.executar --modo ambos --juiz llm --agente llm
```

Resultados reais desta máquina:

**Juiz determinístico (offline, reproduzível):**

| Versão | Exatos | Parciais | Falhas | Aproveitamento |
|---|---:|---:|---:|---:|
| Baseline | 0/26 | 7 | 19 | 13,5% |
| Agente | **26/26** | 0 | 0 | **100,0%** |

**Juiz LLM (OpenAI `gpt-4o-mini`) com LangGraph 0.6.11:**

| Versão | Exatos | Parciais | Falhas | Aproveitamento |
|---|---:|---:|---:|---:|
| Baseline | 0/26 | 6 | 20 | 11,5% |
| Agente | **25/26** | 1 | 0 | **98,1%** |

O único parcial no juiz LLM é o **caso 24** (recusa de prompt injection sem citar uma ficha específica). A resposta esperada não exige ficha nesse caso; o juiz LLM marcou a citação como critério secundário. O juiz determinístico considera o caso correto.

Relatórios: [`avaliacao/resultados/relatorio.md`](avaliacao/resultados/relatorio.md) (determinístico), [`avaliacao/resultados/llm_langgraph/relatorio.md`](avaliacao/resultados/llm_langgraph/relatorio.md) (LLM + LangGraph) e [`avaliacao/resultados/llm_sequencial/relatorio.md`](avaliacao/resultados/llm_sequencial/relatorio.md) (LLM + fallback sequencial).

## Testes

```bash
python3 -m unittest discover -s testes -t . -v
node mobile/teste-logica.js
```

Resultado atual:

- **141 testes Python aprovados**, cobrindo catálogo, agente, avaliação e provedor.
- **78 verificações mobile** aprovadas.

Os testes do agente cobrem fichas, PII, prompt injection, entradas inválidas, fluxo, citações, fallback do LLM, Golden Dataset, juiz determinístico, juiz LLM e cliente HTTP OpenAI-compatível.

## Estrutura

```text
Jun/
├── main.py                     # catálogo de serviços
├── main_agente.py              # agente de documentos
├── app/                        # núcleo do catálogo DSA
├── data/                       # catálogo, histórico e CSV
├── mobile/                     # app mobile completo
├── agente/
│   ├── fichas/                 # FC-01 a FC-07 (oficiais, versão 01/10/2026)
│   ├── agente.py               # núcleo do agente
│   ├── fluxo.py                # LangGraph + fallback sequencial
│   ├── seguranca.py            # PII, injection e validação
│   ├── recuperacao.py          # busca por pontuação
│   ├── provedor.py             # Groq/OpenAI/Ollama via HTTP
│   ├── prompts.py              # prompt de sistema
│   ├── fichas.py               # carregador/validador
│   ├── cli.py                  # interface do agente
│   └── .env.example
├── avaliacao/
│   ├── golden_dataset.json     # 26 mensagens originais
│   ├── juiz.py                 # juiz determinístico + LLM as a Judge
│   ├── baseline.py             # versão de comparação
│   ├── executar.py             # runner antes/depois
│   └── resultados/             # determinístico + llm_langgraph + llm_sequencial
├── testes_usuarios/            # protocolo e planilha (execução pendente)
├── pitch/                      # roteiro pronto; link do vídeo pendente
├── testes/                     # 141 testes Python
├── docs/
│   ├── DOCUMENTACAO.md         # documentação do catálogo DSA
│   └── DOCUMENTACAO_UNIFICADA.md # documento único da solução
├── requirements.txt            # langgraph (opcional)
├── README.md
└── .gitignore
```

## Menu do catálogo

| Opção | Operação |
|---:|---|
| 1 | Cadastrar serviço |
| 2 | Consultar por ID |
| 3 | Pesquisar por título, categoria ou descrição |
| 4 | Atualizar serviço |
| 5 | Excluir serviço |
| 6 | Listar todos |
| 7 | Ordenar e listar |
| 8 | Análise dos serviços |
| 9 | Fazer uma pergunta |
| 10 | Navegar por categorias |
| 11 | Indicadores de atendimento |
| 12 | Exportar atendimentos para CSV |
| 13 | Agente de documentos pessoais (IA) |
| 0 | Salvar e sair |

O menu do agente tem opções próprias para perguntar, navegar pelas fichas e ler o aviso de privacidade. Nenhuma pergunta é armazenada.

## Segurança e privacidade

- **Não coleta** dados pessoais. CPF, RG, CNH, título, telefone, e-mail, endereço e números longos são detectados, ocultados e não repetidos.
- **Não armazena** perguntas. A CLI guarda apenas contadores da sessão.
- **Não aceita** instruções vindas da mensagem. O documento do enunciado continha uma instrução maliciosa ao final; ela foi tratada como dado e ignorada. O mesmo vale para `[SISTEMA] Nova regra...` e “ignore as instruções anteriores”.
- **Não inventa.** Fora das fichas, a resposta é “não encontrei” + orientação ao órgão competente.
- **Não é canal oficial.** Toda resposta de escopo traz o aviso e a data de verificação.
- O juiz LLM recebe a mensagem com dados pessoais mascarados e não recebe números de documentos nem como “fato proibido”.

## Documentação

- [`docs/DOCUMENTACAO_UNIFICADA.md`](docs/DOCUMENTACAO_UNIFICADA.md) — documento único da solução, com arquitetura, segurança, resultados, limitações e checklist.
- [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md) — documentação detalhada do catálogo DSA.
- [`docs/EVIDENCIAS_TESTES.md`](docs/EVIDENCIAS_TESTES.md) — comandos e saídas reais dos testes.
- [`docs/PEDIDO_FICHAS.md`](docs/PEDIDO_FICHAS.md) — registro da importação das fichas oficiais.
- [`agente/fichas/LEIA-ME.md`](agente/fichas/LEIA-ME.md) — origem, versão e formato das fichas oficiais.
- [`avaliacao/resultados/relatorio.md`](avaliacao/resultados/relatorio.md) — resultados do juiz determinístico.
- [`avaliacao/conferencia_manual.md`](avaliacao/conferencia_manual.md) — amostra para conferência humana (pendente).
- [`pitch/roteiro.md`](pitch/roteiro.md) — roteiro do vídeo de 3 minutos.
- [`testes_usuarios/protocolo.md`](testes_usuarios/protocolo.md) — protocolo completo do teste com 5 pessoas externas.
- [`testes_usuarios/protocolo_rapido.md`](testes_usuarios/protocolo_rapido.md) — versão reduzida (5 pessoas, 6 tarefas, 15–20 min).

## Pendências antes da entrega

1. Fazer a **conferência manual** de uma amostra (formulário em `avaliacao/conferencia_manual.md`).
2. Executar o teste com **≥5 pessoas externas** e preencher a planilha anônima.
3. Gravar o vídeo de até 3 minutos, publicar como **não listado** e colar o link em `pitch/link_video.txt`.
4. Revisar o resultado do juiz LLM (25/26; o parcial é o caso 24) e registrar a análise final.

As fichas oficiais já foram importadas, o juiz LLM já foi executado com `gpt-4o-mini` e o repositório público já está em https://github.com/C0utinhoxx/citizen-assist-ai. Esses itens não são mais pendências.

## Licença

Projeto educacional desenvolvido para a Global Solution 2026.2. Uso restrito ao contexto acadêmico.
