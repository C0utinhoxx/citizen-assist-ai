# Entrega — SERS (Soluções em Energias Renováveis e Sustentáveis)

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (SERS)
**Turma:** 1CCPX
**Instituição:** FIAP

**Integrantes:**

- Bruno Riquelme Coutinho Pereira — RM 569619
- Eduardo Bigoli Portela — RM 569897
- Gustavo Fondato de Souza — RM 573651

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Pitch (até 3 min):** pendente de gravação e publicação como não listado.

---

## 1. Público e necessidade energética

**Público:** pessoas idosas (60 anos ou mais) e famílias de baixa renda, com o mesmo recorte do Citizen Assist AI.

**Necessidade:** reduzir a conta de luz sem perder conforto e segurança. A pessoa idosa passa mais tempo em casa, usa iluminação e ventilação por mais horas e, muitas vezes, tem renda fixa. A conta de luz compete com alimentação e remédios.

**Pergunta que o módulo responde:** vale mais a pena reduzir o consumo ou instalar energia solar?

---

## 2. Cenário, dados e unidades

| Premissa | Valor | Unidade | Período | Origem |
|---|---:|---|---|---|
| Consumo da casa | 150 | kWh/mês | 12 meses | Estimativa abaixo da média residencial da EPE (183,8 kWh/mês) |
| Consumo anual | 1.800 | kWh/ano | 12 meses | 150 × 12 |
| Tarifa residencial | 0,90 | R$/kWh | 2025 | Referência de São Paulo, com tributos |
| Fator de emissão do SIN | 0,040 | kg CO₂/kWh | ano-base 2024 | MCTI |
| Lâmpadas trocadas | 5 | unidades | uso diário | Premissa da equipe |
| Potência antiga | 60 | W | 2 h/dia | Lâmpada incandescente |
| Potência LED | 9 | W | 2 h/dia | Lâmpada LED |
| Standby | 8 | W | 24 h/dia | Aparelhos em espera |
| Produtividade solar | 1.200 | kWh/kWp/ano | 1 ano | Estimativa para São Paulo |
| Custo do sistema | 5.000 | R$/kWp | 2026 | Faixa de mercado |
| Fator de compensação | 0,85 | adimensional | 1 ano | Perdas, autoconsumo e Fio B |
| Vida útil | 25 | anos | 25 anos | Premissa conservadora |

Conta base: **150 kWh × R$ 0,90 = R$ 135,00/mês** e **R$ 1.620,00/ano**.

---

## 3. Alternativa A — eficiência energética

**Ações:** trocar 5 lâmpadas de 60 W por LED de 9 W e cortar 8 W de standby.

Cálculos:

- LED: `5 × (60 − 9) W × 2 h × 30 dias ÷ 1.000 = 15,3 kWh/mês`
- Standby: `8 W × 24 h × 30 dias ÷ 1.000 = 5,76 kWh/mês`
- Total: **21,06 kWh/mês** e **252,72 kWh/ano**
- Economia: **R$ 18,95/mês** e **R$ 227,45/ano**
- Investimento: **R$ 135,00** (5 LEDs a R$ 15,00 + R$ 60,00 para cortar standby)
- Payback: **7,1 meses**
- Consumo final: **128,94 kWh/mês** (redução de 14%)
- CO₂ evitado: **10,11 kg/ano**

**Vantagens:** barato, rápido, funciona em casa alugada e não exige obra.
**Limitações:** não zera a conta e depende do uso real.

---

## 4. Alternativa B — energia solar fotovoltaica

**Dimensionamento:**

- Consumo anual: `150 × 12 = 1.800 kWh/ano`
- Potência: `1.800 ÷ 1.200 = 1,5 kWp`
- Geração estimada: **1.800 kWh/ano**
- Área aproximada: **6 m²**

**Custos e retorno:**

- Investimento: `1,5 × R$ 5.000,00 = R$ 7.500,00`
- Energia compensada: **1.800 kWh/ano**
- Economia: `1.800 × 0,90 × 0,85 = R$ 1.377,00/ano` — **R$ 114,75/mês**
- Payback simples: **5,4 anos** (65,4 meses)
- Economia líquida em 25 anos: **R$ 26.925,00**, sem reajuste tarifário
- CO₂ evitado: **72,0 kg/ano**; cerca de **1,8 t em 25 anos**

**Condições:** imóvel próprio, telhado sem sombra, aprovação da distribuidora, orçamento de empresa habilitada e capital inicial ou financiamento.

---

## 5. Comparação e recomendação

