# Fichas de referência do agente

Esta pasta deve conter as **sete fichas oficiais** fornecidas pelos professores:

| Ficha | Arquivo esperado | Assunto |
|---|---|---|
| FC-01 | `FC-01_rg_segunda_via.md` | RG, primeira e segunda via |
| FC-02 | `FC-02_cpf.md` | CPF: inscrição e atendimento |
| FC-03 | `FC-03_titulo_de_eleitor.md` | Título de eleitor |
| FC-04 | `FC-04_carteira_de_trabalho.md` | Carteira de Trabalho |
| FC-05 | `FC-05_certidoes.md` | Certidões de nascimento, casamento e óbito |
| FC-06 | `FC-06_cnh_renovacao.md` | CNH: renovação |
| FC-07 | `FC-07_regras_gerais.md` | Atendimento, agendamento, terceiros, pagamento e acessibilidade |

## Situação atual

Os sete arquivos desta pasta são **provisórios**. Eles foram montados **somente com os fatos que aparecem nas 26 mensagens do Golden Dataset oficial e com os assuntos das fichas indicados no enunciado**, porque os arquivos originais das fichas não estavam disponíveis no computador no momento da implementação.

Nenhum valor, prazo, documento ou regra foi inventado. Onde o Golden Dataset não traz um fato, a ficha simplesmente não tem a seção. O agente responde “não encontrei nas fichas” nesses casos.

Cada arquivo tem um aviso `STATUS: PROVISÓRIA` e uma data de verificação provisória. **Antes da entrega, substitua os sete arquivos pelas fichas oficiais.** O carregador aceita o mesmo formato Markdown descrito abaixo; não é necessário alterar código.

## Formato aceito

```markdown
# FC-01 — Título da ficha

- **Fonte:** Ficha FC-01 — Central do Cidadão de Aurora
- **Data de verificação:** 2026-01-01
- **Palavras-chave:** rg, identidade, segunda via

## Nome da seção | palavra-chave 1, palavra-chave 2
Texto da seção.
```

Regras:

1. A primeira linha deve começar com `# FC-XX —`.
2. `Fonte` e `Data de verificação` são obrigatórios.
3. Cada seção começa com `##`.
4. O trecho após `|` é opcional e serve apenas para a busca.
5. Não escreva dados pessoais reais nas fichas.

Se uma ficha oficial tiver outro formato (por exemplo, PDF ou texto corrido), converta para este Markdown mantendo o conteúdo literal. Não resuma nem complete informações.
