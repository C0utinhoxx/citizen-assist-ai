# Entrega — PCP (Pensamento Computacional e Programação)

**Global Solution 2026.2 — Citizen Tech**
**Disciplina:** Pensamento Computacional e Programação
**Turma:** 1CCPX
**Instituição:** FIAP

**Integrantes:**

- Bruno Riquelme Coutinho Pereira — RM 569619
- Eduardo Bigoli Portela — RM 569897
- Gustavo Fondato de Souza — RM 573651

**Repositório:** https://github.com/C0utinhoxx/citizen-assist-ai
**Vídeo técnico:** pendente de gravação e publicação como não listado.

---

## 1. Problema e público

**Público:** pessoas idosas (60 anos ou mais) e familiares ou cuidadores que ajudam essas pessoas a acessar serviços públicos.

**Problema:** a informação sobre serviços públicos está espalhada em vários sites, escrita em linguagem técnica e misturada com páginas que não são oficiais. A pessoa perde tempo, vai ao lugar errado ou leva documentos incompletos.

**Proposta:** um assistente em terminal que responde com uma base verificada, mostra documentos, local, fonte e data de verificação, e avisa que não é canal oficial.

---

## 2. O que foi entregue

| Requisito | Como foi atendido | Onde está |
|---|---|---|
| Três classes | `Orientacao`, `BaseConhecimento` e `Assistente` | `app/modelos.py`, `app/base_conhecimento.py`, `app/assistente.py` |
| Base em JSON | 18 orientações, 5 categorias, campos do enunciado | `data/base_conhecimento.json` |
| Busca com pontuação | +3 por palavra-chave e +1 por palavra do título | `app/base_conhecimento.py` |
| Confiança | ALTA com 6 pontos ou mais; MÉDIA de 3 a 5 | `app/assistente.py` |
| Categorias | Navegação pela opção 10 | `app/interface.py` |
| Entrada inválida | Validação de opções, textos vazios e IDs | `app/interface.py` |
| Bloqueio de PII | CPF, RG, CNH, título, telefone, e-mail, endereço e números longos | `app/assistente.py` |
| Histórico e indicadores | JSON e opção 11 | `data/historico.json`, `app/assistente.py` |
| Exportação CSV | Opção 12 | `data/atendimentos.csv` |
| Integração com IA | Opção 13 | `app/interface.py` |
| Integração com SERS | Opção 14 | `app/interface.py`, `sers/` |
| Teste com usuários | Protocolos e planilhas prontos | `testes_usuarios/` |
| Vídeo técnico | Roteiro pronto | `pitch/roteiro.md` |

### As três classes

- **`Orientacao`** guarda um registro da base: id, categoria, título, palavras-chave, resposta, documentos, onde, fonte e data de verificação.
- **`BaseConhecimento`** carrega o JSON, valida os registros, calcula a pontuação e devolve o ranking.
- **`Assistente`** conversa com o usuário, aplica segurança, registra o atendimento e calcula os indicadores.

### Exemplo de pontuação

Pergunta: `Como faço o cartão do SUS?`

- `cartao do sus` → +3
- `sus` → +3
- `cartao` aparece no título → +1
- Total: **7 pontos → confiança ALTA**

---

## 3. Como executar

```bash
cd Jun
python3 main.py
```

Menu principal:

| Opção | Operação |
|---:|---|
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
| 13 | Agente de documentos pessoais (IA) |
| 14 | Energia e sustentabilidade (SERS) |
| 0 | Salvar e sair |

---

## 4. Testes e evidências

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

A suíte cobre catálogo, lista encadeada, persistência, assistente, agente, avaliação, SERS, API e voz mobile. Os testes do PCP incluem:

- carga do JSON e campos obrigatórios;
- busca com pontuação e ranking;
- pergunta encontrada, não encontrada e com PII;
- histórico, indicadores e CSV;
- CRUD completo;
- entrada inválida e lista vazia.

Evidências detalhadas: [`../docs/EVIDENCIAS_TESTES.md`](../docs/EVIDENCIAS_TESTES.md).

---

## 5. Teste com usuários

**Status:** protocolo pronto; execução pendente.

- Protocolo completo: [`../testes_usuarios/protocolo.md`](../testes_usuarios/protocolo.md)
- Versão rápida: [`../testes_usuarios/protocolo_rapido.md`](../testes_usuarios/protocolo_rapido.md)
- Planilha: [`../testes_usuarios/planilha.csv`](../testes_usuarios/planilha.csv)
- Questionário: [`../testes_usuarios/questionario.csv`](../testes_usuarios/questionario.csv)
- Relatório: [`../testes_usuarios/relatorio.md`](../testes_usuarios/relatorio.md)

Regra: pelo menos **3 pessoas externas** e **10 atendimentos**, sem nomes ou dados pessoais. Os resultados só devem ser preenchidos depois da execução real.

---

## 6. Decisões técnicas

1. **Busca por regras em vez de embeddings.** É explicável, offline e reproduzível; cada ponto pode ser auditado.
2. **JSON em vez de banco de dados.** Atende ao escopo, é legível e fácil de versionar.
3. **PII bloqueada antes da busca.** A pergunta com CPF não entra no histórico e não é repetida.
4. **Base separada do agente de IA.** O catálogo usa fontes oficiais; o agente usa apenas as fichas FC-01 a FC-07.

---

## 7. Limitações

- A base é estática e local: 18 orientações em 5 categorias.
- A busca não entende sinônimos que não estejam nas palavras-chave.
- Não há banco de dados, autenticação ou múltiplos usuários simultâneos.
- O assistente não consulta sistemas do governo e não é canal oficial.
- As estimativas de energia dependem de tarifa, consumo e condições do imóvel.

---

## 8. Pendências antes de entregar

- [ ] Executar o teste com pelo menos 3 pessoas e 10 atendimentos.
- [ ] Preencher a planilha, o questionário e o relatório.
- [ ] Registrar uma melhoria concreta feita após o teste.
- [ ] Gravar o vídeo técnico de 5 a 8 minutos com todos os integrantes falando.
- [ ] Publicar o vídeo como não listado e colar o link em `PCP.txt`.
- [ ] Confirmar que o repositório abre sem login.

---

## 9. Roteiro do vídeo técnico

O roteiro completo está em [`../pitch/roteiro.md`](../pitch/roteiro.md). Blocos obrigatórios:

1. Equipe, público e problema.
2. JSON e um registro da base.
3. Classes `Orientacao`, `BaseConhecimento` e `Assistente`.
4. `normalizar()` e `pontuar()` no exemplo do Cartão SUS.
5. Execução: pergunta encontrada, não encontrada, entrada inválida e CPF bloqueado.
6. Alteração ao vivo no JSON e nova busca.
7. Histórico, CSV e indicadores.
8. Uma decisão técnica e uma limitação.

---

## 10. Texto para o portal

O arquivo [`PCP.txt`](PCP.txt) contém o texto pronto. Falta apenas o link do vídeo.
