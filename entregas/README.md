# Entregáveis por disciplina

Cada matéria tem seu próprio documento e seu próprio texto de portal. Todos apontam para o mesmo repositório, mas descrevem apenas o que aquela disciplina exige.

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Turma:** 1CCPX
**Equipe:** Bruno Riquelme Coutinho Pereira (RM 569619), Eduardo Bigoli Portela (RM 569897), Gustavo Fondato de Souza (RM 573651)
**Prazo:** 19/11/2026, 23h59

| Disciplina | Documento completo | Texto para o portal | Status |
|---|---|---|---|
| PCP — Pensamento Computacional e Programação | [`PCP.md`](PCP.md) | [`PCP.txt`](PCP.txt) | Pronto; faltam teste com pessoas e vídeo |
| IA — Prompt and Artificial Intelligence | [`IA.md`](IA.md) | [`IA.txt`](IA.txt) | Pronto; faltam teste com pessoas e conferência manual |
| SERS — Soluções em Energias Renováveis e Sustentáveis | [`SERS.md`](SERS.md) | [`SERS.txt`](SERS.txt) | Pronto; faltam teste com pessoas e pitch |
| DSA — Data Structures and Algorithms | [`DSA.md`](DSA.md) | [`DSA.txt`](DSA.txt) | Pronto; falta o vídeo de demonstração |

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
