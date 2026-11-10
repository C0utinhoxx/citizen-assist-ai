# Citizen Assist AI

Sistema de terminal para organizar serviços e orientações ao cidadão, desenvolvido para a **Global Solution 2026.2 — Citizen Tech** da disciplina **Data Structures and Algorithms (DSA)**.

O projeto unifica a **Lição 1** (proposta de atendimento ao cidadão) e a **Lição 2** (lista encadeada e algoritmos) em uma única solução em **Python**.

## O que o sistema faz

- Cadastra, consulta, atualiza e exclui serviços em uma **lista encadeada implementada pela equipe**.
- Consulta por ID e pesquisa por título, categoria ou descrição.
- Ordena por título, categoria ou ID com **Selection Sort** próprio.
- Analisa os serviços por categoria e gera indicadores de atendimento.
- Responde perguntas em texto livre com pontuação e confiança.
- No celular, aceita **pergunta por voz** (com o texto aparecendo na tela) e lê a resposta em voz alta, com voz do navegador offline ou voz natural Azure opcional.
- Navega por categorias.
- Mantém histórico, exporta CSV e protege dados pessoais.
- Persiste o catálogo em JSON.

## Como executar

Pré-requisito: Python 3.8 ou superior, sem dependências externas.

```bash
cd Jun
python3 main.py
```

No Windows:

```bash
python main.py
```

## Versão mobile (celular)

Além do terminal, o projeto tem uma versão mobile completa em **um único arquivo HTML**, para rodar no celular **sem instalação e sem hospedagem**. O app funciona offline; o ditado por voz e a voz natural Azure são opcionais e podem depender de internet:

- [`mobile/index.html`](mobile/index.html) — app completo (HTML + CSS + JavaScript + os 12 serviços iniciais embutidos).
- [`mobile/README.md`](mobile/README.md) — como transferir e abrir no Android/iPhone, backup, voz natural, servidor local opcional e solução de problemas.
- [`mobile/servir.py`](mobile/servir.py) — servidor local opcional, sem dependências, para abrir o app pelo Wi-Fi quando o navegador do celular bloqueia arquivos locais e para a API de voz natural.
- [`mobile/tts.py`](mobile/tts.py) — adaptador de voz natural (Azure) com modo de teste, cache e validação; a chave fica no computador, nunca no HTML.
- [`mobile/.env.example`](mobile/.env.example) — modelo de configuração da voz natural.
- [`mobile/teste-logica.js`](mobile/teste-logica.js) — testes da lógica com Node.js.

Para usar no celular, envie o `mobile/index.html` por WhatsApp, e-mail, Google Drive, AirDrop ou cabo USB e abra no navegador. No iPhone, se o armazenamento local for bloqueado em `file://`, execute `python3 mobile/servir.py` no computador e abra o endereço de rede exibido no celular. Para a voz natural, copie `mobile/.env.example` para `mobile/.env` e preencha a chave do Azure; sem chave, o servidor inicia em modo de teste.

A versão mobile reimplementa a lista encadeada, o Selection Sort, a busca por pontuação, o histórico, os indicadores e o CSV em JavaScript. Os dados ficam no `localStorage` do aparelho. A aba **Assistente** tem um botão **Falar** que transcreve a pergunta em tempo real e um botão **Ouvir resposta** que lê a orientação em voz alta, com escolha entre a voz do navegador (offline) e a voz natural Azure (opcional) em **Aparência**. A voz natural é desligada por padrão e, quando ativada, envia apenas o texto da resposta ao Azure; a pergunta não é enviada. Veja os requisitos, o modo de teste e os limites em [`mobile/README.md`](mobile/README.md#voz-natural-azure--opcional). Testes da lógica mobile: **78 verificações aprovadas** com `node mobile/teste-logica.js`.

## Testes

```bash
python3 -m unittest discover -s testes -t . -v
node mobile/teste-logica.js
```

Resultado atual: **81 testes Python aprovados** (59 do sistema + 22 da voz natural mobile) e **78 verificações mobile** aprovadas.

## Estrutura

```text
Jun/
├── main.py
├── app/
│   ├── modelos.py
│   ├── texto.py
│   ├── lista_encadeada.py
│   ├── base_conhecimento.py
│   ├── assistente.py
│   ├── persistencia.py
│   └── interface.py
├── data/
│   ├── servicos.json
│   ├── historico.json
│   └── atendimentos.csv
├── mobile/
│   ├── index.html
│   ├── servir.py
│   ├── tts.py
│   ├── __init__.py
│   ├── .env.example
│   ├── .gitignore
│   ├── teste-logica.js
│   └── README.md
├── testes/
│   ├── test_tts_mobile.py
│   └── ... (demais testes Python)
├── docs/
│   └── DOCUMENTACAO.md
├── README.md
└── .gitignore
```

## Menu

| Opção | Operação |
|---|---|
| 1 | Cadastrar serviço |
| 2 | Consultar por ID |
| 3 | Pesquisar por título, categoria ou descrição |
| 4 | Atualizar serviço |
| 5 | Excluir serviço |
| 6 | Listar todos |
| 7 | Ordenar e listar |
| 8 | Análise dos serviços |
| 9 | Fazer uma pergunta |
| 10 | Navegar por categorias |
| 11 | Indicadores de atendimento |
| 12 | Exportar atendimentos para CSV |
| 0 | Salvar e sair |

## Documentação

A documentação unificada, com a proposta da Lição 1, a implementação da Lição 2, a análise Big-O, o checklist dos requisitos e as evidências de testes, está em:

- [`docs/DOCUMENTACAO.md`](docs/DOCUMENTACAO.md)

As versões originais dos dois projetos foram preservadas em `../python` e `../dts`, sem alterações.
