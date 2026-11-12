# Citizen Assist AI — versão mobile

Aplicativo completo em **um único arquivo HTML**, feito para rodar no celular **sem instalação e sem hospedagem**. Ele reimplementa em JavaScript a mesma lógica do projeto Python e guarda os dados no próprio aparelho. O app funciona offline; o ditado por voz é opcional e pode depender do serviço de voz do navegador. A **voz natural Azure** também é opcional: quando ativada, só o texto da resposta é enviado ao serviço, nunca a pergunta.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `index.html` | O aplicativo inteiro: HTML, CSS, JavaScript e os 12 serviços iniciais embutidos. É o único arquivo necessário no celular. |
| `servir.py` | Opcional. Servidor local em Python para abrir o app pelo Wi-Fi quando o navegador do celular bloqueia arquivos locais. Também oferece a API opcional de voz natural. |
| `tts.py` | Opcional. Síntese de voz natural (Azure) ou modo de teste, usada pelo `servir.py`. A chave da API fica no computador, nunca no HTML. |
| `.env.example` | Modelo de configuração da voz natural. Copie para `.env` e preencha a chave do Azure. |
| `teste-logica.js` | Opcional. Testes automatizados da lógica, executados no computador com Node.js. |
| `README.md` | Este guia. |

## Como levar para o celular

Você pode enviar o `index.html` por WhatsApp, Telegram, e-mail, Google Drive, AirDrop, cabo USB ou qualquer outro meio. Depois, abra o arquivo no navegador do celular.

### Android

1. Salve o `index.html` no celular (por exemplo, em `Downloads`).
2. Abra o arquivo com o **Chrome** ou outro navegador.
3. Se ele abrir como texto, use **Abrir com → Chrome** ou digite no navegador:
   `file:///sdcard/Download/index.html`
4. No menu do Chrome, escolha **Adicionar à tela inicial** para criar um atalho.

### iPhone / iPad

1. Salve o `index.html` no app **Arquivos** (em “Meu iPhone” ou “No meu iPad”).
2. Toque no arquivo para visualizar.
3. Se o Safari bloquear o JavaScript ou o armazenamento, use a opção do servidor local abaixo. O iOS às vezes bloqueia `localStorage` em endereços `file://`.
4. Para um atalho, no Safari use **Compartilhar → Adicionar à Tela de Início**. Funciona melhor quando o app é aberto por `http://` (servidor local).

> **Importante:** em `file://`, alguns navegadores bloqueiam o armazenamento. O app mostra um aviso vermelho e continua funcionando só durante a sessão. Nesse caso, exporte um backup em **Mais → Exportar backup completo** ou use o servidor local.

## Opção recomendada no iPhone: servidor local

O servidor local **não é hospedagem** e não publica nada na internet. Ele apenas entrega o arquivo para o celular na mesma rede Wi-Fi.

No computador, dentro da pasta `mobile`:

```bash
python3 servir.py
```

O terminal mostra algo assim:

```text
 Computador: http://localhost:8000/
 Celular:    http://192.168.0.10:8000/
```

No celular, abra o endereço **Celular** no navegador. O computador e o celular precisam estar na mesma rede Wi-Fi. Se não abrir, verifique o firewall do computador. Para parar, pressione `Ctrl+C`.

> **Voz no iPhone:** o servidor local usa `http`, e o Safari exige `https` (ou arquivo local) para liberar o microfone. Se o botão **Falar** não aparecer nesse endereço, use o **microfone do teclado** do iPhone ou abra o app por um endereço `https`.

Para usar outra porta:

```bash
python3 servir.py --port 8080
```

Para escolher uma porta livre automaticamente:

```bash
python3 servir.py --port 0
```

## O que dá para fazer

