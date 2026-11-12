# Citizen Assist AI — Documentação do Catálogo DSA (Projetos 1 e 2)

> **Nota:** este documento detalha o catálogo DSA dos Projetos 1 e 2. A documentação única dos Projetos 1 a 4, com o agente de IA, a avaliação e o checklist de entrega, está em [`DOCUMENTACAO_UNIFICADA.md`](DOCUMENTACAO_UNIFICADA.md).

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Data Structures and Algorithms (DSA)
**Linguagem:** Python 3.8+
**Projeto:** unificação da Lição 1 (proposta e atendimento) com a Lição 2 (lista encadeada e algoritmos)

---

## 1. Visão geral

O **Citizen Assist AI** é um sistema de terminal que organiza serviços e orientações ao cidadão. O projeto reúne, em uma única solução:

- o catálogo de serviços com CRUD completo;
- a lista encadeada implementada pela equipe;
- a busca por identificador e a pesquisa por atributo;
- o algoritmo **Selection Sort** implementado pela equipe;
- a análise dos dados cadastrados;
- o atendimento por pergunta livre com pontuação e confiança;
- a navegação por categorias;
- o histórico de atendimentos, os indicadores e a exportação CSV;
- a validação de entradas, a proteção de dados pessoais e a persistência em JSON.

A proposta da Lição 1 foi preservada e passou a usar a mesma lista encadeada da Lição 2. Assim, não existem duas bases independentes: existe **um único catálogo**, uma única lista e um único menu.

> As versões originais foram mantidas em `../python` (Lição 1) e `../dts` (Lição 2), sem alterações. Este projeto é a versão unificada.

---

## 2. Integrantes

> Preencher com os dados reais da equipe antes da entrega.

| Nome | RM |
|---|---|
| Integrante 1 | RM000000 |
| Integrante 2 | RM000000 |
| Integrante 3 | RM000000 |

**Repositório GitHub:** (preencher)
**Vídeo de demonstração:** (preencher)

---

## 3. Proposta da Lição 1 — problema e público

### 3.1. Público

Pessoas idosas (60 anos ou mais) e familiares ou cuidadores que ajudam essas pessoas a acessar serviços públicos.

### 3.2. Problema

As informações sobre serviços públicos existem, mas estão espalhadas em vários sites, usam linguagem técnica e se misturam com páginas que não são oficiais. Isso faz a pessoa perder tempo, ir ao lugar errado ou levar documentos incompletos.

### 3.3. Solução proposta

O Citizen Assist AI responde dúvidas em linguagem simples usando uma base de conhecimento previamente verificada. Cada resposta apresenta:

- título e categoria;
- descrição da orientação;
- documentos e requisitos;
- local de atendimento;
- fonte oficial;
- data de verificação;
- aviso de que o assistente **não** é um canal oficial.

O sistema não inventa respostas, não consulta a internet em tempo real e não substitui os canais oficiais do governo.

### 3.4. ODS relacionados

- **ODS 3 — Saúde e Bem-Estar:** Cartão SUS, vacinação e consultas na UBS.
- **ODS 10 — Redução das Desigualdades:** acesso de pessoas idosas a documentos, benefícios e transporte.
- **ODS 16 — Paz, Justiça e Instituições Eficazes:** orientação sobre denúncia de violência e acesso a serviços públicos.

### 3.5. Recorte escolhido

O catálogo cobre **12 orientações em 4 categorias**:

| Categoria | Orientações |
|---|---|
| Saúde | Cartão SUS, vacina da gripe e consulta na UBS |
| Documentos | CIN (RG), CPF, título de eleitor e certidão de nascimento |
| Direitos e Benefícios | Aposentadoria, BPC/LOAS e denúncia de violência |
| Transporte | Gratuidade municipal e Carteira da Pessoa Idosa |

### 3.6. Funcionalidades da Lição 1 preservadas

- pergunta em texto livre com busca por pontuação;
- confiança **ALTA**, **MÉDIA** ou resposta não encontrada;
- até duas orientações alternativas;
- navegação por categorias;
- bloqueio de CPF, telefone e e-mail na pergunta;
- histórico de atendimentos em JSON;
- indicadores de uso;
- exportação dos atendimentos para CSV;
- aviso de fonte, data de verificação e canal não oficial.

### 3.7. Acessibilidade para pessoas idosas

A versão mobile foi pensada para quem tem pouca familiaridade com celular e dificuldade de digitar:

