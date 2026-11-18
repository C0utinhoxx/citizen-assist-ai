# Entregáveis — Global Solution 2026.2

**Projeto:** Citizen Assist AI · **Turma:** 1CCPX
**Integrantes:** Bruno Riquelme Coutinho Pereira (RM 569619), Eduardo Bigoli Portela (RM 569897), Gustavo Fondato de Souza (RM 573651)
**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Prazo:** 19/11/2026, 23h59

Cada disciplina tem seu próprio documento e seu próprio texto de portal. Não existe um único entregável: existem quatro.

| Disciplina | Documento completo | Texto de portal | Status |
|---|---|---|---|
| **PCP** — Pensamento Computacional e Programação | [`entregas/PCP.md`](entregas/PCP.md) | [`entregas/PCP.txt`](entregas/PCP.txt) | Pronto; faltam teste com pessoas e vídeo |
| **IA** — Prompt and Artificial Intelligence | [`entregas/IA.md`](entregas/IA.md) | [`entregas/IA.txt`](entregas/IA.txt) | Pronto; faltam teste com pessoas e conferência manual |
| **SERS** — Soluções em Energias Renováveis e Sustentáveis | [`entregas/SERS.md`](entregas/SERS.md) | [`entregas/SERS.txt`](entregas/SERS.txt) | Pronto; faltam teste com pessoas e pitch |
| **DSA** — Data Structures and Algorithms | [`entregas/DSA.md`](entregas/DSA.md) | [`entregas/DSA.txt`](entregas/DSA.txt) | Pronto; falta o vídeo de demonstração |

Guia rápido: [`entregas/README.md`](entregas/README.md).

---

## O que cada documento contém

### PCP

- Problema, público e proposta.
- As três classes `Orientacao`, `BaseConhecimento` e `Assistente`.
- Base JSON com 18 orientações e 5 categorias.
- Busca pontuada, confiança, categorias, PII, histórico, indicadores e CSV.
- Menu completo, testes, decisões, limitações e roteiro do vídeo.

### IA

- Framework LangGraph e fallback sequencial.
- Arquitetura, modelo `gpt-4o-mini` e justificativa.
- Onde entra a IA e onde a lógica é determinística.
- Fichas FC-01 a FC-07, Golden Dataset de 26 mensagens.
- Antes/depois: 0/26 → 26/26 no juiz determinístico.
- LLM as a Judge: 24/26 (94,2%).
- Segurança, testes e pendências.

### SERS

- Público e necessidade energética.
- Premissas, unidades, período e fontes.
- Alternativa A: eficiência (LED + standby).
- Alternativa B: solar fotovoltaico.
- Cálculos, custos, payback, cenário combinado e CO₂ evitado.
- Tarifa Social, integração ao menu, referências e limitações.

### DSA

- Lista encadeada manual com `No` e `ListaEncadeada`.
- CRUD, busca por ID e por texto.
- Selection Sort próprio.
- Análise Big-O de cada operação.
- Testes, versão mobile, decisões e limitações.

---

## Verificação comum

```bash
python3 -m unittest discover -s testes -t .    # 178 testes
node mobile/teste-logica.js                    # 90 verificações
python3 -m avaliacao.executar --modo ambos --juiz deterministico --agente extrativo
python3 -m sers
```

## Pendências que dependem de pessoas

1. Teste com usuários do PCP: pelo menos 3 pessoas e 10 atendimentos.
2. Teste com usuários da IA: 5 pessoas e 6 tarefas.
3. Teste com usuários do SERS: pelo menos 3 pessoas.
4. Conferência manual da amostra do juiz.
5. Vídeo técnico do PCP, de 5 a 8 minutos.
6. Pitch SERS, de até 3 minutos.
7. Inserir os links dos vídeos nos arquivos `.txt` correspondentes.

Nenhum resultado de teste com pessoas ou de vídeo foi inventado. Os protocolos e modelos estão prontos em `testes_usuarios/`.