- Cadastrar, consultar, editar e excluir serviços.
- Pesquisar por título, categoria ou descrição.
- Filtrar por categoria e ordenar por título, categoria ou ID.
- Fazer perguntas em texto livre e receber uma orientação com nível de confiança.
- **Falar a pergunta** em vez de digitar, com o texto aparecendo na tela enquanto você fala.
- **Ouvir a resposta** em voz alta, com leitura automática opcional.
- Escolher entre a **voz do navegador** (offline) e a **voz natural Azure** (internet), com teste antes de usar.
- Navegar por categorias.
- Ver a análise dos serviços (quantidade por categoria e qualidade dos registros).
- Ver indicadores de atendimento (quantidade, respostas encontradas, ajuda, tempo médio, tentativas e facilidade).
- Avaliar a facilidade de uso com 1 a 5 estrelas.
- Exportar atendimentos em **CSV**.
- Exportar e importar **backup em JSON**.
- Alternar entre tema claro, escuro e automático.
- Aumentar o tamanho do texto.
- Restaurar os 12 serviços de exemplo.

## Voz: falar em vez de digitar

A aba **Assistente** tem um botão grande **Falar**, pensado para quem tem dificuldade de digitar:

1. Toque em **Falar**.
2. Se o navegador pedir, permita o uso do **microfone**.
3. Fale devagar. O que você disser aparece escrito na caixa em tempo real.
4. Toque em **Parar de falar** quando terminar.
5. Confira o texto e toque em **Perguntar**.

Depois da resposta, toque em **Ouvir resposta** para o aplicativo ler a orientação em voz alta. Em **Mais → Aparência → Leitura em voz alta** você pode deixar a leitura automática ligada.

Na mesma tela, em **Voz do navegador (offline)**, você pode escolher a voz e tocar em **Ouvir teste da voz do navegador**. O aplicativo prefere automaticamente vozes mais naturais quando existem: Google, Microsoft Natural, Enhanced ou Premium. Se a lista estiver vazia, toque em **Atualizar vozes** ou instale uma voz em português no aparelho. Para uma voz ainda mais natural, use o **Motor de voz → Natural (Azure)** descrito abaixo.

### O que você precisa saber

- O ditado usa a **Web Speech API** do próprio navegador, em português do Brasil. Não é um serviço do aplicativo.
- Funciona melhor no **Chrome do Android** e no **Safari do iPhone** (iOS 14.5 ou superior). No Firefox para computador o ditado geralmente não existe.
- No **Safari do Mac**, o ditado pode mostrar erro de rede mesmo com internet. Ative o **Ditado** em **Ajustes do Sistema → Teclado → Ditado** e permita o microfone; o próprio botão **Falar** do Safari depende desse recurso. Se ainda falhar, use o **Google Chrome** ou pressione **Fn duas vezes** na caixa de texto para usar o Ditado do macOS.
- No **Chrome do Mac**, se aparecer erro de rede, verifique VPN, proxy ou firewall da rede: o Chrome usa um serviço online do Google para transcrever.
- A voz do navegador vem do **sistema ou do navegador**, não é uma voz do aplicativo. Vozes como Siri e Gemini não ficam disponíveis para sites; para chegar perto delas, instale uma voz **Enhanced/Premium** no aparelho, use Chrome/Edge ou ative a **voz natural Azure** opcional.
- No **Mac**, instale vozes melhores em **Ajustes do Sistema → Acessibilidade → Conteúdo Falado → Voz do Sistema → Gerenciar Vozes**. Depois volte em **Aparência → Voz do navegador** e escolha a voz.
- O microfone precisa de **permissão** do navegador. Se você negar, o app avisa e continua funcionando pelo teclado.
- Em alguns navegadores, o reconhecimento de voz usa **internet** e pode enviar o áudio para um serviço online do fabricante. O app **não grava nem guarda áudio**.
- Se o botão **Falar** não aparecer, use o **microfone do teclado** do celular: toque na caixa de texto e depois no ícone de microfone do teclado. Funciona em qualquer campo e é a alternativa mais compatível.
- O ditado só funciona em **contexto seguro**: `https` ou `http://localhost`. No Mac, rode `python3 servir.py` e abra `http://localhost:8000` no Chrome. Em `file://` o microfone pode ser bloqueado, e o `servir.py` na rede Wi-Fi usa `http://IP`, onde o navegador também pode bloquear. Nesses casos, use o **microfone do teclado** ou publique o arquivo em um endereço `https`.
- O aplicativo continua funcionando **offline** para tudo, menos para o ditado quando o navegador exigir internet e para a voz natural Azure quando ela estiver ativada.