- botão **Falar** grande e com texto, não apenas ícone;
- transcrição em tempo real: a pessoa vê escrito o que está falando antes de enviar;
- confirmação explícita no botão **Perguntar**, para evitar envios por engano;
- botão **Ouvir resposta** que lê a orientação em voz alta, com opção de leitura automática;
- escolha da **voz do navegador** em **Mais → Aparência → Voz do navegador**, com teste e preferência automática por vozes mais naturais (Google, Microsoft Natural, Enhanced ou Premium);
- **voz natural Azure opcional**, desligada por padrão e ativada com consentimento explícito em **Mais → Aparência → Motor de voz**, para uma leitura menos robotizada;
- textos e áreas de toque maiores, tema claro/escuro e aumento do tamanho da letra;
- mensagens de erro simples e instrução para usar o **microfone do teclado** quando o navegador não tiver ditado por voz.

O reconhecimento de voz usa a Web Speech API do navegador e só funciona em contexto seguro (`https` ou arquivo local). O aplicativo não grava áudio; alguns navegadores podem enviar o áudio a um serviço online do fabricante para transcrever. No Safari do Mac, o ditado pode retornar erro de rede mesmo com internet; para o botão **Falar** funcionar, o **Ditado** precisa estar ativado em **Ajustes do Sistema → Teclado → Ditado**. Se ainda falhar, a alternativa é usar o Google Chrome ou o Ditado do macOS (Fn duas vezes). Por isso, o ditado é opcional e o teclado — inclusive o microfone do teclado do celular — continua funcionando em qualquer situação.

A leitura em voz alta usa, por padrão, as vozes instaladas no sistema ou oferecidas pelo navegador. Vozes de assistentes como Siri e Gemini não são expostas a páginas web; para uma leitura menos robotizada, o aplicativo prioriza vozes naturais quando disponíveis e permite escolher outra voz. No Mac, vozes **Enhanced** ou **Premium** podem ser instaladas em **Ajustes do Sistema → Acessibilidade → Conteúdo Falado → Voz do Sistema → Gerenciar Vozes**.

Como alternativa, o projeto oferece uma **voz neural Azure** opcional. O app continua funcionando offline com a voz do navegador; a voz natural só é usada depois que a pessoa escolhe **Natural (Azure)** e confirma o aviso de privacidade. A chave da API fica em `mobile/.env`, no computador, e nunca no `index.html`; o servidor bloqueia o download de `.env` e da pasta `.cache`. O pequeno servidor `mobile/servir.py` expõe `POST /api/tts`, valida o texto (limite de 600 caracteres), escapa o SSML, usa cache por texto e voz, aplica tempo limite, limita 20 requisições por minuto por IP e faz fallback para a voz do navegador quando o serviço falha. Apenas o **texto da resposta** é enviado ao Azure; a pergunta não é enviada. Sem chave, o servidor inicia em **modo de teste** (`TTS_PROVIDER=mock`), que valida a interface e a reprodução sem avaliar a qualidade da voz Azure.

---

## 4. Implementação da Lição 2 — estrutura e algoritmos

A Lição 2 acrescentou os requisitos de estruturas de dados e algoritmos:

- lista encadeada própria com nós e referências;
- cadastro, consulta, atualização e exclusão;
- busca por identificador e pesquisa por atributo;
- ordenação com algoritmo próprio;
- análise dos dados cadastrados;
- menu, validação de entradas e testes.

### 4.1. O que foi unificado

| Item | Lição 1 | Lição 2 | Solução unificada |
|---|---|---|---|
| Registro | `Orientacao` | `Servico` | `Servico` com todos os campos |
| Texto principal | `resposta` | `descricao` | `descricao` |
| Documentos | lista `documentos` | texto `requisitos` | lista `documentos` |
| Local | `onde` | `local` | `local` |
| Palavras-chave | `palavras_chave` | não existia | `palavras_chave` |
| Verificação | `verificado_em` | não existia | `verificado_em` |
| Armazenamento | lista Python | lista encadeada | lista encadeada |
| Base de dados | `base_conhecimento.json` | `servicos.json` | um único `servicos.json` |
| Atendimento | pergunta, categorias, histórico, CSV | não existia | mantido no menu unificado |
| CRUD e algoritmos | não existiam | completos | mantidos no menu unificado |

