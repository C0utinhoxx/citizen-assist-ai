# SERS — Energia e Sustentabilidade no Citizen Assist AI

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (SERS)
**Instituição:** FIAP · **Turma:** 1CCPX

**Integrantes:**

- Bruno Riquelme Coutinho Pereira — RM 569619
- Eduardo Bigoli Portela — RM 569897
- Gustavo Fondato de Souza — RM 573651

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Vídeo SERS (até 3 min):** _pendente de gravação e publicação como não listado_

---

## 1. Público e necessidade energética

**Público:** pessoas idosas (60 anos ou mais) e familiares ou cuidadores que ajudam essas pessoas a acessar serviços públicos. É o mesmo público do Citizen Assist AI, o que permite integrar a orientação energética ao atendimento que já existe.

**Necessidade:** reduzir o valor da conta de luz sem perder conforto e segurança, em uma casa de baixa renda. A pessoa idosa costuma passar mais tempo em casa, usa iluminação e ventilação por mais horas e, muitas vezes, tem renda fixa. A conta de luz compete com alimentação e remédios.

**Como a orientação ajuda:** o assistente explica, em linguagem simples, duas alternativas — eficiência energética e geração solar — com custo, economia estimada, tempo de retorno, condições e limites. A pessoa consegue comparar antes de gastar e é orientada a confirmar tudo com a distribuidora e com um profissional.

> **Aviso:** esta é uma contribuição educacional. Os valores são estimativas, não garantia de economia. O assistente não é um canal oficial.

---

## 2. Dados, unidades, período e premissas

O cenário de referência é uma casa com **consumo de 150 kWh/mês**, medido ao longo de **12 meses** (1.800 kWh/ano), e tarifa de **R$ 0,90/kWh**. O consumo de 150 kWh/mês é uma **estimativa conservadora**: fica abaixo da média residencial nacional de 183,8 kWh/mês do Anuário EPE 2025, porque o público de baixa renda tende a consumir menos.

| Dado | Valor adotado | Unidade | Período | Origem | Tipo |
|---|---:|---|---|---|---|
| Consumo da casa | 150 | kWh/mês | 12 meses | Estimativa da equipe, abaixo da média EPE 2025 (183,8 kWh/mês) | Estimado |
| Consumo anual | 1.800 | kWh/ano | 12 meses | 150 × 12 | Calculado |
| Tarifa residencial | 0,90 | R$/kWh | jul/2025 | Tarifa B1 Enel SP de R$ 725,18/MWh + ICMS de 18% ≈ R$ 0,86/kWh; arredondada para 0,90 | Estimado |
| Fator de emissão do SIN | 0,040 | kg CO2/kWh | ano-base 2024 | MCTI — fatores de emissão do SIN (≈ 40 kg CO2/MWh) | Real |
| Lâmpadas trocadas | 5 | unidades | uso diário | Premissa da equipe | Estimado |
| Potência da lâmpada antiga | 60 | W | 2 h/dia | Lâmpada incandescente comum | Estimado |
| Potência da lâmpada LED | 9 | W | 2 h/dia | Lâmpada LED equivalente | Estimado |
| Custo de cada LED | 15,00 | R$ | compra única | Faixa de mercado | Estimado |
| Standby cortado | 8 | W | 24 h/dia | TV, receptor, carregadores e micro-ondas em espera | Estimado |
| Filtro de linha com interruptor | 60,00 | R$ | compra única | Faixa de mercado | Estimado |
| Produtividade solar em SP | 1.200 | kWh/kWp/ano | 1 ano | Irradiação de 4,46 kWh/m²/dia e desempenho de 74% | Estimado |
| Custo do sistema solar | 5.000 | R$/kWp | 2026 | Faixa de mercado de R$ 4.800 a R$ 5.500/kWp | Estimado |
| Fator de compensação | 0,85 | adimensional | 1 ano | Perdas, autoconsumo e cobrança da Fio B | Estimado |
| Vida útil do sistema | 25 | anos | 25 anos | Garantia típica dos módulos | Estimado |

**Premissas explícitas:**

