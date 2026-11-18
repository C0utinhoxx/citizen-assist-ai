# Protocolo de teste com usuários — SERS (energia)

**Objetivo:** verificar se as orientações de energia são compreensíveis e úteis
para o público do Citizen Assist AI, sem coletar dados pessoais.

**Público:** pessoas externas ao grupo, preferencialmente pessoas idosas e
cuidadores. Pode ser a mesma pessoa que participou do teste do assistente, mas
registre a sessão de energia separadamente.

**Tempo estimado:** 8 a 12 minutos por participante.
**Status:** protocolo pronto; execução pendente.

> Não invente participantes, tempos ou notas. Não registre nome, idade, CPF,
> endereço, telefone, e-mail ou valor da conta de luz com identificação.

---

## 1. Privacidade

- Use apenas códigos anônimos: **S01, S02, S03, S04, S05**.
- Consentimento verbal; registre apenas “concordou: sim/não”.
- Não grave áudio, vídeo ou tela.
- O consumo informado é um número de kWh, não um dado pessoal. Ainda assim, não
  registre o valor individual na planilha; registre apenas se o cálculo rodou.
- Não peça a conta de luz, nome, CPF ou endereço.

---

## 2. Roteiro

### Abertura

> “Vamos testar uma parte do assistente que compara formas de economizar
> energia. Ele não é um canal oficial e não garante economia. Não vamos pedir
> seus dados e não vamos gravar. Você pode parar quando quiser. Podemos
> começar?”

### Tarefa 1 — Entender as alternativas

Abra `python3 main.py` → opção **14** → opção **1**.

Peça: “Me explique, com suas palavras, a diferença entre a alternativa A e a
alternativa B.”

Observe:
- [ ] Citou eficiência/LED como mais barata e rápida.
- [ ] Citou solar como fonte renovável e com investimento maior.
- [ ] Não confundiu as duas.

### Tarefa 2 — Comparar custo e retorno

Ainda na tabela, peça: “Qual das duas se paga mais rápido? Por quê?”

Observe:
- [ ] Apontou a eficiência (payback de poucos meses).
- [ ] Entendeu que o solar tem payback maior, mas economia anual maior.

### Tarefa 3 — Calcular com um consumo

Opção **2**, informe `150` kWh/mês e tarifa `0,90`.

Peça: “O que mudou no resultado?”

Observe:
- [ ] Leu o investimento e a economia.
- [ ] Percebeu que o valor é uma estimativa.

### Tarefa 4 — Reconhecer uma limitação

Abra a opção **3** (fontes e limitações).

Peça: “Cite uma coisa que esse cálculo não garante.”

Observe:
- [ ] Disse que é estimativa, não garantia.
- [ ] Ou citou tarifa, telhado, manutenção ou juros.

### Tarefa 5 — Decidir

Peça: “Se fosse para a sua casa, o que você faria primeiro? Por quê?”

Observe:
- [ ] Escolha coerente com a recomendação (eficiência primeiro).
- [ ] Ou justificou por que não pode investir no solar.

---

## 3. Registro

Use a planilha [`planilha_sers.csv`](planilha_sers.csv):

```text
participante,tarefa,acertou,tempo_segundos,clareza_1_5,observacoes
```

Exemplo **sem dados pessoais**:

```text
S01,1,C,35,5,entendeu a diferenca
S01,4,P,20,4,disse que e estimativa mas nao citou manutencao
```

Critérios de sucesso sugeridos:

- ≥ 4 de 5 participantes entendem a diferença entre as alternativas;
- ≥ 4 de 5 reconhecem que os valores são estimativas;
- ≥ 4 de 5 consideram a recomendação útil;
- tempo médio por tarefa ≤ 90 segundos;
- clareza média ≥ 4,0 (escala 1 a 5).

---

## 4. Perguntas de fechamento (1 a 5)

1. “O que ficou mais claro?”
2. “O que ficou mais difícil?”
3. “A recomendação foi fácil de entender?” — 1 (muito difícil) a 5 (muito fácil)
4. “Você confiaria nessa comparação? Por quê?”
5. “O que mudaria para ajudar você a decidir?”

Registre as respostas em [`questionario_sers.csv`](questionario_sers.csv).

---

## 5. O que não pode

- Inventar participantes ou resultados.
- Usar integrantes do grupo como participantes.
- Coletar nome, CPF, endereço, telefone, e-mail ou foto da conta de luz.
- Prometer economia ou apresentar a estimativa como garantia.
- Deixar o participante achar que o assistente é um canal oficial.