O carregador aceita os nomes antigos (`resposta`, `requisitos`, `onde`) para facilitar a importação de dados das duas versões. O arquivo unificado já foi gerado a partir das duas bases, que continham os mesmos 12 registros.

### 4.2. Organização do código

O código foi separado por responsabilidade:

| Arquivo | Responsabilidade |
|---|---|
| `app/modelos.py` | classe `Servico` |
| `app/texto.py` | normalização de texto (acentos, maiúsculas e pontuação) |
| `app/lista_encadeada.py` | `No`, `ListaEncadeada`, CRUD, busca e Selection Sort |
| `app/base_conhecimento.py` | categorias, pontuação e ranking da busca |
| `app/assistente.py` | atendimento, navegação, histórico, indicadores e CSV |
| `app/persistencia.py` | leitura/gravação JSON e exportação CSV |
| `app/interface.py` | menu, validação de entradas e operações do catálogo |
| `main.py` | carrega os dados e inicia o sistema |

---

## 5. Modelo dos registros

A classe `Servico` representa um registro do catálogo:

| Campo | Tipo | Obrigatório | Exemplo |
|---|---|---|---|
| `id` | inteiro | sim | `1` |
| `titulo` | texto | sim | `Fazer o Cartão Nacional de Saúde (Cartão SUS)` |
| `categoria` | texto | sim | `Saúde` |
| `descricao` | texto | sim | `O Cartão Nacional de Saúde (CNS) é gratuito...` |
| `documentos` | lista de textos | sim | `["Documento com foto", "CPF"]` |
| `local` | texto | sim | `Qualquer UBS` |
| `fonte` | texto | recomendado | `https://www.gov.br/...` |
| `palavras_chave` | lista de textos | recomendado | `["cartao sus", "sus"]` |
| `verificado_em` | texto (data) | recomendado | `2026-11-05` |

O `id` é único. A operação de inserção recusa um ID que já exista na lista.

---

## 6. Lista encadeada

A lista está em `app/lista_encadeada.py` e foi implementada com classes e referências, sem usar listas prontas para armazenar os registros.

```text
inicio
  |
  v
[No: Servico 1 | proximo] --> [No: Servico 2 | proximo] --> [No: Servico 3 | proximo] --> None
```

Cada `No` guarda um `Servico` e uma referência `proximo`. A classe `ListaEncadeada` mantém `inicio` e `quantidade`.

| Operação | Método | Como funciona |
|---|---|---|
| Inserção | `inserir()` | Verifica ID duplicado e percorre até o último nó para inserir no fim |
| Percurso | `percorrer()` | Começa em `inicio` e segue `proximo` até `None` |
| Busca por ID | `buscar_por_id()` | Busca linear, nó por nó |
| Pesquisa por atributo | `pesquisar()` | Busca linear em título, categoria e descrição |
| Atualização | `atualizar()` | Localiza o nó e altera os campos permitidos |
| Remoção | `remover()` | Ajusta o `proximo` do nó anterior |
| Ordenação | `ordenar_por()` | Selection Sort trocando os dados dos nós |
| Análise | `contar_por_categoria()` | Percorre a lista e conta os registros por categoria |

A remoção trata três casos: primeiro nó, nó do meio e último nó. Em todos eles a lista continua íntegra.

---

## 7. Menu unificado

| Opção | Operação |
|---|---|
| 1 | Cadastrar serviço |
| 2 | Consultar por ID |
| 3 | Pesquisar por título, categoria ou descrição |
| 4 | Atualizar serviço |
| 5 | Excluir serviço |
| 6 | Listar todos |
| 7 | Ordenar por título, categoria ou ID |
| 8 | Análise dos serviços |
| 9 | Fazer uma pergunta |
| 10 | Navegar por categorias |
| 11 | Indicadores de atendimento |
| 12 | Exportar atendimentos para CSV |
| 13 | Agente de documentos pessoais (IA) |
| 0 | Salvar e sair |

O menu mostra a quantidade de serviços e as categorias carregadas. Opções inválidas não encerram o programa.

---

## 8. Busca implementada

### 8.1. Consulta por identificador

`ListaEncadeada.buscar_por_id(id)` percorre os nós do início ao fim e compara o ID. Se não encontrar, devolve `None` e o menu mostra `Serviço não encontrado.`.

### 8.2. Pesquisa por atributo

`ListaEncadeada.pesquisar(texto)` faz busca linear em:

