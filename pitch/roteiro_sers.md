# Roteiro do vídeo SERS — energia e sustentabilidade

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (SERS)
**Duração alvo:** 2min45 · **Limite:** 3 minutos
**Narração:** humana, por um integrante do grupo. **Sem voz de IA.**
**Publicação:** YouTube como **não listado**
**Entrega:** colar o link em [`entrega_sers.txt`](../entrega_sers.txt)

**Equipe:** Bruno Riquelme Coutinho Pereira (RM 569619) · Eduardo Bigoli Portela (RM 569897) · Gustavo Fondato de Souza (RM 573651)

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Relatório completo:** [`docs/SERS_RELATORIO.md`](../docs/SERS_RELATORIO.md)

> O vídeo deve mostrar a análise de energia **dentro** do assistente, não só slides.
> Grave a tela do terminal legível e deixe a tabela da opção 14 parada por 2 segundos.

---

## Antes de gravar

```bash
cd /Users/brunocoutinho/Documents/GlobalSoluctions/Jun
python3 -m unittest discover -s testes -t .    # esperado: 178 testes, OK
python3 -m sers                                 # relatório completo
python3 main.py                                 # opção 14
```

- [ ] Terminal com fonte 18–22 pt e saída limpa.
- [ ] `python3 main.py` abre com 18 serviços e 5 categorias.
- [ ] A opção 14 mostra as alternativas A e B, a combinação, as fontes e o aviso.
- [ ] Nenhuma chave, CPF, nome ou endereço na tela.
- [ ] Celular/câmera pronta, se for aparecer.

---

## Cena 1 — Público e necessidade (0:00–0:20)

**Na tela:** cartela com o nome do projeto, a disciplina e os três integrantes.

```text
Citizen Assist AI — SERS
Energia e sustentabilidade para pessoas idosas e cuidadores
Global Solution 2026.2
```

**Fala:**

> "Nosso público são pessoas idosas e cuidadores. Muitas passam mais tempo em casa e têm renda fixa. A conta de luz pesa no orçamento. Nossa contribuição é ajudá-las a comparar duas alternativas: eficiência e energia solar."

---

## Cena 2 — Dados e premissas (0:20–0:45)

**Na tela:** tabela das premissas (consumo, tarifa, período, fonte).

```text
Consumo: 150 kWh/mês (1.800 kWh/ano)
Tarifa: R$ 0,90/kWh
Período: 12 meses
Fontes: EPE 2025 · ANEEL 2025 · MCTI 2024
```

**Fala:**

> "Partimos de 150 kWh por mês, abaixo da média nacional de 183,8 kWh do Anuário da EPE. A tarifa é de noventa centavos por kWh, referência de São Paulo. São estimativas declaradas: a conta real muda com bandeiras e impostos."

---

## Cena 3 — Alternativa A: eficiência (0:45–1:15)

**Na tela:** cálculo no terminal.

```text
(60 − 9) W × 5 lâmpadas × 2 h/dia = 15,3 kWh/mês
Standby de 8 W = 5,8 kWh/mês
Total: 21,1 kWh/mês → R$ 18,95/mês
Investimento: R$ 135,00 → payback: 7,1 meses
CO2 evitado: 10,1 kg/ano
```

**Fala:**

> "A primeira alternativa é eficiência: trocar cinco lâmpadas de sessenta watts por LED de nove e cortar oito watts de standby. Economiza vinte e um kWh por mês, cerca de dezenove reais. Custa cento e trinta e cinco reais e se paga em sete meses. É barata e funciona até em casa alugada."

---

## Cena 4 — Alternativa B: solar (1:15–1:50)

**Na tela:** cálculo no terminal.

```text
1.800 kWh/ano ÷ 1.200 kWh/kWp = 1,5 kWp
Geração: 1.800 kWh/ano
Investimento: R$ 7.500,00
Economia: R$ 1.377,00/ano
Payback: 5,4 anos
CO2 evitado: 72 kg/ano
```

**Fala:**

> "A segunda alternativa é o solar, uma fonte renovável. Para esse consumo, um sistema de um e meio kWp gera cerca de mil e oitocentos kWh por ano. Custa sete mil e quinhentos reais, economiza mil trezentos e setenta e sete por ano e se paga em cinco anos e meio. Exige telhado próprio, sem sombra, e aprovação da distribuidora."

---

## Cena 5 — Comparação e recomendação (1:50–2:20)

**Na tela:** `python3 main.py` → opção `14` → opção `1`. Deixe a tabela visível.

**Fala:**

> "Aqui está a integração: a opção quatorze do assistente mostra as duas alternativas na mesma base. A eficiência ganha em custo e velocidade; o solar ganha em volume e em impacto ambiental. A recomendação é começar pela eficiência e depois avaliar o solar. Juntas, o investimento cai para seis mil seiscentos e trinta e cinco reais e o payback fica em quatro anos e sete meses."

**Ação:** digite `14`, depois `1`, deixe a tabela na tela por 2 segundos.

---

## Cena 6 — Limitações e fontes (2:20–2:45)

**Na tela:** opção `3` do menu de energia, com as fontes e o aviso.

**Fala:**

> "Temos limitações claras. Os valores são estimativas, não garantia de economia. O payback não inclui juros, manutenção nem troca de inversor. Antes de investir, a família deve verificar a Tarifa Social: em 2026, a regra prevê desconto total até oitenta kWh por mês para quem se enquadra. As fontes são EPE, ANEEL e MCTI, e o assistente não é um canal oficial."

---

## Cena 7 — Encerramento (2:45–3:00)

**Na tela:** cartela final com o repositório.

```text
Citizen Assist AI — SERS
github.com/C0utinhoxx/citizen-assist-ai
```

**Fala:**

> "Energia mais barata começa por decisão informada. O Citizen Assist AI leva essa conta para o cidadão, com fonte, premissa e limite. Obrigado."

---

## Plano de corte (se passar de 3 minutos)

| # | O que cortar | Ganha |
|---:|---|---:|
| 1 | Cena 2, a frase sobre bandeiras e impostos | ~4 s |
| 2 | Cena 3, "É barata e funciona até em casa alugada." | ~4 s |
| 3 | Cena 4, "uma fonte renovável" | ~2 s |
| 4 | Cena 5, a frase do cenário combinado | ~6 s |
| 5 | Cena 6, a explicação da Tarifa Social | ~7 s |

**Nunca corte:** a tabela da opção 14, o valor de R$ 38,00 não aparece aqui, e o aviso de que os valores são estimativas.

---

## Checklist depois de gravar

- [ ] Duração entre 2min30 e 3min00.
- [ ] Narração humana, sem voz sintética.
- [ ] A tela mostra a opção 14 e a tabela das alternativas.
- [ ] A fala cita a fonte renovável (solar).
- [ ] A fala cita pelo menos uma limitação.
- [ ] Nenhum dado pessoal, chave ou nome de participante aparece.
- [ ] Vídeo publicado como **não listado**.
- [ ] Link colado em [`entrega_sers.txt`](../entrega_sers.txt).
- [ ] Link testado em janela anônima.
