# Relatório do teste com usuários — Citizen Assist AI

**Status:** CONCLUÍDO

**Equipe:** Bruno Riquelme Coutinho Pereira (RM 569619), Eduardo Bigoli Portela (RM 569897) e Gustavo Fondato de Souza (RM 573651)
**Data da aplicação:** 19/11/2026
**Versão testada:** commit `bb2e707`
**Interface usada:** terminal (`python3 main_agente.py`)

---

## 1. Participantes

Os participantes foram recrutados externamente e responderam individualmente. Nenhum dado pessoal (nome, idade, profissão ou documento) foi registrado, preservando integralmente o sigilo e a privacidade dos voluntários.

| Código | Consentimento | Tarefas concluídas | Observações |
|---|---|---|---|
| P01 | Sim (verbal) | 10 / 10 | Precisou de ajuda em 3 tarefas |
| P02 | Sim (verbal) | 10 / 10 | Precisou de ajuda em 3 tarefas |
| P03 | Sim (verbal) | 10 / 10 | Precisou de ajuda em 3 tarefas |
| P04 | Sim (verbal) | 10 / 10 | Precisou de ajuda em 3 tarefas |
| P05 | Sim (verbal) | 10 / 10 | Precisou de ajuda em 3 tarefas |

- Participantes externos: **5**
- Tarefas por participante: **10**
- Total de tarefas aplicadas: **50**
- Nenhum dado pessoal registrado: sim

---

## 2. Resultados consolidados por bloco de tarefa

| # | Descrição do tipo de serviço | C | P | I | Tempo médio (s) | Facilidade média (1–5) |
|---:|---|:---:|:---:|:---:|---:|---:|
| 1 | Emissão de documentos civis e identificação (RG, Passaporte, SUS) | 3 | 2 | 0 | 41,2 | 4,6 |
| 2 | Acesso a serviços de saúde (Conecte SUS, Farmácia Popular, UBS) | 3 | 2 | 0 | 47,0 | 4,4 |
| 3 | Trabalho e previdência básica (CTPS Digital, CNH Social, CRLV) | 4 | 1 | 0 | 44,2 | 4,2 |
| 4 | Certidões, gratuidades e contestações (Bolsa Família, multas) | 1 | 0 | 4 | 94,0 | 2,4 |
| 5 | Atualização cadastral e programas sociais (CadÚnico, PIS, NIS) | 4 | 0 | 1 | 45,4 | 4,2 |
| 6 | Regularização fiscal e educacional (CPF, ENEM, Pronatec) | 3 | 2 | 0 | 53,4 | 4,0 |
| 7 | Segurança pública, transporte e trânsito (BO, seguro-desemprego) | 2 | 3 | 0 | 56,4 | 4,0 |
| 8 | Documentação eleitoral e registros em cartório (e-Título, casamento) | 3 | 0 | 2 | 59,0 | 3,6 |
| 9 | Requerimentos previdenciários e assistência jurídica (BPC, IPTU) | 3 | 0 | 2 | 72,6 | 3,0 |
| 10 | Certidões e antecedentes (Polícia Federal, agendamento 135) | 4 | 0 | 1 | 50,4 | 4,4 |

**Totais consolidados**

| Métrica | Valor |
|---|---|
| Tarefas aplicadas | 50 / 50 |
| Acertos exatos (C) | 30 (60,0 %) |
| Acertos parciais (P) | 10 (20,0 %) |
| Respostas incorretas (I) | 10 (20,0 %) |
| Taxa de resolução útil (C + P) | 80,0 % |
| Tempo médio geral por tarefa | 56,4 s |
| Tempo médio por participante | P01: 56,5 s; P02: 58,0 s; P03: 56,8 s; P04: 54,6 s; P05: 55,9 s |
| Facilidade média geral (1–5) | 3,88 |
| Tarefas que demandaram apoio | 15 / 50 |

---

## 3. Questionário de facilidade de uso

| Código | Q1 — mais fácil | Q2 — mais difícil | Q3 — clareza (1–5) | Q4 — confiaria | Q5 — o que mudaria |
|---|---|---|:---:|:---:|---|
| P01 | A parte do novo RG digital e da carteira de trabalho | Achar o PDF do cartão do SUS e o BPC | 4 | Sim, passou bastante segurança nas explicações do Gov.br | Deixar mais claro onde clica pra baixar os arquivos |
| P02 | Consultar as vacinas no Conecte SUS e o PIS | Entender a diferença do Caixa Tem pro Bolsa Família | 4 | Confiaria, mas confirmaria valores de taxas no site oficial | Colocar o valor das taxas junto com o passo a passo |
| P03 | Segunda via do RG e marcar consulta na UBS | A parte da perícia médica e transferência do título | 4 | Sim, as respostas batem com o que pedem nos postos | Explicar melhor como funciona a perícia do INSS |
| P04 | Remédios da Farmácia Popular e o CRLV do carro | Como recorrer de multa de trânsito | 4 | Confiaria, bem direto ao ponto na maioria das dúvidas | Adicionar lista com os documentos obrigatórios em tópicos |
| P05 | Atualizar o cadastro do SUS e certidão do TST | Recuperar a senha antiga do Gov.br | 3 | Confiaria na maior parte, tirando a recuperação de conta | Encurtar as respostas muito longas pra ler mais rápido |

**Média da Q3 (clareza das respostas):** 3,8 (de 1 a 5)  
**Participantes que declararam confiança:** 4 / 5

---

## 4. Critérios de sucesso

| Critério | Meta | Resultado | Atendeu? |
|---|---|---|---|
| Taxa de resolução útil (C + P) | ≥ 75% | 80,0 % | sim |
| Tempo médio por tarefa | ≤ 60 s | 56,4 s | sim |
| Facilidade média | ≥ 3,5 | 3,88 | sim |
| Nenhum dado pessoal registrado | 0 ocorrências | 0 | sim |

---

## 5. Conclusão do teste

**O que funcionou bem:**

```text
Respostas diretas e precisas para documentos básicos e rotineiros (novo RG/CIN, Carteira
de Trabalho Digital, agendamento de consultas na UBS, vacinas no Conecte SUS e antecedentes
criminais da Polícia Federal). Preservação de dados pessoais durante todas as interações
e tempo médio de 56,4 s, dentro do teto estipulado de 60 s.
```

**O que precisa melhorar:**

```text
Orientações sobre benefícios assistenciais e previdenciários (BPC/LOAS, pensão e aposentadoria)
demandam passos mais detalhados. Também é importante deixar explícito quando um serviço depende
de agendamento prévio ou taxas, além de disponibilizar links diretos para download de arquivos.
```

**As respostas do agente estavam corretas para os participantes?**
( ) sim (x) parcialmente ( ) não — 80% das dúvidas foram respondidas de forma útil (60% exatas e 20% parciais), com pontos de atenção identificados em serviços mais burocráticos.

---

## 6. Checklist de fechamento

- [x] 5 participantes externos recrutados.
- [x] Consentimento verbal registrado para cada participante.
- [x] 10 tarefas aplicadas por participante.
- [x] `planilha.csv` preenchido.
- [x] `questionario.csv` preenchido.
- [x] Médias calculadas e conferidas.
- [x] Comentários revisados para remover dados pessoais.
- [x] Seção 2 deste relatório preenchida.
- [x] Seção 3 deste relatório preenchida.
- [x] Link para este relatório adicionado ao `README.md` e à `docs/DOCUMENTACAO_UNIFICADA.md`.
- [x] Repositório atualizado no GitHub.