- título;
- categoria;
- descrição.

A comparação ignora maiúsculas/minúsculas, acentos e pontuação. Quando não há resultado, o menu mostra `Nenhum registro encontrado.`.

### 8.3. Busca por pontuação (Lição 1)

A pergunta livre usa `BaseConhecimento.pontuar()`:

| Regra | Pontos |
|---|---|
| Uma palavra-chave da orientação aparece inteira na pergunta | +3 por palavra-chave |
| Uma palavra da pergunta (4 letras ou mais) aparece inteira no título | +1 por palavra |

| Pontuação da melhor orientação | Resultado |
|---|---|
| 6 pontos ou mais | Confiança **ALTA** |
| 3 a 5 pontos | Confiança **MÉDIA** |
| menos de 3 pontos | **Não encontrei** |

Exemplo: em “Como faço o cartão do SUS?”, a orientação do Cartão SUS recebe:

- +3 por `cartao do sus`;
- +3 por `sus`;
- +1 porque `cartao` aparece no título.

Total: **7 pontos → confiança ALTA**.

`BaseConhecimento.buscar()` devolve uma lista de tuplas `(pontos, servico)` da maior para a menor pontuação. O desempate usa o menor ID. O assistente mostra a melhor resposta e até duas alternativas.

A busca é **linear**. Não foi usada busca binária porque a lista encadeada não oferece acesso direto por índice. Mesmo após ordenar, seria necessário percorrer os nós para chegar ao meio.

---

## 9. Ordenação implementada

Foi implementado **Selection Sort** em `ListaEncadeada.ordenar_por()`:

1. Percorre a lista a partir do nó atual.
2. Procura o menor valor no restante da lista.
3. Troca os dados do nó atual com os do menor nó encontrado.
4. Avança para o próximo nó e repete.

Critérios disponíveis: `titulo`, `categoria` e `id`. A ordenação por texto usa `normalizar()`, que remove acentos e ignora maiúsculas.

O código **não usa `sorted()` nem `list.sort()`** para ordenar os registros. Também foram implementados, pela equipe, pequenos Insertion Sorts auxiliares para:

- ordenar as categorias exibidas no menu;
- ordenar os resultados da busca por pontuação;
- ordenar a contagem por categoria na análise.

Esses Insertion Sorts auxiliares não substituem o Selection Sort exigido: a ordenação do catálogo é feita pelo Selection Sort.

---

## 10. Atualização, exclusão e integridade

- **Atualização:** localiza o registro pelo ID e altera apenas os campos informados. Enter mantém o valor atual.
- **Exclusão:** localiza o nó, ajusta o ponteiro do nó anterior e diminui a quantidade. Pede confirmação `s/n`.
- **ID inexistente:** consulta, atualização e exclusão mostram mensagem e não alteram a lista.
- **ID duplicado:** o cadastro é recusado.
- **Persistência:** o catálogo é salvo em `data/servicos.json` após cada alteração e ao sair.
- **Lista vazia:** listagem, ordenação e análise tratam o caso sem erro.

---

## 11. Análise de dados

O sistema produz duas análises complementares.

### 11.1. Análise dos serviços (opção 8)

- total de registros;
- quantidade e percentual por categoria;
- categoria com mais serviços;
- registros sem palavras-chave;
- registros sem fonte;
- total de palavras-chave e média por registro.

### 11.2. Indicadores de atendimento (opção 11)

- atendimentos realizados;
- percentual de respostas encontradas;
- percentual de respostas que ajudaram a resolver a dúvida;
- tempo médio para encontrar a resposta;
- tentativas por atendimento;
- facilidade de uso (1 a 5);
- lista de dúvidas sem solução.

O histórico registra data, origem, pergunta, ID da orientação, se encontrou, se ajudou, tentativas e tempo. O CSV é gerado em `data/atendimentos.csv`.

---

## 12. Validação, privacidade e robustez

- ID deve ser inteiro positivo; ID duplicado é recusado.
- Título, categoria, descrição e local não podem ficar vazios.
- Opções de menu fora da faixa são recusadas e o menu é mostrado novamente.
- Respostas diferentes de `s/n` são recusadas.
- Consulta, atualização e exclusão de ID inexistente mostram mensagem.
- Pesquisa sem resultado mostra `Nenhum registro encontrado.`
- Lista vazia é tratada em listagem, ordenação e análise.
- JSON ausente, corrompido ou com registro incompleto não derruba o programa.
- O histórico antigo, se inválido, é substituído por um novo com aviso.
- Perguntas com **8 ou mais dígitos** ou com **@** são recusadas e **não entram no histórico**.
- Toda resposta mostra fonte, data de verificação e o aviso de que o assistente não é um canal oficial.