1. A casa é própria e o telhado tem área livre de sombra para o solar.
2. A tarifa não muda durante o ano; bandeiras tarifárias e reajustes não entram no cálculo.
3. O sistema solar é dimensionado para compensar o consumo anual; não há venda de excedente.
4. O payback não inclui juros, financiamento, manutenção, limpeza nem troca do inversor.
5. O CO2 evitado usa o fator médio do SIN; a fabricação e o descarte dos equipamentos não entram na conta.

---

## 3. Fórmulas usadas

**Consumo anual**

```text
consumo_anual = consumo_mensal × 12
```

**Eficiência (LED + standby)**

```text
economia_led_dia  = (P_antiga − P_led) × n_lâmpadas × horas_dia ÷ 1000
economia_led_mês  = economia_led_dia × 30
economia_standby  = P_standby × 24 ÷ 1000 × 30
economia_kwh_mês  = economia_led_mês + economia_standby
economia_rs_mês   = economia_kwh_mês × tarifa
payback_meses     = investimento ÷ economia_rs_mês
```

**Solar fotovoltaico**

```text
potência_kwp      = consumo_anual ÷ produtividade_kWh_kWp_ano
geração_anual     = potência_kwp × produtividade
energia_compensada = mínimo(geração_anual, consumo_anual)
economia_rs_ano   = energia_compensada × tarifa × fator_compensação
payback_anos      = investimento ÷ economia_rs_ano
```

**Emissões evitadas**

```text
CO2_evitado_kg = energia_evitada_kWh × 0,040 kg/kWh
```

O código que aplica essas fórmulas está em [`sers/energia.py`](../sers/energia.py) e pode ser executado com `python3 -m sers`.

---

## 4. Alternativas comparadas

### Alternativa A — Eficiência energética (LED + corte de standby)

- 5 lâmpadas de 60 W trocadas por LED de 9 W, usadas 2 h/dia:
  `(60 − 9) × 5 × 2 ÷ 1000 = 0,51 kWh/dia = 15,3 kWh/mês`.
- Corte de 8 W de standby:
  `8 × 24 ÷ 1000 = 0,192 kWh/dia = 5,76 kWh/mês`.
- Total: **21,06 kWh/mês** e **252,7 kWh/ano**.
- Economia: **R$ 18,95/mês** e **R$ 227,45/ano** (tarifa de R$ 0,90/kWh).
- Investimento: 5 × R$ 15,00 + R$ 60,00 = **R$ 135,00**.
- Payback: **7,1 meses** (0,6 ano).
- CO2 evitado: **10,1 kg/ano**.

**Viabilidade:** alta. É barato, não precisa de obra, funciona em casa alugada e pode ser feito aos poucos. A limitação é que a economia é pequena em relação ao total da conta.

### Alternativa B — Geração solar fotovoltaica (fonte renovável)

- Consumo anual: 1.800 kWh.
- Potência necessária: `1.800 ÷ 1.200 = 1,5 kWp`.
- Geração estimada: **1.800 kWh/ano**.
- Investimento: `1,5 × R$ 5.000 = R$ 7.500,00`.
- Economia: `1.800 × 0,90 × 0,85 = R$ 1.377,00/ano`.
- Payback: **5,4 anos**.
- CO2 evitado: **72,0 kg/ano**.
- Economia líquida em 25 anos: **R$ 26.925,00** (sem contar juros, manutenção e troca de inversor).
- Área aproximada: **6 m²**.

**Viabilidade:** média. Exige casa própria, telhado em boas condições e sem sombra, aprovação da distribuidora e capital inicial ou financiamento. Para uma família de baixa renda, o investimento inicial é a maior barreira.

### Alternativa C — Combinação (recomendada)

Fazer primeiro a eficiência reduz o consumo para **128,94 kWh/mês**. O sistema solar cai para **1,3 kWp**, com investimento de **R$ 6.500,00**. O investimento total fica em **R$ 6.635,00**, a economia em **R$ 1.411,12/ano** e o payback em **4,7 anos**. É a melhor combinação: gasta menos para gerar e gera menos porque a casa desperdiça menos.

### Direito que deve ser conferido antes de investir

A **Tarifa Social de Energia Elétrica** pode dar desconto maior que qualquer economia calculada. Pela regra da ANEEL vigente em 2026, famílias de baixa renda no CadÚnico, e idosos ou pessoas com deficiência que recebem o BPC, têm **100% de desconto no consumo de até 80 kWh/mês**; a parcela acima disso não recebe desconto. O endereço no CadÚnico ou no BPC precisa estar atualizado. Antes de comprar LED ou solar, a família deve verificar esse direito na distribuidora.

