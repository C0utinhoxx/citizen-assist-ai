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

As **sete fichas oficiais** foram localizadas em `~/Downloads/referencia` e importadas em **2026-11-11**. A versão oficial é de **01/10/2026** e a fonte é a **Central do Cidadão de Aurora** (material didático fictício do exercício).

Os arquivos desta pasta foram convertidos do formato original (campos em negrito) para o Markdown aceito pelo carregador, **sem resumir nem inventar conteúdo**. O texto de cada campo foi preservado; apenas os campos foram agrupados em seções pesquisáveis e receberam palavras-chave de índice. O aviso original do professor está em [`00_LEIA-ME.md`](00_LEIA-ME.md).

O importador usado está em [`ferramentas/importar_fichas.py`](../../ferramentas/importar_fichas.py). Para reimportar outra versão oficial:

```bash
python3 ferramentas/importar_fichas.py /caminho/para/a/pasta/com/as/FC
```

O carregador aceita o formato Markdown descrito abaixo; não é necessário alterar o código do agente.

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