---

## 13. Análise de complexidade Big-O

Legenda: `n` = quantidade de registros; `m` = tamanho dos textos comparados; `r` = quantidade de resultados; `k` = quantidade de categorias.

| Operação | Complexidade | Justificativa |
|---|---|---|
| Inserir no fim | `O(n)` | Verifica ID duplicado (`O(n)`) e percorre até o último nó (`O(n)`) |
| Buscar por ID | `O(n)` | No pior caso, percorre todos os nós; no melhor caso, `O(1)` |
| Pesquisar por texto | `O(n * m)` | Normaliza e compara três campos de cada nó |
| Atualizar | `O(n)` | Localiza o nó; a alteração dos campos é `O(1)` |
| Remover | `O(n)` | Localiza o nó; o ajuste dos ponteiros é `O(1)` |
| Percorrer/listar | `O(n)` | Visita cada nó uma vez |
| Ordenar (Selection Sort) | `O(n²)` | Para cada nó, percorre o restante da lista |
| Contar por categoria | `O(n)` | Percorre a lista uma vez e usa `O(k)` de memória |
| Ordenar a contagem | `O(k²)` | Insertion Sort auxiliar sobre as categorias |
| Busca por pontuação | `O(n * m + r²)` | Pontua todos os nós e ordena os `r` resultados com Insertion Sort |
| Carregar/salvar JSON | `O(n)` | Converte cada registro uma vez |
| Exportar CSV | `O(n)` | Escreve cada atendimento uma vez |

**Memória auxiliar:** a lista usa `O(n)` para os nós. A ordenação por troca de dados usa `O(1)` de memória extra. A busca por texto usa `O(r)` para os resultados. O histórico usa `O(h)` para `h` atendimentos.

**Por que não usar estrutura pronta?** O requisito pede a implementação da lista encadeada e de pelo menos um algoritmo de ordenação pela equipe. Por isso, o armazenamento do catálogo é feito apenas com nós e referências, e a ordenação do catálogo é feita com Selection Sort.

---

## 14. Testes realizados

### 14.1. Testes automatizados

Comando:

```bash
cd Jun
python3 -m unittest discover -s testes -t . -v
```

Resultado observado:

```text
Ran 81 tests in 0.058s

OK
```

> **Atualização (2026-11-10):** este bloco registra a suíte original dos Projetos 1 e 2. Depois da inclusão do agente, `python3 -m unittest discover -s testes -t .` passou a executar **143 testes**: 82 do catálogo/mobile e 61 do agente/avaliação/provedor. O `test_integracao.py` ganhou 1 teste da opção 13 (17 → 18). Veja [`EVIDENCIAS_TESTES.md`](EVIDENCIAS_TESTES.md).

Distribuição dos 81 testes originais:

| Arquivo | Testes | Cobertura |
|---|---:|---|
| `testes/test_lista_encadeada.py` | 14 | inserção, percurso, busca, atualização, remoção, ordenação, lista vazia e integridade dos ponteiros |
| `testes/test_base_conhecimento.py` | 9 | dados unificados, categorias, pontuação, ranking, empate e busca sem resultado |
| `testes/test_assistente.py` | 11 | pergunta, categorias, privacidade, histórico, indicadores, CSV e encerramento |
| `testes/test_persistencia.py` | 8 | JSON, compatibilidade com as duas versões, arquivo ausente, JSON corrompido e CSV |
| `testes/test_integracao.py` | 17 | validações, CRUD completo e fluxo do menu unificado |
| `testes/test_tts_mobile.py` | 22 | configuração mock/Azure, chave e região, SSML, escape, cache, formatos de áudio, voz inválida, erros HTTP, `.env`, limite por IP e bloqueio de `.env`/`.cache` |

A versão mobile tem testes próprios, executados com Node.js:

```bash
cd Jun/mobile
node teste-logica.js
```

Resultado atual: **78 verificações aprovadas**, cobrindo lista encadeada, ordenação, busca, privacidade, histórico, CSV, indicadores, voz do navegador, motor de voz natural e renderização das telas.

