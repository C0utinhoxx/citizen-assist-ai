# Fichas oficiais FC-01 a FC-07 — registro

**Status:** resolvido em **2026-11-11**.

As sete fichas oficiais foram localizadas na pasta `referencia` em `~/Downloads` e importadas para `agente/fichas/`.

- **Versão oficial:** 01/10/2026.
- **Fonte:** Central do Cidadão de Aurora (material didático fictício do exercício).
- **Arquivos importados:** `FC-01_rg_segunda_via.md` a `FC-07_regras_gerais.md`.
- **Aviso original:** copiado para `agente/fichas/00_LEIA-ME.md`.
- **Importador:** `ferramentas/importar_fichas.py`.

O conteúdo foi convertido para o formato Markdown do carregador sem resumir nem inventar fatos. A avaliação foi reexecutada com as fichas oficiais.

## Histórico

Antes da localização, este documento continha uma mensagem pronta para pedir as fichas ao professor. Ela não é mais necessária. O texto antigo partia de fichas provisórias, que já foram substituídas.

## Como reimportar

```bash
python3 ferramentas/importar_fichas.py /caminho/para/a/pasta/com/as/FC
```

O script espera os sete arquivos `FC-*.md` e o `00_LEIA-ME.md` na pasta de origem. Ele preserva o texto dos campos e agrupa o conteúdo em seções pesquisáveis.