| Indicador | Eficiência (LED + standby) | Solar fotovoltaico |
|---|---:|---:|
| Investimento | R$ 135,00 | R$ 7.500,00 |
| Economia mensal | R$ 18,95 | R$ 114,75 |
| Economia anual | R$ 227,45 | R$ 1.377,00 |
| Payback | 7,1 meses | 5,4 anos |
| Redução de consumo | 14% | 85% de compensação |
| CO₂ evitado/ano | 10,11 kg | 72,0 kg |
| Exige obra ou aprovação | Não | Sim |

**Cenário combinado:** eficiência primeiro e solar depois.

- Investimento: **R$ 6.635,00**
- Economia: **R$ 1.411,12/ano**
- Payback: **4,7 anos**
- CO₂ evitado: **72,0 kg/ano**

**Recomendação:** começar pela eficiência, que é barata e rápida. Avaliar o solar apenas se a casa for própria, o telhado tiver sombra livre e houver condições de investir. Antes de qualquer compra, verificar o direito à **Tarifa Social**.

---

## 6. Tarifa Social

Famílias de baixa renda no CadÚnico, e idosos ou pessoas com deficiência que recebem o BPC, podem ter **100% de desconto no consumo de até 80 kWh/mês**. A parcela acima disso não recebe desconto. O endereço no CadÚnico ou no BPC precisa estar atualizado.

Essa verificação vem antes de LED ou solar: em alguns casos, o desconto da Tarifa Social é maior que qualquer economia calculada.

---

## 7. Integração ao assistente

- Menu principal, opção **14 — Energia e sustentabilidade (SERS)**.
- Execução direta: `python3 -m sers`.
- Três orientações na categoria **Energia** da base:
  - id 16 — reduzir o consumo;
  - id 17 — instalar energia solar;
  - id 18 — pedir a Tarifa Social.
- Cálculos em [`../sers/energia.py`](../sers/energia.py).
- Testes em [`../testes/test_sers_energia.py`](../testes/test_sers_energia.py), com 9 casos.
- Relatório completo: [`../docs/SERS_RELATORIO.md`](../docs/SERS_RELATORIO.md).

---

## 8. Impacto ambiental

- **Eficiência:** evita cerca de **10 kg CO₂/ano** e reduz a demanda por geração.
- **Solar:** evita cerca de **72 kg CO₂/ano** pelo fator médio do SIN.
- **Cenário combinado:** mantém a economia de 72 kg CO₂/ano.
- A conta não inclui a pegada de fabricação, transporte e descarte dos equipamentos; é uma estimativa, não um inventário.

---

## 9. Referências

- EPE — consumo de energia elétrica: https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/consumo-de-energia-eletrica
- ANEEL — geração distribuída: https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida
- ANEEL — Tarifa Social: https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social
- EPE — Atlas de Energia Solar Brasileira: https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/atlas-de-energia-solar-brasileira
- MCTI — fatores de emissão do SIN: https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao
- CustoSolar — preços residenciais 2026: https://custosolar.com/blog/quanto-custa-energia-solar-2026-precos-reais/

---

## 10. Limitações

- Tarifa, impostos, bandeiras e consumo real mudam o resultado.
- A produtividade solar varia por região, inclinação e sombreamento.
- O payback é simples: não inclui juros, inflação, degradação nem reajuste tarifário.
- O cálculo não inclui manutenção, troca de inversor ou financiamento.
- A Tarifa Social depende de CadÚnico/BPC e de regras que mudam.
- O módulo não substitui orçamento de empresa habilitada nem projeto elétrico.

---

## 11. Teste com usuários

**Status:** protocolo pronto; execução pendente.

- Protocolo: [`../testes_usuarios/protocolo_sers.md`](../testes_usuarios/protocolo_sers.md)
- Planilha: [`../testes_usuarios/planilha_sers.csv`](../testes_usuarios/planilha_sers.csv)
- Questionário: [`../testes_usuarios/questionario_sers.csv`](../testes_usuarios/questionario_sers.csv)

Regra: pelo menos **3 pessoas externas**, sem nomes ou dados pessoais. Os resultados só devem ser preenchidos depois da execução real.

---

## 12. Pendências antes de entregar

- [ ] Executar o teste com pelo menos 3 pessoas.
- [ ] Gravar o pitch de até 3 minutos, com narração humana.
- [ ] Publicar como não listado e colar o link em `SERS.txt`.
- [ ] Confirmar que o repositório abre sem login.

---

## 13. Texto para o portal

O arquivo [`SERS.txt`](SERS.txt) contém o texto pronto. Falta apenas o link do vídeo.