### 14.2. Casos cobertos

| Caso | Entrada | Resultado esperado | Resultado observado |
|---|---|---|---|
| Cadastro normal | ID 99 e dados completos | Serviço cadastrado | `Serviço cadastrado com sucesso.` |
| ID duplicado | ID 1 | Cadastro recusado | `Já existe um serviço com esse ID.` |
| Consulta existente | ID 4 | Registro exibido | Título, documentos, local, fonte e aviso |
| Consulta inexistente | ID 999 | Não encontrado | `Serviço não encontrado.` |
| Pesquisa por atributo | `saude` | 3 resultados | 3 registros da categoria Saúde |
| Pesquisa sem resultado | `xyz` | Nenhum resultado | `Nenhum registro encontrado.` |
| Atualização | ID 99, novo título | Campo atualizado; demais mantidos | `Serviço atualizado com sucesso.` |
| Atualização inexistente | ID 999 | Não encontrado | `Serviço não encontrado.` |
| Exclusão confirmada | ID 99, `s` | Registro removido | `Serviço excluído.` |
| Exclusão cancelada | ID 99, `n` | Nada alterado | `Operação cancelada.` |
| Exclusão inexistente | ID 999 | Não encontrado | `Serviço não encontrado.` |
| Opção inválida | `14` | Pedir novamente | `Entrada inválida. Digite um número de 0 a 13.` |
| Texto vazio | Enter | Pedir novamente | `Este campo não pode ficar vazio.` |
| Lista vazia | ordenar/listar/analisar | Sem erro | Avisos específicos |
| Pergunta encontrada | `Como faço o cartão do SUS?` | Confiança ALTA | 7 pontos |
| Pergunta sem resultado | `assunto inexistente` | Não encontrada | `Não encontrei uma orientação para essa dúvida.` |
| Dado pessoal | CPF na pergunta | Pergunta recusada | `Atenção: não digite CPF...` e nada no histórico |
| Arquivo ausente | JSON inexistente | Sem erro | Lista vazia e aviso |
| JSON corrompido | arquivo inválido | Sem erro | Lista vazia e aviso |

### 14.3. Teste manual de ponta a ponta

Foi executada uma sessão real do `main.py`, com backup e restauração dos dados de entrega, cobrindo:

1. cadastro do ID 99;
2. consulta do ID 99;
3. pesquisa por `manual`;
4. atualização do ID 99;
5. exclusão do ID 99 com confirmação;
6. ordenação por título com Selection Sort;
7. análise dos 12 serviços;
8. pergunta “Como faço o cartão do SUS?” com confiança ALTA (7 pontos);
9. indicadores de atendimento;
10. exportação CSV;
11. encerramento com nota de facilidade.

Resultados observados:

```text
Serviço cadastrado com sucesso.
>> Serviço de Teste E2E [Teste]
1 resultado(s):
Serviço atualizado com sucesso.
Serviço excluído.
Lista ordenada por titulo (Selection Sort):
Total de registros: 12
Confiança da resposta: ALTA (7 pontos)
Atendimentos: 1
CSV exportado: .../data/atendimentos.csv (1 atendimentos).
Obrigado por usar o Citizen Assist AI!
```

Após o teste, os arquivos de dados foram restaurados para o estado de entrega.

---

## 15. Estrutura final de pastas e arquivos

```text
Jun/
├── main.py                        # ponto de entrada
├── app/
│   ├── __init__.py
│   ├── modelos.py                 # classe Servico
│   ├── texto.py                   # normalização de texto
│   ├── lista_encadeada.py         # No e ListaEncadeada
│   ├── base_conhecimento.py       # categorias, pontuação e ranking
│   ├── assistente.py              # atendimento, histórico e indicadores
│   ├── persistencia.py            # JSON e CSV
│   └── interface.py               # menu, validações e CRUD
├── data/
│   ├── servicos.json              # 12 registros unificados
│   ├── historico.json             # histórico de atendimentos
│   └── atendimentos.csv           # exportação dos atendimentos
├── testes/
│   ├── __init__.py
│   ├── apoio.py
│   ├── test_lista_encadeada.py
│   ├── test_base_conhecimento.py
│   ├── test_assistente.py
│   ├── test_persistencia.py
│   ├── test_integracao.py
│   └── test_tts_mobile.py         # voz natural do app mobile
├── mobile/
│   ├── index.html                 # app mobile completo
│   ├── servir.py                  # servidor local e API de voz
│   ├── tts.py                     # Azure ou modo de teste
│   ├── __init__.py
│   ├── .env.example               # modelo sem chave real
│   ├── .gitignore
│   ├── teste-logica.js
│   └── README.md
├── docs/
│   └── DOCUMENTACAO.md            # este documento
├── README.md
└── .gitignore
```

