# Entregas por disciplina — Global Solution 2026.2

**Projeto:** Citizen Assist AI · **Turma:** 1CCPX
**Integrantes:** Bruno Riquelme Coutinho Pereira (RM 569619), Eduardo Bigoli Portela (RM 569897), Gustavo Fondato de Souza (RM 573651)
**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Prazo:** 19/11/2026, 23h59

Este arquivo é o índice de conferência. Ele diz **o que cada disciplina pede**, **onde está a evidência** e **o que ainda depende de execução humana**. Nada aqui declara concluído o que não foi executado.

---

## Visão geral

| Disciplina | Entrega principal | Código / documento | Status | Falta |
|---|---|---|---|---|
| **PCP — Pensamento Computacional e Programação** | Catálogo em Python com 3 classes, JSON, busca pontuada, histórico/CSV e teste com usuários | `main.py`, `app/`, `data/base_conhecimento.json` | Pronto para entregar | Teste com pessoas e vídeo técnico |
| **IA — Prompt and Artificial Intelligence** | Agente com framework, fichas, segurança, Golden Dataset 26 e LLM as a Judge | `agente/`, `avaliacao/` | Pronto para entregar | Teste com pessoas e conferência manual |
| **SERS — Soluções em Energias Renováveis e Sustentáveis** | Análise de energia com duas alternativas, cálculos, custos, payback, impacto e integração | `sers/`, `docs/SERS_RELATORIO.md` | Pronto para entregar | Teste com pessoas e pitch |
| **DSA — Data Structures and Algorithms** | Lista encadeada manual, CRUD, busca, Selection Sort, Big-O e testes | `app/lista_encadeada.py`, `docs/DOCUMENTACAO.md` | Pronto para entregar | Vídeo (o mesmo do PCP) |

---

## PCP — Pensamento Computacional e Programação

### Requisitos e onde estão

| Requisito | Evidência |
|---|---|
| 3 classes: `Orientacao`, `BaseConhecimento`, `Assistente` | `app/modelos.py`, `app/base_conhecimento.py`, `app/assistente.py` |
| Base em JSON com campos do enunciado | `data/base_conhecimento.json` (18 orientações, 5 categorias) |
| Busca com pontuação e confiança ALTA/MÉDIA | `normalizar()`, `pontuar()`, `buscar()`; 7 pontos no exemplo do Cartão SUS |
| Categorias e navegação | menu opção 10; `BaseConhecimento.categorias()` |
| Entrada inválida e lista vazia | `ler_inteiro()`, `ler_texto()`, `confirmar()`; testes de integração |
| Bloqueio de PII (CPF, RG, CNH, telefone, e-mail, endereço) | `Assistente._tem_dado_pessoal()` |
| Histórico, indicadores e CSV | `data/historico.json`, `data/atendimentos.csv`, menus 11 e 12 |
| Integração com o agente de IA | menu opção 13 |
| Integração com SERS | menu opção 14 |
| Teste com usuários | protocolos em `testes_usuarios/`; **execução pendente** |
| Vídeo técnico de 5–8 min | roteiro em `pitch/roteiro.md`; **gravação pendente** |

### Documentos para ler antes de entregar

- [`README.md`](README.md) — visão geral, execução e limitações.
- [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md) — decisões de implementação, Big-O e roteiro de demonstração.
- [`testes_usuarios/protocolo_rapido.md`](testes_usuarios/protocolo_rapido.md) — protocolo de 5 pessoas / 6 tarefas.
- [`testes_usuarios/relatorio.md`](testes_usuarios/relatorio.md) — modelo de relatório (preencher após executar).
- [`entrega_portal.txt`](entrega_portal.txt) — texto de entrega (falta o link do vídeo).

### Checklist PCP

