# Evidências de testes

**Data da execução:** 2026-11-11
**Ambiente:** macOS, Python 3.9.6, Node.js v26.7.0
**LangGraph:** 0.6.11 (ambiente de teste separado)
**Provedor LLM real:** OpenAI `gpt-4o-mini` (chave somente em `agente/.env`, ignorado pelo Git)
**Fichas:** oficiais, versão 01/10/2026, importadas de `~/Downloads/referencia`

> Todos os números abaixo foram produzidos nesta máquina. Nenhum resultado foi estimado ou inventado. A chave do provedor não aparece neste documento nem no repositório.

## 1. Suíte Python — sem LangGraph

```bash
cd Jun
python3 -m unittest discover -s testes -t .
```

Saída:

```text
Ran 141 tests in 1.373s

OK
```

## 2. Suíte Python — com LangGraph

```bash
/tmp/venv_lg/bin/python -m unittest discover -s testes -t .
```

Saída (resumo):

```text
Ran 141 tests in 1.476s

OK
```

O teste `test_fluxo_usa_langgraph_quando_disponivel` confirma que o fluxo usa `langgraph` quando a biblioteca está instalada e `sequencial` quando não está.

## 3. Mobile

```bash
node mobile/teste-logica.js
```

Saída:

```text
OK — 78 verificações passaram.
```

## 4. Golden Dataset — juiz determinístico

```bash
python3 -m avaliacao.executar --modo ambos --juiz deterministico --agente extrativo
```

Saída:

```text
baseline: 0/26 exatos, 7 parciais, 19 falhas, média 0.135 (13.5%).
melhorado: 26/26 exatos, 0 parciais, 0 falhas, média 1.0 (100.0%).
Resultados salvos em .../avaliacao/resultados
```

Metadados do relatório:

```text
- Dataset: 1.0 (26 mensagens originais)
- Juiz: deterministico
- Fluxo do agente: {'baseline': 'sequencial (baseline)', 'melhorado': 'sequencial'}
```

Arquivos:

- `avaliacao/resultados/relatorio.md`
- `avaliacao/resultados/resultados.json`

## 5. Golden Dataset — juiz LLM com LangGraph

```bash
/tmp/venv_lg/bin/python -m avaliacao.executar \
  --modo ambos --juiz llm --agente llm \
  --saida avaliacao/resultados/llm_langgraph
```

Saída:

```text
baseline: 0/26 exatos, 6 parciais, 20 falhas, média 0.115 (11.5%).
melhorado: 25/26 exatos, 1 parciais, 0 falhas, média 0.981 (98.1%).
Resultados salvos em .../avaliacao/resultados/llm_langgraph
```

Metadados do relatório:

```text
- Dataset: 1.0 (26 mensagens originais)
- Juiz: llm
- Provedor: openai (configurado)
- Fluxo do agente: {'baseline': 'sequencial (baseline)', 'melhorado': 'langgraph'}
```

O único parcial é o **caso 24** (recusa de prompt injection sem citar uma ficha específica). A resposta esperada não exige ficha nesse caso; o juiz LLM tratou a citação como critério secundário. O juiz determinístico considera o caso correto.

Arquivos:

- `avaliacao/resultados/llm_langgraph/relatorio.md`
- `avaliacao/resultados/llm_langgraph/resultados.json`

## 6. Golden Dataset — juiz LLM com fallback sequencial

```bash
python3 -m avaliacao.executar \
  --modo ambos --juiz llm --agente llm \
  --saida avaliacao/resultados/llm_sequencial
```

Saída:

```text
baseline: 0/26 exatos, 6 parciais, 20 falhas, média 0.115 (11.5%).
melhorado: 25/26 exatos, 1 parciais, 0 falhas, média 0.981 (98.1%).
```

Arquivos:

- `avaliacao/resultados/llm_sequencial/relatorio.md`
- `avaliacao/resultados/llm_sequencial/resultados.json`

## 7. Teste do cliente HTTP OpenAI-compatível

```bash
python3 -m unittest testes.test_provedor_http -v
```

O teste sobe um servidor HTTP local, envia uma requisição no formato OpenAI, confere modelo, mensagens, cabeçalho `Authorization`, resposta e erro HTTP 500. Não usa internet nem chave real.

## 8. Testes do juiz LLM

Além da execução real, o juiz LLM é coberto por:

- provedor falso devolvendo JSON válido;
- JSON dentro de cerca Markdown;
- JSON inválido (erro controlado);
- verificação de que o CPF do caso 22 não aparece no payload enviado ao provedor;
- envio das fichas de referência com fonte e data de verificação.

## 9. O que ainda não foi executado

| Item | Motivo |
|---|---|
| Teste com 5 pessoas externas | Depende de recrutamento e execução presencial/remota pelo grupo. |
| Conferência manual humana | Formulário regenerado com as fichas oficiais; falta preencher. |
| Vídeo de 3 minutos | Depende de gravação e publicação pelo grupo. |
| Link público do GitHub | Depende de autenticação/publicação pelo grupo. |

## 10. Como reproduzir

```bash
cd Jun
python3 -m unittest discover -s testes -t . -v
node mobile/teste-logica.js
python3 -m avaliacao.executar --modo ambos --juiz deterministico --agente extrativo
python3 main_agente.py
```

Para o modo LLM:

```bash
cp agente/.env.example agente/.env
# edite agente/.env com a chave do provedor; não versione esse arquivo
python3 -m avaliacao.executar --modo ambos --juiz llm --agente llm \
  --saida avaliacao/resultados/llm_sequencial
```

Com LangGraph instalado, o mesmo comando usa o fluxo `langgraph` automaticamente.