---

## 16. Como executar

Pré-requisito: Python 3.8 ou superior. O projeto usa apenas a biblioteca padrão.

```bash
cd Jun
python3 main.py
```

No Windows, pode ser:

```bash
python main.py
```

Não é necessário instalar dependências. O sistema lê e grava os arquivos na pasta `data/`.

Para abrir o app mobile no computador ou no celular pela rede local:

```bash
python3 mobile/servir.py
```

A voz natural Azure é opcional. Sem `mobile/.env`, o servidor inicia em modo de teste. Para usar a voz real, copie `mobile/.env.example` para `mobile/.env`, preencha `AZURE_SPEECH_KEY` e `AZURE_SPEECH_REGION` e reinicie o servidor. O app também pode ser aberto diretamente pelo `mobile/index.html`, mas nesse caso a voz natural não funciona e a voz do navegador é usada.

### Testes

```bash
python3 -m unittest discover -s testes -t . -v
node mobile/teste-logica.js
```

---

## 17. Checklist dos requisitos da Global Solution

| Requisito oficial | Onde está implementado | Status |
|---|---|---|
| Cadastro de múltiplos registros com ID único | menu 1, `cadastrar()`, `ListaEncadeada.inserir()` | Atendido |
| Dados mantidos em lista encadeada própria | `No`, `ListaEncadeada`, `inicio`/`proximo` | Atendido |
| Consulta por identificador | menu 2, `buscar_por_id()` | Atendido |
| Pesquisa por atributo relevante | menu 3, `pesquisar()` em título, categoria e descrição | Atendido |
| Explicação do algoritmo de busca | seção 8 | Atendido |
| Comportamento quando não encontra | mensagens de não encontrado | Atendido |
| Ordenação por critério definido | menu 7, título/categoria/ID | Atendido |
| Algoritmo de ordenação próprio | Selection Sort em `ordenar_por()` | Atendido |
| Sem uso exclusivo de funções prontas | nenhum `sorted()`/`.sort()` no código de produção | Atendido |
| Lista com inserção, percurso e remoção | `inserir()`, `percorrer()`, `remover()` | Atendido |
| Modelagem em Python com classes e referências | `Servico`, `No`, `ListaEncadeada` | Atendido |
| Atualização e exclusão preservando a lista | menus 4 e 5 | Atendido |
| Informação útil de processamento | menus 8 e 11 | Atendido |
| Menu interativo com todas as operações | menu 0 a 13 (12 do catálogo + agente) | Atendido |
| Validação de entradas e opções inexistentes | `ler_inteiro()`, `ler_texto()`, `confirmar()` | Atendido |
| IDs duplicados | recusa no cadastro | Atendido |
| Consultas sem resultado | mensagens específicas | Atendido |
| Análise Big-O | seção 13 | Atendido |
| Testes normais, inexistentes, inválidos e lista vazia | 81 testes originais do P1/P2 (143 na suíte atual) | Atendido |
| Persistência em arquivos (opcional) | JSON e CSV | Atendido |
| Relatórios/indicadores (opcional) | menus 8 e 11 | Atendido |
| Documentação técnica | este documento | Atendido |
| Evidências de testes | seção 14 e suíte automatizada | Atendido |
| Demonstração prática | roteiro na seção 19 | A gravar |

### 17.1. Critérios de avaliação da Global Solution

| Critério oficial | Pontos | Como o projeto atende |
|---|---:|---|
| Funcionamento do sistema, CRUD, menu e validação | 3,0 | menus 1 a 8, persistência, validações e mensagens de erro |
| Lista encadeada e recursos específicos da linguagem | 3,0 | `No`, `ListaEncadeada`, referências, percurso e remoção |
| Algoritmos de busca e ordenação implementados | 2,0 | busca linear por ID/texto, pontuação e Selection Sort |
| Organização do código, documentação e Big-O | 1,0 | módulos separados, esta documentação e seção 13 |
| Evidências de testes e demonstração | 1,0 | 81 testes do P1/P2 + 61 do agente (143 no total), teste manual e roteiro de demonstração |