- [x] Código, JSON e classes alinhados ao enunciado
- [x] Busca pontuada documentada e testada
- [x] PII, entrada inválida e lista vazia tratadas
- [x] Histórico, indicadores e CSV funcionando
- [x] 178 testes Python e 90 verificações mobile aprovados
- [ ] Teste com ≥3 pessoas e ≥10 atendimentos, com planilha anônima
- [ ] Uma melhoria concreta registrada após o teste
- [ ] Vídeo técnico de 5–8 min, não listado, com todos falando
- [ ] Link do vídeo em `entrega_portal.txt`

---

## IA — Prompt and Artificial Intelligence

### Requisitos e onde estão

| Requisito | Evidência |
|---|---|
| Framework de agentes | `agente/fluxo.py` com LangGraph e fallback sequencial |
| Arquitetura explícita | `docs/arquitetura_agente.svg` e seção 9 da documentação única |
| Justificativa do modelo | `docs/DOCUMENTACAO_UNIFICADA.md` (seções 8–9) e `agente/provedor.py` |
| Uso de IA vs. lógica determinística | seção “Onde entra a IA e onde bastam algoritmos” |
| Fichas FC-01 a FC-07 | `agente/fichas/` (versão 01/10/2026) |
| Golden Dataset com 26 mensagens | `avaliacao/golden_dataset.json` |
| LLM as a Judge antes/depois | `avaliacao/juiz.py`, `avaliacao/executar.py`, `avaliacao/resultados/` |
| Segurança: PII e prompt injection | `agente/seguranca.py` e testes |
| Resultados reais | determinístico 0/26 → 26/26; LLM 24/26 (94,2%) |
| Teste com 5 pessoas | protocolo em `testes_usuarios/`; **execução pendente** |
| Conferência manual da amostra | `avaliacao/conferencia_manual.md`; **execução pendente** |

### Documentos para ler antes de entregar

- [`docs/DOCUMENTACAO_UNIFICADA.md`](docs/DOCUMENTACAO_UNIFICADA.md) — documento único (seções 8 a 12).
- [`avaliacao/resultados/relatorio.md`](avaliacao/resultados/relatorio.md) — juiz determinístico.
- [`avaliacao/resultados/llm_langgraph/relatorio.md`](avaliacao/resultados/llm_langgraph/relatorio.md) — juiz LLM.
- [`avaliacao/conferencia_manual.md`](avaliacao/conferencia_manual.md) — formulário de conferência.
- [`pitch/descricao_youtube.md`](pitch/descricao_youtube.md) — descrição e comentário do vídeo.

### Checklist IA

- [x] LangGraph com fallback e testes nos dois modos
- [x] Fichas oficiais importadas e citadas com data
- [x] Golden Dataset com as 26 mensagens originais
- [x] Comparação antes/depois com juiz determinístico
- [x] LLM as a Judge executado com `gpt-4o-mini`
- [x] PII, injection e entradas inválidas cobertas por testes
- [ ] Conferência manual de 9 casos assinada
- [ ] Teste com 5 pessoas e relatório preenchido
- [ ] Análise final dos casos 24 (parcial) e 25 (falha) do juiz LLM

---

## SERS — Soluções em Energias Renováveis e Sustentáveis

### Requisitos e onde estão

| Requisito | Evidência |
|---|---|
| Público e necessidade energética | `docs/SERS_RELATORIO.md`, seção 1 |
| Consumo, unidades, período e fontes | seção 2, com 150 kWh/mês, 1.800 kWh/ano e R$ 0,90/kWh |
| Alternativa 1 — eficiência (LED + standby) | seção 3; `sers/energia.py` |
| Alternativa 2 — solar fotovoltaico (renovável) | seção 4; `sers/energia.py` |
| Cálculos e memória de cálculo | seções 3–5 e testes `testes/test_sers_energia.py` |
| Custos, payback e viabilidade | seções 3–6 |
| Impacto ambiental (CO₂ evitado) | seções 3–5 |
| Integração ao assistente | opção 14 do menu e orientações 16–18 na categoria Energia |
| Referências e limitações | seções 8–9 do relatório |
| Teste com usuários | `testes_usuarios/protocolo_sers.md`; **execução pendente** |
| Pitch de até 3 min | `pitch/roteiro_sers.md`; **gravação pendente** |

