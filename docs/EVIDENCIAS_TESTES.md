# Evidências de testes

**Data da execução:** 2026-11-10  
**Ambiente:** macOS, Python 3.9.6, Node.js v26.7.0  
**LangGraph:** 0.6.11 (ambiente de teste separado)  
**Provedor LLM real:** não configurado (sem chave)

> Todos os números abaixo foram produzidos nesta máquina. Nenhum resultado foi estimado ou inventado.

## 1. Suíte Python — sem LangGraph

```bash
cd Jun
python3 -m unittest discover -s testes -t .
```

Saída:

```text
...........................................................................................................................................
----------------------------------------------------------------------
Ran 141 tests in 1.235s

OK
```

## 2. Suíte Python — com LangGraph

```bash
/tmp/venv_lg/bin/python -m unittest discover -s testes -t .
```

Saída (resumo):

```text
Ran 141 tests in 1.305s

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
/tmp/venv_lg/bin/python -m avaliacao.executar --modo ambos --juiz deterministico
```

Saída:

```text
baseline: 0/26 exatos, 6 parciais, 20 falhas, média 0.115 (11.5%).
melhorado: 26/26 exatos, 0 parciais, 0 falhas, média 1.0 (100.0%).
Resultados salvos em .../avaliacao/resultados
```

Metadados do relatório:

```text
- Dataset: 1.0 (26 mensagens originais)
- Juiz: deterministico
- Fluxo do agente: {'baseline': 'sequencial (baseline)', 'melhorado': 'langgraph'}
```

Arquivos:

- `avaliacao/resultados/relatorio.md`
- `avaliacao/resultados/resultados.json`

## 5. Teste do cliente HTTP OpenAI-compatível

```bash
python3 -m unittest testes.test_provedor_http -v
```

O teste sobe um servidor HTTP local, envia uma requisição no formato OpenAI, confere modelo, mensagens, cabeçalho `Authorization`, resposta e erro HTTP 500. Não usa internet nem chave real.

## 6. Juiz LLM

Testado com:

- provedor falso devolvendo JSON válido;
- JSON dentro de cerca Markdown;
- JSON inválido (erro controlado);
- verificação de que o CPF do caso 22 não aparece no payload enviado ao provedor.

**Execução com modelo real:** pendente de configuração de `GROQ_API_KEY`, `OPENAI_API_KEY` ou Ollama.

## 7. O que ainda não foi executado

| Item | Motivo |
|---|---|
| Juiz LLM com modelo real | Sem chave/modelo configurado. |
| Teste com 5 pessoas externas | Depende de recrutamento e execução presencial/remota pelo grupo. |
| Conferência manual humana | Formulário pronto; falta preencher. |
| Vídeo de 3 minutos | Depende de gravação e publicação pelo grupo. |
| Substituição das fichas oficiais | Arquivos FC-01 a FC-07 oficiais não estavam disponíveis. |

## 8. Como reproduzir

```bash
cd Jun
python3 -m unittest discover -s testes -t . -v
node mobile/teste-logica.js
python3 -m avaliacao.executar --modo ambos --juiz deterministico
python3 main_agente.py
```

Para o modo LLM:

```bash
cp agente/.env.example agente/.env
# edite agente/.env com a chave do provedor
python3 -m avaliacao.executar --modo ambos --juiz llm --agente llm
```