O único item deste recorte P1/P2 que ainda depende da equipe é a **gravação da demonstração em vídeo**; o roteiro está pronto na seção 19. As pendências do Projeto 3 e do Projeto 4 estão na documentação única.

---

## 18. O que ainda falta e limitações

Itens que dependem da equipe ou não são exigidos:

- link do GitHub: publicado em https://github.com/C0utinhoxx/citizen-assist-ai; nomes e RMs já preenchidos;
- link do vídeo: ainda pendente;
- gravar o vídeo de demonstração;
- realizar o teste com pelo menos 3 pessoas de fora da equipe e preencher os indicadores (a Lição 1 previa esse teste);
- preencher o arquivo `.txt` de entrega no portal, se solicitado.

Limitações técnicas conscientes:

- a persistência é local, em JSON; não há banco de dados;
- a versão de terminal não tem interface gráfica; a versão mobile é um HTML separado, com dados no `localStorage`;
- o ditado por voz depende do navegador e pode exigir internet e permissão de microfone; o microfone do teclado é a alternativa compatível;
- a voz natural Azure é opcional, exige o servidor local e uma chave configurada no computador; sem chave, o modo de teste valida a interface, mas não a qualidade da voz. A pergunta nunca é enviada ao Azure, apenas o texto da resposta;
- a busca é linear; para uma base muito grande, uma estrutura indexada seria mais eficiente;
- não há autenticação, usuários ou controle de acesso concorrente;
- as informações são estáticas e devem ser conferidas nos canais oficiais;
- o assistente não é um canal oficial e não acompanha processos individuais;
- em Python não há gerenciamento manual de memória, pois a linguagem cuida disso.

---

## 19. Roteiro de demonstração prática

1. Mostrar a estrutura de pastas e o `Servico` com todos os campos.
2. Abrir `app/lista_encadeada.py` e explicar `No`, `inicio`, `proximo` e `quantidade`.
3. Executar `python3 main.py` e mostrar os 12 serviços e as 4 categorias.
4. Consultar o ID 4 e mostrar documentos, local, fonte e aviso.
5. Pesquisar `saude` e mostrar os 3 resultados.
6. Cadastrar um serviço com ID 99 e tentar cadastrar o mesmo ID novamente.
7. Atualizar o ID 99, ordenar por título e mostrar a análise da opção 8.
8. Fazer a pergunta “Como faço o cartão do SUS?” e mostrar os 7 pontos e a confiança ALTA.
9. Navegar por categorias e mostrar uma orientação.
10. Mostrar os indicadores da opção 11 e o CSV exportado.
11. Excluir o ID 99 e mostrar que a lista continua íntegra.
12. Sair e abrir `data/servicos.json` para mostrar a persistência.

Durante a demonstração, destacar que o CRUD, a busca e a ordenação percorrem a lista encadeada real, e não uma lista pronta da linguagem.

---

## 20. Fontes consultadas

Todas as fontes foram conferidas em **05/11/2026** e estão registradas em cada registro do JSON.

| Tema | Fonte oficial |
|---|---|
| Cartão SUS / Meu SUS Digital | https://www.gov.br/saude/pt-br/composicao/seidigi/meususdigital/perguntas-e-respostas/cidadao/9-como-faco-o-cartao |
| Vacinação | https://www.gov.br/saude/pt-br/vacinacao |
| Atenção Primária / UBS | https://www.gov.br/saude/pt-br/assuntos/atencao-primaria |
| Carteira de Identidade Nacional (CIN) | https://www.gov.br/governodigital/pt-br/identidade/cin |
| CPF / Receita Federal | https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf |
| Título de eleitor / TSE | https://www.tse.jus.br/servicos-eleitorais/titulo-eleitor |
| Certidão de nascimento | https://www.registrocivil.org.br/ |
| Aposentadoria por idade / INSS | https://www.gov.br/pt-br/servicos/solicitar-aposentadoria-por-idade-trabalhador-urbano |
| BPC / LOAS | https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-ao-idoso |
| Denúncia / Disque 100 | https://www.gov.br/pt-br/servicos/denunciar-violacao-de-direitos-humanos |
| Estatuto da Pessoa Idosa (Lei 10.741/2003) | https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm |
| Carteira da Pessoa Idosa | https://www.gov.br/pt-br/servicos/adquirir-carteira-do-idoso |