---

## 5. Comparação na mesma base

Base comum: **150 kWh/mês · 1.800 kWh/ano · 12 meses · tarifa de R$ 0,90/kWh**.

| Indicador | Eficiência (LED + standby) | Solar fotovoltaico | Combinação |
|---|---:|---:|---:|
| Investimento | R$ 135,00 | R$ 7.500,00 | R$ 6.635,00 |
| Economia por mês | R$ 18,95 | R$ 114,75 | R$ 117,59 |
| Economia por ano | R$ 227,45 | R$ 1.377,00 | R$ 1.411,12 |
| Payback | 0,6 ano (7,1 meses) | 5,4 anos | 4,7 anos |
| CO2 evitado por ano | 10,1 kg | 72,0 kg | 72,0 kg |
| Precisa de obra? | Não | Sim | Sim (só para o solar) |
| Funciona em casa alugada? | Sim | Não | Não |
| Barreira principal | Economia limitada | Custo inicial | Custo inicial |

**Leitura:** a eficiência ganha em custo e velocidade; o solar ganha em volume de economia e em impacto ambiental. A combinação tem o melhor payback entre as opções com solar.

---

## 6. Impactos ambientais

- **Eficiência:** evita cerca de **10 kg CO2/ano** e reduz a demanda por geração. Também diminui o lixo doméstico quando as lâmpadas antigas são descartadas em ponto de coleta.
- **Solar:** evita cerca de **72 kg CO2/ano** pelo fator médio do SIN. Em 25 anos, isso representa cerca de **1,8 t CO2** — sem contar a pegada de fabricação, transporte e descarte dos módulos e do inversor.
- **Limite da conta:** o fator do SIN é uma média; a emissão real varia com o despacho das usinas e com a região. A conta não substitui um inventário de emissões.

---

## 7. Integração funcional ao Citizen Assist AI

A contribuição SERS não é um anexo: ela está dentro do assistente.

1. **Menu principal — opção 14:** `python3 main.py` → `14` abre o módulo "Energia e sustentabilidade (SERS)".
2. **Cenário padrão:** a opção 1 mostra as duas alternativas, o cenário combinado, a recomendação, as fontes e o aviso.
3. **Cálculo personalizado:** a opção 2 pede apenas o consumo em kWh/mês e a tarifa. Não pede nome, CPF, endereço ou número da unidade consumidora.
4. **Fontes e limitações:** a opção 3 mostra as premissas, os links e as condições.
5. **Busca em texto livre:** a base `data/base_conhecimento.json` ganhou três orientações na categoria **Energia**:
   - id 16 — reduzir o consumo com LED e standby;
   - id 17 — instalar energia solar fotovoltaica;
   - id 18 — pedir a Tarifa Social.
   Assim, perguntas como "como economizar energia?" ou "quanto custa placa solar?" também são respondidas pela busca por pontuação, com fonte e data de verificação.

**Comandos de demonstração:**

```bash
python3 main.py          # opção 14
python3 -m sers          # relatório completo no terminal
```

**Arquivos:**

| Arquivo | Papel |
|---|---|
| `sers/energia.py` | premissas, cálculos, fontes e relatório |
| `sers/cli.py` | menu da opção 14 e cálculo personalizado |
| `sers/__main__.py` | execução do relatório com `python3 -m sers` |
| `data/base_conhecimento.json` | ids 16 a 18, categoria Energia |
| `testes/test_sers_energia.py` | 9 testes dos cálculos e da integração |

---

## 8. Recomendações ao cidadão

1. **Confira a Tarifa Social primeiro.** Se a família se enquadra, o desconto pode ser maior que a economia de LED e solar juntos.
2. **Comece pela eficiência.** LED e corte de standby custam pouco, pagam rápido e não dependem de obra.
3. **Só depois avalie o solar.** Se a casa for própria, o telhado tiver sombra livre e houver condições de investir ou financiar.
4. **Peça três orçamentos.** Compare potência, garantia, inversor, homologação e suporte.
5. **Não trate a estimativa como promessa.** Tarifa, impostos, bandeiras e consumo real mudam o resultado.
6. **Confirme com a distribuidora e com um profissional habilitado.** O assistente não é canal oficial.

