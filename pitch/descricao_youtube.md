# Descrição e comentário do YouTube — Citizen Assist AI

**Status:** material pronto; publicação pendente.

Use este arquivo depois de gravar o vídeo. **Copie e cole** os blocos abaixo no
YouTube. Ajuste apenas o link do vídeo (linha `VIDEO`) e a data, se quiser.

---

## 1. Título

```text
Citizen Assist AI — Global Solution 2026.2
```

---

## 2. Descrição do vídeo

```text
Citizen Assist AI — Global Solution 2026.2 (Citizen Tech)

Orientação clara sobre documentos pessoais, sem pedir dados pessoais e sem inventar informação.

O Citizen Assist AI é um assistente digital que responde a dúvidas sobre RG, CPF, título de eleitor, carteira de trabalho, certidões e CNH. O agente usa apenas sete fichas de referência como fonte de verdade e, quando não encontra a resposta, admite e orienta a consultar o órgão competente.

O projeto tem quatro componentes:
• DSA (Projetos 1 e 2) — catálogo de serviços com lista encadeada e Selection Sort implementados manualmente, busca por pontuação, indicadores e exportação CSV.
• Citizen Assist AI (Projeto 3) — agente de IA com LangGraph, proteção de dados pessoais, resistência a prompt injection e avaliação automática no Golden Dataset de 26 casos com LLM as a Judge.
• Vídeo pitch (Projeto 4) — este vídeo.

Tecnologias: Python 3.9+, LangGraph (com fallback sequencial), modelos compatíveis com OpenAI (Groq, OpenAI e Ollama local), HTML/CSS/JavaScript sem framework.

Avaliação: 26 de 26 acertos exatos no juiz determinístico (offline, reproduzível) e 24 de 26 no juiz LLM com gpt-4o-mini e LangGraph (94,2%). O fallback sequencial recebeu nota idêntica nos 26 casos. A suíte tem 143 testes Python e 78 verificações mobile aprovados.

Importante: as fichas são material didático fictício da Central do Cidadão de Aurora, criado exclusivamente para a atividade acadêmica. O assistente não é um canal oficial e não consulta sistemas do governo. Confirme sempre as informações no órgão competente.

Integrantes:
• Bruno Riquelme Coutinho Pereira — RM 569619
• Eduardo Bigoli Portela — RM 569897
• Gustavo Fondato de Souza — RM 573651

Turma: 1CCPX

Repositório: https://github.com/C0utinhoxx/citizen-assist-ai
VIDEO
```

> O placeholder `VIDEO` deve ser substituído pela URL do YouTube depois da publicação.
> O vídeo precisa estar como **não listado**.

---

## 3. Comentário do vídeo

O enunciado pede que os integrantes e RMs sejam informados **nos comentários**.
Cole o bloco abaixo como primeiro comentário do vídeo.

```text
Trabalho em trio.

Integrantes:
• Bruno Riquelme Coutinho Pereira — RM 569619
• Eduardo Bigoli Portela — RM 569897
• Gustavo Fondato de Souza — RM 573651

Turma: 1CCPX
Global Solution 2026.2 — Citizen Tech

Projeto: Citizen Assist AI
Repositório: https://github.com/C0utinhoxx/citizen-assist-ai

Entrega realizada por: Bruno Riquelme Coutinho Pereira — RM 569619
```

> A entrega é feita por **somente um integrante**. Troque a última linha pelo
> nome e RM de quem for gravar e submeter.

---

## 4. Checklist de publicação

- [ ] Vídeo com no máximo 3 minutos.
- [ ] Narração humana (sem voz gerada por IA).
- [ ] Integrantes e RMs no início ou na descrição.
- [ ] Comentário do vídeo publicado com os nomes e RMs.
- [ ] Visibilidade **Não listado**.
- [ ] Link testado em janela anônima.
- [ ] Nenhum dado pessoal real e nenhuma chave de API na tela.
- [ ] Link do vídeo colado em `pitch/link_video.txt`.
- [ ] Link do vídeo colado na descrição (substituindo `VIDEO`).
- [ ] README e `docs/DOCUMENTACAO_UNIFICADA.md` atualizados com o link.
