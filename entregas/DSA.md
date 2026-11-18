# Entrega — DSA (Data Structures and Algorithms)

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Data Structures and Algorithms (DSA)
**Turma:** 1CCPX
**Instituição:** FIAP

**Integrantes:**

- Bruno Riquelme Coutinho Pereira — RM 569619
- Eduardo Bigoli Portela — RM 569897
- Gustavo Fondato de Souza — RM 573651

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Vídeo de demonstração:** pendente de gravação e publicação como não listado.

---

## 1. Objetivo

Demonstrar, em um sistema real, o uso de **lista encadeada manual**, CRUD, busca, ordenação própria e análise de complexidade, sem depender de listas prontas do Python para a estrutura principal.

O sistema é o catálogo de serviços públicos do Citizen Assist AI.

---

## 2. Estrutura implementada

```text
No
├── dado: Orientacao
└── proximo: No | None

ListaEncadeada
├── inicio: No | None
├── quantidade: int
├── inserir()
├── buscar_por_id()
├── pesquisar()
├── atualizar()
├── remover()
├── percorrer()
└── ordenar_por()
```

Arquivos:

- [`../app/lista_encadeada.py`](../app/lista_encadeada.py) — `No` e `ListaEncadeada`.
- [`../app/modelos.py`](../app/modelos.py) — `Orientacao` (registro do catálogo).
- [`../app/base_conhecimento.py`](../app/base_conhecimento.py) — carga, categorias e pontuação.
- [`../app/interface.py`](../app/interface.py) — menu e CRUD.
- [`../app/persistencia.py`](../app/persistencia.py) — JSON e CSV.

### Por que lista encadeada

- O requisito pede inserção, percurso e remoção com nós e referências.
- Cada nó guarda um objeto `Orientacao` e um ponteiro para o próximo.
- A lista não usa `list` do Python para armazenar os registros principais.
- A ordenação não usa `sorted()` nem `.sort()` no código de produção.

---

## 3. CRUD e busca

| Operação | Menu | Como funciona |
|---|---:|---|
| Criar | 1 | Valida os campos, recusa ID duplicado e insere no fim |
| Consultar | 2 | Percorre a lista comparando IDs |
| Pesquisar | 3 | Normaliza e compara título, categoria e resposta |
| Atualizar | 4 | Localiza o nó e altera os campos escolhidos |
| Excluir | 5 | Localiza o nó, ajusta os ponteiros e confirma |
| Listar | 6 | Percorre todos os nós |
| Ordenar | 7 | Selection Sort por título, categoria ou ID |
| Analisar | 8 | Conta registros por categoria e calcula percentuais |
| Perguntar | 9 | Busca por pontuação e devolve confiança |
| Categorias | 10 | Navegação por categoria |
| Indicadores | 11 | Atendimentos, acertos, tempo e facilidade |
| CSV | 12 | Exporta o histórico de atendimentos |

### Busca por pontuação

- +3 pontos para cada palavra-chave da orientação que aparece inteira na pergunta.
- +1 ponto para cada palavra da pergunta com 4 letras ou mais que aparece no título.
- ALTA: 6 pontos ou mais.
- MÉDIA: 3 a 5 pontos.
- Sem resultado: menos de 3 pontos.

Exemplo: `Como faço o cartão do SUS?` → 3 + 3 + 1 = **7 pontos, ALTA**.

---

## 4. Selection Sort

O algoritmo está em `ListaEncadeada.ordenar_por()`:

1. Para cada posição da lista, procura o menor elemento no restante.
2. Troca apenas os dados dos nós, sem remover ou inserir nós.
3. Repete até o fim.

Complexidade: **O(n²)** no pior e no melhor caso, com **O(1)** de memória extra.

---

## 5. Análise Big-O

Legenda: `n` = registros; `m` = tamanho dos textos; `r` = resultados; `k` = categorias.

| Operação | Complexidade | Justificativa |
|---|---|---|
| Inserir no fim | `O(n)` | Verifica ID duplicado e percorre até o último nó |
| Buscar por ID | `O(n)` | No pior caso, percorre todos os nós; no melhor, `O(1)` |
| Pesquisar por texto | `O(n * m)` | Normaliza e compara três campos por nó |
| Atualizar | `O(n)` | Localiza o nó; a alteração é `O(1)` |
| Remover | `O(n)` | Localiza o nó; o ajuste de ponteiros é `O(1)` |
| Percorrer/listar | `O(n)` | Visita cada nó uma vez |
| Ordenar (Selection Sort) | `O(n²)` | Para cada nó, percorre o restante |
| Contar por categoria | `O(n)` | Percorre a lista uma vez e usa `O(k)` de memória |
| Ordenar a contagem | `O(k²)` | Insertion Sort auxiliar |
| Busca por pontuação | `O(n * m + r²)` | Pontua todos e ordena os resultados |
| Carregar/salvar JSON | `O(n)` | Converte cada registro uma vez |
| Exportar CSV | `O(n)` | Escreve cada atendimento uma vez |

---

## 6. Persistência

- Catálogo: `data/base_conhecimento.json`.
- Histórico: `data/historico.json`.
- Exportação: `data/atendimentos.csv`.
- JSON ausente ou corrompido não derruba o programa: avisa e usa lista vazia.

---

## 7. Testes e evidências

```bash
python3 -m unittest discover -s testes -t .
node mobile/teste-logica.js
```

Resultado real:

```text
Ran 178 tests

OK
OK — 90 verificações passaram.
```

Testes específicos de DSA:

- `test_lista_encadeada.py` — 14 casos: inserção, percurso, busca, atualização, remoção, ordenação, lista vazia, ponteiros, ID duplicado e contagem por categoria.
- `test_base_conhecimento.py` — 9 casos: carga, categorias, pontuação, ranking, empate e busca sem resultado.
- `test_integracao.py` — 19 casos: validações, CRUD completo e menu unificado.
- `test_persistencia.py` — 8 casos: JSON ausente, corrompido, compatibilidade e CSV.

Evidências: [`../docs/EVIDENCIAS_TESTES.md`](../docs/EVIDENCIAS_TESTES.md).
Análise completa: [`../docs/DOCUMENTACAO.md`](../docs/DOCUMENTACAO.md).

---

## 8. Versão mobile

O app em [`../mobile/index.html`](../mobile/index.html) reimplementa em JavaScript:

- lista encadeada;
- Selection Sort;
- busca e categorias;
- histórico e indicadores;
- CSV e backup JSON;
- voz e acessibilidade.

Testes: **90 verificações aprovadas** com `node mobile/teste-logica.js`.

---

## 9. Decisões e limitações

**Decisões:**

- Lista encadeada manual em vez de `list`, para atender ao requisito.
- Selection Sort próprio em vez de `sorted()`.
- JSON em vez de banco de dados, pelo escopo e pela facilidade de inspeção.
- Busca lexical explicável em vez de embeddings.

**Limitações:**

- A busca é linear; uma base muito maior pediria índice.
- Não há autenticação, usuários ou controle de concorrência.
- A informação é estática e deve ser conferida no órgão oficial.
- O assistente não é canal oficial e não acompanha processos.

---

## 10. Pendências antes de entregar

- [ ] Gravar o vídeo de demonstração.
- [ ] Publicar como não listado e colar o link em `DSA.txt`.
- [ ] Confirmar que o repositório abre sem login.

---

## 11. Texto para o portal

O arquivo [`DSA.txt`](DSA.txt) contém o texto pronto. Falta apenas o link do vídeo.
