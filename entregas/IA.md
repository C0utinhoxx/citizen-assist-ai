# Entrega — IA (Prompt and Artificial Intelligence)

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Prompt and Artificial Intelligence
**Turma:** 1CCPX
**Instituição:** FIAP

**Integrantes:**

- Bruno Riquelme Coutinho Pereira — RM 569619
- Eduardo Bigoli Portela — RM 569897
- Gustavo Fondato de Souza — RM 573651

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Vídeo:** pendente de gravação e publicação como não listado.

---

## 1. Objetivo do agente

O agente responde dúvidas sobre documentos pessoais usando **exclusivamente** as fichas FC-01 a FC-07 fornecidas no enunciado. Ele cita a ficha de origem e a data de verificação, admite desconhecimento quando a ficha não responde e não é um canal oficial.

**Escopo:** RG/CIN, CPF, título de eleitor, carteira de trabalho, certidões, CNH e benefícios citados nas fichas.

**Fora do escopo:** preços, prazos ou documentos que não estejam nas fichas; consulta a sistemas do governo; agendamento; acompanhamento de processos.

---

## 2. Framework e arquitetura

- **Framework:** LangGraph, com fallback sequencial quando a biblioteca não está instalada.
- **Provedores compatíveis com OpenAI:** Groq, OpenAI e Ollama local.
- **Modelo usado na avaliação:** OpenAI `gpt-4o-mini`.
- **Fluxo:** segurança → recuperação nas fichas → contexto citado → resposta extrativa ou LLM → citação e aviso.

Diagrama: [`../docs/arquitetura_agente.svg`](../docs/arquitetura_agente.svg).

Nós do grafo:

1. `analisar` — validação, PII, injection e intenção.
2. `bloquear` — resposta segura sem repetir dados.
3. `recuperar` — busca lexical e seleção de seções.
4. `sem_resultado` — admissão de desconhecimento.
5. `responder` — redação extrativa ou por LLM.

O fallback sequencial executa os mesmos passos na mesma ordem e devolve as mesmas respostas no modo extrativo.

---

## 3. Onde entra a IA e onde bastam algoritmos

| Etapa | Tecnologia | Por quê |
|---|---|---|
| Validação de entrada | Regras | Precisa ser previsível e offline |
| Detecção de PII | Regex | Não pode depender de LLM para proteger dados |
| Prompt injection | Regras | Precisa bloquear antes de qualquer chamada |
| Busca nas fichas | Pontuação lexical | Explicável e reproduzível |
| Seleção de contexto | Regras | Evita misturar fichas |
| Redação | LLM opcional | Melhora a fluidez, mas não decide fatos |
| Citação e aviso | Código | Garante que a fonte sempre apareça |

**Decisão:** o LLM não decide preço, prazo, documento ou elegibilidade. Ele apenas redige com base no contexto recuperado. No modo extrativo, o sistema funciona sem nenhuma chave ou chamada de rede.

---

## 4. Segurança e privacidade

- CPF, RG, CNH, título, telefone, e-mail, endereço e números longos são detectados, ocultados e não repetidos.
- Perguntas com PII são recusadas e **não entram no histórico**.
- Instruções como “ignore as instruções anteriores”, `[SISTEMA]` e “modo desenvolvedor” são tratadas como dado, não como comando.
- Nenhuma pergunta é gravada em arquivo, banco ou histórico.
- O juiz LLM recebe a mensagem com PII mascarada.
- Nenhuma chave de API fica no código; o `.env` é ignorado pelo Git.

---

## 5. Golden Dataset e avaliação

O Golden Dataset tem **26 mensagens originais**, mantidas sem substituição. A avaliação compara uma linha de base ingênua com o agente melhorado.

### Juiz determinístico

```bash
python3 -m avaliacao.executar --modo ambos --juiz deterministico --agente extrativo
```

Resultado real:

```text
baseline: 0/26 exatos, 7 parciais, 19 falhas, média 0.135 (13.5%).
melhorado: 26/26 exatos, 0 parciais, 0 falhas, média 1.0 (100.0%).
```

### LLM as a Judge

- Modelo: OpenAI `gpt-4o-mini`.
- Fluxo: LangGraph 0.6.11.
- Resultado: **24/26 exatos, 1 parcial e 1 falha — 94,2%**.
- Caso parcial: 24. Caso com falha: 25.
- O fallback sequencial recebeu a mesma nota nos 26 casos.

Arquivos:

- [`../avaliacao/golden_dataset.json`](../avaliacao/golden_dataset.json)
- [`../avaliacao/juiz.py`](../avaliacao/juiz.py)
- [`../avaliacao/executar.py`](../avaliacao/executar.py)
- [`../avaliacao/resultados/`](../avaliacao/resultados/)
- [`../docs/DOCUMENTACAO_UNIFICADA.md`](../docs/DOCUMENTACAO_UNIFICADA.md)

---

## 6. Testes automatizados

```bash
python3 -m unittest discover -s testes -t .
```

Resultado real: **178 testes aprovados**, incluindo:

- carga e validação das fichas FC-01 a FC-07;
- fluxo LangGraph e fallback sequencial;
- PII, injection, entrada vazia, curta e longa;
- citação de ficha e data;
- fallback quando o LLM falha ou vaza prompt;
- Golden Dataset, juiz determinístico e juiz LLM;
- cliente HTTP compatível com OpenAI.

A suíte passa com e sem LangGraph instalado.

---

## 7. Justificativa do modelo e do framework

- **LangGraph:** permite explicitar nós e arestas, com estado e caminhos condicionais, em vez de esconder a lógica em um prompt gigante.
- **`gpt-4o-mini`:** custo baixo, boa qualidade em português e disponibilidade para a avaliação.
- **Provedores alternativos:** Groq e Ollama permitem testar sem depender de um único fornecedor.
- **Modo extrativo:** garante que a demonstração funcione offline e que o resultado não dependa de uma chave paga.

---

## 8. Resultados e limitações

**Resultados:**

- 26/26 no juiz determinístico no modo extrativo.
- 24/26 no juiz LLM com LangGraph.
- 178 testes Python e 90 verificações mobile aprovados.

**Limitações:**

- As fichas são fictícias e não valem para órgãos reais.
- O juiz LLM usa um único modelo; outra execução pode variar.
- A busca é lexical e pode falhar com sinônimos não previstos.
- A detecção de PII é por regex e pode deixar passar formatos incomuns.
- A conferência manual e o teste com pessoas ainda não foram executados.

---

## 9. Pendências antes de entregar

- [ ] Preencher a conferência manual de 9 casos em [`../avaliacao/conferencia_manual.md`](../avaliacao/conferencia_manual.md).
- [ ] Executar o teste com 5 pessoas externas e preencher as planilhas.
- [ ] Registrar a análise final dos casos 24 e 25 do juiz LLM.
- [ ] Gravar o vídeo e colar o link em `IA.txt`.
- [ ] Confirmar que o repositório abre sem login.

---

## 10. Texto para o portal

O arquivo [`IA.txt`](IA.txt) contém o texto pronto. Falta apenas o link do vídeo, se exigido.