### Números do cenário padrão

| Indicador | Eficiência | Solar |
|---|---:|---:|
| Investimento | R$ 135,00 | R$ 7.500,00 |
| Economia mensal | R$ 18,95 | R$ 114,75 |
| Economia anual | R$ 227,45 | R$ 1.377,00 |
| Payback | 7,1 meses | 5,4 anos |
| CO₂ evitado/ano | 10,11 kg | 72 kg |
| Redução de consumo | 14% | 85% de compensação |

### Documentos para ler antes de entregar

- [`docs/SERS_RELATORIO.md`](docs/SERS_RELATORIO.md) — relatório completo.
- [`pitch/roteiro_sers.md`](pitch/roteiro_sers.md) — roteiro do pitch.
- [`testes_usuarios/protocolo_sers.md`](testes_usuarios/protocolo_sers.md) — protocolo de teste.
- [`entrega_sers.txt`](entrega_sers.txt) — texto de entrega (falta o link do vídeo).

### Checklist SERS

- [x] Duas alternativas, incluindo fonte renovável
- [x] Premissas, unidades, período e fontes declarados
- [x] Cálculos, custos, payback e CO₂ cobertos por 9 testes
- [x] Integração real ao menu e à base de conhecimento
- [x] Limitações e recomendações explícitas
- [ ] Teste com ≥3 pessoas, com planilha e questionário
- [ ] Pitch de até 3 min, narração humana e não listado
- [ ] Link do vídeo em `entrega_sers.txt`

---

## DSA — Data Structures and Algorithms

### Requisitos e onde estão

| Requisito | Evidência |
|---|---|
| Lista encadeada manual | `app/lista_encadeada.py` (`No`, `ListaEncadeada`) |
| Inserção, percurso, busca, atualização e remoção | métodos da lista e menu 1–5 |
| Busca implementada | busca por ID e busca textual |
| Ordenação própria | Selection Sort em `ordenar_por()` |
| Análise Big-O | `docs/DOCUMENTACAO.md`, seção 13 |
| CRUD completo | menus 1 a 6 |
| Testes e evidências | `testes/test_lista_encadeada.py` e `docs/EVIDENCIAS_TESTES.md` |
| Mobile | `mobile/index.html` e `mobile/teste-logica.js` |

### Checklist DSA

- [x] Nenhum `sorted()`/`.sort()` no código de produção da estrutura
- [x] Inserção, remoção e atualização preservam os ponteiros
- [x] Selection Sort próprio e análise Big-O
- [x] Testes de lista vazia, inexistente, inválida e ordenação
- [x] 178 testes Python e 90 verificações mobile aprovados
- [ ] Vídeo de demonstração (o mesmo vídeo técnico do PCP)

---

## Roteiro de verificação final

```bash
cd /Users/brunocoutinho/Documents/GlobalSoluctions/Jun

python3 -m unittest discover -s testes -t .    # 178 testes
node mobile/teste-logica.js                    # 90 verificações
python3 -m avaliacao.executar --modo ambos --juiz deterministico --agente extrativo
python3 -m sers                                # cálculos SERS
python3 main.py                                # opções 9, 10, 11, 13, 14 e 0
python3 main_agente.py                         # agente de fichas
```

## Pendências que dependem de pessoas

Estas pendências **não podem ser simuladas** e estão marcadas como tal em todos os documentos:

1. Teste com usuários do PCP (≥3 pessoas / ≥10 atendimentos).
2. Teste com usuários da IA (5 pessoas / 6 tarefas).
3. Teste com usuários do SERS (≥3 pessoas).
4. Conferência manual da amostra do juiz.
5. Vídeo técnico do PCP (5–8 min).
6. Pitch SERS (até 3 min).
7. Colar os links dos vídeos em `entrega_portal.txt`, `entrega_sers.txt` e `pitch/link_video.txt`.

Enquanto esses itens não forem executados, os arquivos de protocolo e os modelos de relatório permanecem prontos, mas **vazios de resultados reais**.