## Voz natural (Azure) — opcional

A voz do navegador é gratuita e offline, mas pode soar robótica. Para uma leitura mais natural, o projeto inclui uma voz neural do **Azure Speech** em português do Brasil. Ela é **desligada por padrão**: o app só usa a voz natural depois que você escolhe **Natural (Azure)** em **Mais → Aparência → Motor de voz** e confirma o aviso.

### Privacidade

- Só o **texto da resposta** é enviado ao Azure. A sua **pergunta não é enviada**.
- O catálogo, o histórico e os dados pessoais continuam no celular.
- A chave do Azure fica em `mobile/.env`, no computador, e **nunca** aparece no `index.html`. O servidor bloqueia o download de `.env` e da pasta `.cache`.
- Se a voz natural falhar ou estiver sem internet, o app volta automaticamente para a voz do navegador.
- O `servir.py` é para a **rede local de confiança**. Não exponha a porta na internet: quem acessar a API poderá consumir a sua chave do Azure. Para usar só no próprio computador, rode `python3 servir.py --host 127.0.0.1`.

### Testar sem chave (modo de teste)

O modo de teste valida a interface, o carregamento, o cache, o botão de parar e o fallback, sem gastar chamadas do Azure:

```bash
cd mobile
python3 servir.py
```

Sem `AZURE_SPEECH_KEY`, o servidor inicia em **modo de teste** e o áudio é gerado pelo computador (ou um tom curto, se o sistema não tiver voz). A tela **Aparência** mostra “Modo de teste — sem chave do Azure”. O modo de teste **não** permite avaliar a qualidade da voz Azure.

### Ativar a voz real no Azure