---

## 9. Limitações e condições

- Os valores são **estimativas educacionais**, não garantia de economia.
- A tarifa de R$ 0,90/kWh é uma referência de São Paulo; cada cidade e distribuidora tem valor próprio.
- O consumo de 150 kWh/mês é uma premissa; o cálculo personalizado da opção 14 permite usar o valor real.
- O payback não inclui juros, inflação, manutenção, limpeza, troca de inversor ou degradação dos módulos.
- O solar exige casa própria, telhado adequado, sombra livre e homologação na distribuidora.
- A conta de CO2 usa o fator médio do SIN e não é um inventário.
- O módulo não agenda visita, não faz orçamento e não consulta a conta de luz.
- O assistente não é um canal oficial.

---

## 10. Testes com usuários (SERS)

O protocolo está em [`testes_usuarios/protocolo_sers.md`](../testes_usuarios/protocolo_sers.md). A aplicação com pessoas ainda **não ocorreu**; nenhum resultado foi inventado.

Tarefas previstas:

1. Descobrir quanto custa e quanto tempo leva para trocar lâmpadas por LED.
2. Descobrir se o solar vale a pena para 150 kWh/mês.
3. Dizer qual alternativa a pessoa escolheria e por quê.
4. Explicar, com as próprias palavras, uma limitação do cálculo.

Registro previsto (sem nome, CPF ou endereço): código anônimo, tempo, acertos, nota de clareza de 1 a 5 e comentários.

| Indicador | Meta | Resultado |
|---|---|---|
| Entendeu a diferença entre as alternativas | ≥ 4 de 5 | pendente |
| Identificou que os valores são estimativas | ≥ 4 de 5 | pendente |
| Achou a recomendação útil | ≥ 4 de 5 | pendente |
| Tempo médio para comparar | ≤ 90 s | pendente |
| Clareza (1 a 5) | ≥ 4,0 | pendente |

---

## 11. Referências

| Tema | Fonte | Link | Consulta |
|---|---|---|---|
| Consumo residencial médio | EPE — Anuário Estatístico de Energia Elétrica 2025 | https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-160/topico-168/anuario-factsheet.pdf | 18/11/2026 |
| Tarifa B1 Enel SP | MME — Informativo Tarifário do Setor Elétrico 2025 | https://www.gov.br/mme/pt-br/assuntos/secretarias/secretaria-nacional-energia-eletrica/informativo-tarifario-do-setor-eletrico/informativo-tarifario-do-setor-eletrico-ano-2025.pdf | 18/11/2026 |
| Irradiação solar | EPE — Atlas de Energia Solar Brasileira | https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/atlas-de-energia-solar-brasileira | 18/11/2026 |
| Custo do solar | CustoSolar — preços residenciais 2026 | https://custosolar.com/blog/quanto-custa-energia-solar-2026-precos-reais/ | 18/11/2026 |
| Fator de emissão | MCTI — fatores de emissão do SIN, ano-base 2024 | https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao | 18/11/2026 |
| Tarifa Social | ANEEL — Tarifa Social de Energia Elétrica | https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social | 18/11/2026 |
| Geração distribuída | ANEEL — Geração Distribuída | https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida | 18/11/2026 |

---

## 12. Checklist SERS

| Requisito | Onde está | Status |
|---|---|---|
| Público e necessidade energética | seção 1 | Atendido |
| Dados com origem, unidade, período e premissas | seção 2 | Atendido |
| Duas alternativas, incluindo renovável | seções 4 e 5 | Atendido |
| Cálculos e comparação na mesma base | seções 3 e 5 | Atendido |
| Custos, viabilidade e impactos ambientais | seções 4 a 6 | Atendido |
| Integração funcional ao assistente | seção 7 | Atendido |
| Recomendações coerentes com a análise | seção 8 | Atendido |
| Referências e limitações | seções 9 e 11 | Atendido |
| Testes com usuários | seção 10 | **Pendente de execução** |
| Vídeo de até 3 minutos | [`pitch/roteiro_sers.md`](../pitch/roteiro_sers.md) | **Pendente de gravação** |
| Repositório e arquivo `.txt` | [`entregas/SERS.txt`](../entregas/SERS.txt) | Link do vídeo pendente |