1. Crie um recurso **Speech** no [Portal do Azure](https://portal.azure.com/). Para testar, o plano gratuito **F0** em **Brazil South** é suficiente para começar (0,5 milhão de caracteres neurais por mês e limite de 20 requisições por 60 segundos).
2. Copie a **chave** e a **região** do recurso.
3. Na pasta `mobile`, copie o modelo e preencha:

   ```bash
   cp .env.example .env
   ```

   ```dotenv
   TTS_PROVIDER=azure
   AZURE_SPEECH_KEY=sua-chave-aqui
   AZURE_SPEECH_REGION=brazilsouth
   AZURE_TTS_VOICE=pt-BR-ThalitaNeural
   ```

4. Rode `python3 servir.py` e abra `http://localhost:8000` (ou o endereço do celular mostrado no terminal).
5. Em **Mais → Aparência → Motor de voz**, escolha **Natural (Azure)**, confirme o aviso e toque em **Ouvir teste da voz natural**.

A voz padrão é **Thalita**, feminina. A lista também inclui outras vozes neurais pt-BR, como Macerio, Francisca, Antonio, Brenda e Donato. Para trocar, use o seletor **Voz natural**.

### Variáveis de ambiente

| Variável | Padrão | Para que serve |
|---|---|---|
| `TTS_PROVIDER` | `auto` | `mock` para testar sem chave, `azure` para voz real. Sem valor, usa Azure se houver chave; senão, modo de teste. |
| `AZURE_SPEECH_KEY` | vazio | Chave do recurso Speech. **Não compartilhe nem envie ao Git.** |
| `AZURE_SPEECH_REGION` | `brazilsouth` | Região do recurso. Precisa ser a mesma do portal. |
| `AZURE_TTS_VOICE` | `pt-BR-ThalitaNeural` | Voz neural inicial. |
| `AZURE_TTS_FORMAT` | `audio-24khz-48kbitrate-mono-mp3` | Formato de áudio devolvido pelo Azure. |
| `TTS_CACHE_DIR` | `mobile/.cache/tts` | Pasta do cache de áudios. O cache evita repetir chamadas iguais. |

O servidor limita o texto a **600 caracteres**, valida a voz escolhida, escapa o SSML, usa tempo limite, limita **20 requisições por minuto por IP** e guarda os áudios em cache. O arquivo `.env` e a pasta `.cache/` estão no `.gitignore` local.

### Se a qualidade ainda não bastar

O próximo passo previsto é trocar o adaptador para **Google Cloud Text-to-Speech com Chirp 3 HD** em pt-BR, mantendo a mesma interface. O Google oferece cerca de 1 milhão de caracteres por mês no nível gratuito, mas exige faturamento ativado. A interface do app não muda: basta configurar outro provedor no servidor.

## Dados e privacidade

- Por padrão, tudo fica no **seu celular**, em `localStorage`.
- O app não tem login e não envia o catálogo nem o histórico para servidor nenhum por conta própria.
- A primeira exceção possível é o **ditado por voz**: o navegador pode enviar o áudio a um serviço online do fabricante para transcrever. O app não grava nem guarda áudio; quem controla isso é o navegador.
- A segunda exceção é a **voz natural opcional**: quando ativada, apenas o **texto da resposta** é enviado ao Azure. A pergunta não é enviada. Se você não ativar a voz natural, nada sai do aparelho para a leitura.
- Os links de fonte só abrem quando você toca neles; isso é uma ação sua no navegador.
- Perguntas com **8 ou mais dígitos** ou com **@** são recusadas e **não** entram no histórico, para evitar CPF, telefone ou e-mail.
- O assistente **não é um canal oficial**. Confirme as informações nos canais do governo. Em emergência, ligue **190**; para denúncias, ligue **100**.

### Chaves de armazenamento

| Chave | Conteúdo |
|---|---|
| `citizenassist.servicos.v1` | Catálogo de serviços |
| `citizenassist.historico.v1` | Histórico de atendimentos |
| `citizenassist.prefs.v1` | Tema, tamanho do texto, leitura automática, voz do navegador, motor de voz natural e nota de facilidade |

Para apagar tudo, use **Mais → Restaurar dados de exemplo** ou limpe os dados do site nas configurações do navegador.

## Backup e CSV

- **Mais → Exportar backup completo** gera um JSON com serviços, histórico e preferências.
- **Mais → Importar backup** restaura um JSON gerado pelo próprio app.
- **Mais → Exportar atendimentos em CSV** gera uma planilha com o histórico. O arquivo tem BOM UTF-8 para abrir corretamente no Excel.
- No iPhone, o app tenta usar a folha de compartilhamento; no Android e no computador, faz o download normal.

## Como o app funciona por dentro

O catálogo é uma **lista encadeada implementada no próprio código**, com nós (`No`) e ponteiros (`proximo`), igual à versão Python. As operações principais são:

- `inserir`, `percorrer`, `buscarPorId`, `pesquisar`, `atualizar`, `remover`.
- `ordenarPor` com **Selection Sort**.
- Ordenação auxiliar de categorias e resultados com **Insertion Sort**.
- Busca por pontuação: **+3** para cada palavra-chave encontrada e **+1** para cada palavra da pergunta que aparece no título.
- Confiança **ALTA** a partir de 6 pontos e **MÉDIA** a partir de 3 pontos.
- Normalização de texto sem acentos, com correspondência de palavra inteira.

### Complexidade

| Operação | Complexidade |
|---|---|
| Buscar por ID | O(n) |
| Pesquisar por texto | O(n · m) |
| Inserir / remover | O(n) |
| Ordenar (Selection Sort) | O(n²) |
| Busca por pontuação | O(n · m + r²) |

## Testes da lógica

Com Node.js instalado no computador:

```bash
cd mobile
node teste-logica.js
```

O teste extrai o JavaScript do `index.html`, simula o navegador e verifica lista encadeada, ordenação, busca, privacidade, histórico, CSV, indicadores, voz, motor de voz natural e a renderização das telas. Resultado atual: **78 verificações aprovadas**.

Os testes Python incluem a API de voz natural e o servidor local. Na raiz do projeto:

```bash
python3 -m unittest discover -s testes -t . -v
```

Resultado atual: **141 testes Python aprovados** (60 do sistema DSA + 59 do agente e da avaliação + 22 da voz natural mobile).

## Compatibilidade

- Chrome, Edge, Safari e Firefox modernos (celular ou computador).
- Precisa de JavaScript ativado.
- Funciona offline depois de transferido. O ditado por voz e a voz natural opcional podem precisar de internet, conforme o navegador e a configuração.
- A voz natural exige o servidor local (`python3 servir.py`) e, para a voz Azure real, uma chave configurada no computador. O app aberto direto por `file://` continua usando a voz do navegador.
- O layout é mobile-first e também abre bem no computador.

## Solução de problemas

| Problema | O que fazer |
|---|---|
| Tela em branco | Confirme que o arquivo foi aberto como HTML e que o JavaScript está ativado. |
| “Armazenamento bloqueado” | Modo privado ou `file://` no iOS. Exporte um backup ou use `python3 servir.py`. |
| O celular não abre o endereço do servidor | Confirme a mesma rede Wi-Fi, o IP mostrado e o firewall do computador. |
| CSV não abre | Procure o arquivo em Downloads ou use a folha de compartilhamento. |
| Backup inválido | Use apenas um JSON exportado pelo próprio app. |
| O botão Falar não aparece | O navegador não tem ditado por voz. Use o microfone do teclado do celular. |
| O microfone não funciona | Permita o microfone nas configurações do navegador e abra o app em endereço seguro (`https` ou arquivo local). |
| O ditado diz que o serviço não respondeu ou que precisa de internet | No Safari do Mac, ative o Ditado em Ajustes do Sistema → Teclado → Ditado e permita o microfone. Se ainda falhar, use o Google Chrome ou o Ditado do macOS (clique na caixa de texto e pressione Fn duas vezes). No Chrome, verifique VPN, proxy e firewall. |
| O ditado não entende | Fale mais devagar, em local silencioso, e toque em Tentar de novo. |
| A resposta não é lida em voz alta | Verifique o volume do aparelho e se o navegador tem voz em português instalada. Se estiver usando a voz natural, confira o status em **Aparência → Motor de voz**. |
| A voz natural não aparece ou diz “servidor não encontrado” | Abra o app por `http://localhost:8000` com `python3 servir.py`; em `file://` não existe API de voz natural. O app continua usando a voz do navegador. |
| A voz natural está em “Modo de teste” | Falta `AZURE_SPEECH_KEY` no `mobile/.env`. Preencha a chave e a região e reinicie `python3 servir.py`. |
| O Azure recusou a chave | Confira se a chave e a região são do mesmo recurso Speech. Em **Brazil South**, use `AZURE_SPEECH_REGION=brazilsouth`. |
| “Muitas solicitações” na voz natural | O plano F0 permite 20 requisições por 60 segundos. Aguarde e tente de novo; respostas repetidas usam cache. |
| A voz natural demora ou não toca no iPhone | O navegador pode bloquear áudio automático. Toque em **Ouvir resposta**; se a voz natural falhar, o app volta para a voz do navegador. |
| Porta ocupada | `python3 servir.py --port 8080` ou `--port 0`. |
| Quero voltar aos dados iniciais | **Mais → Restaurar dados de exemplo**. |

## Relação com a versão Python

A versão desktop continua em Python, com menu de terminal, arquivos JSON e testes unitários. A versão mobile é uma reimplementação independente para estudo: não importa os módulos Python, não precisa de Python no celular e mantém os mesmos conceitos de lista encadeada, ordenação, busca por pontuação, histórico, indicadores e CSV.

O CSV mobile inclui uma coluna extra, `nota_facilidade`, para registrar a avaliação de 1 a 5 estrelas feita na tela de indicadores.
