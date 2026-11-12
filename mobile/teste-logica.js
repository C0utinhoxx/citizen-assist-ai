#!/usr/bin/env node

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ARQUIVO = path.join(__dirname, "index.html");
const html = fs.readFileSync(ARQUIVO, "utf8");
const encontrado = html.match(/<script id="app-script">([\s\S]*?)<\/script>/);
if (!encontrado) {
  console.error('Não encontrei o bloco <script id="app-script"> em index.html.');
  process.exit(1);
}
const codigo = encontrado[1];

function criarElemento(tag) {
  const el = {
    tagName: tag || "div",
    _html: "",
    textContent: "",
    value: "",
    files: [],
    children: [],
    firstElementChild: null,
    dataset: {},
    style: { setProperty() {} },
    classList: { add() {}, remove() {}, toggle() {} },
    setAttribute() {},
    getAttribute() { return null; },
    removeAttribute() {},
    addEventListener() {},
    removeChild() {},
    appendChild() {},
    focus() {},
    scrollIntoView() {},
    click() {},
    querySelector() { return criarElemento("div"); },
    querySelectorAll() { return []; },
    closest() { return null; }
  };
  Object.defineProperty(el, "innerHTML", {
    get() { return el._html; },
    set(valor) {
      el._html = valor;
      el.firstElementChild = criarElemento("div");
    }
  });
  return el;
}

const elementos = {};
["view", "sheet-root", "modal-root", "toast-root", "arquivo-import", "form-erro"].forEach((id) => {
  elementos[id] = criarElemento("div");
});

const documento = {
  documentElement: criarElemento("html"),
  body: criarElemento("body"),
  addEventListener() {},
  getElementById(id) { return elementos[id] || null; },
  querySelector() { return null; },
  querySelectorAll() { return []; },
  createElement(tag) { return criarElemento(tag); },
  createEvent() { return { initEvent() {} }; }
};

const armazem = {};
const janela = {
  localStorage: {
    getItem(chave) {
      return Object.prototype.hasOwnProperty.call(armazem, chave) ? armazem[chave] : null;
    },
    setItem(chave, valor) { armazem[chave] = String(valor); },
    removeItem(chave) { delete armazem[chave]; }
  },
  location: { href: "http://localhost/" },
  matchMedia() {
    return { matches: false, addEventListener() {}, addListener() {} };
  },
  scrollTo() {},
  addEventListener() {}
};

const historicoNavegador = {
  state: null,
  pushState(estado) { this.state = estado; },
  replaceState(estado) { this.state = estado; },
  back() {}
};

const contexto = {
  window: janela,
  document: documento,
  history: historicoNavegador,
  navigator: {},
  URL,
  Blob: function () {},
  File: function () {},
  FileReader: function () {},
  setTimeout,
  clearTimeout,
  console,
  Math,
  Date,
  JSON,
  Number,
  String,
  Array,
  Object,
  isFinite,
  Promise,
  RegExp
};

vm.createContext(contexto);
vm.runInContext(codigo, contexto, { filename: "citizen-assist.js" });

let passaram = 0;

function teste(nome, condicao) {
  if (!condicao) throw new Error("FALHOU: " + nome);
  passaram++;
}

function formularioFalso(valores) {
  return {
    elements: {
      id: { value: valores.id },
      titulo: { value: valores.titulo },
      categoria: { value: valores.categoria },
      descricao: { value: valores.descricao },
      documentos: { value: valores.documentos || "" },
      local: { value: valores.local },
      fonte: { value: valores.fonte || "" },
      palavras: { value: valores.palavras || "" },
      verificado: { value: valores.verificado || "" }
    }
  };
}

try {
  teste("carregou os 12 serviços iniciais", contexto.lista.quantidade === 12);
  teste("normalização remove acentos", contexto.normalizar("Saúde") === "saude");
  teste(
    "busca por cartão SUS pontua 7",
    contexto.base.buscar("Como faço o cartão do SUS?")[0][0] === 7
  );
  teste(
    "categorias em ordem alfabética",
    contexto.base.categorias().join("|") ===
      "Direitos e Benefícios|Documentos|Saúde|Transporte"
  );
  teste("pesquisa por saúde retorna 3", contexto.lista.pesquisar("saude").length === 3);
  teste(
    "busca por ID 4",
    contexto.lista.buscarPorId(4).titulo.indexOf("Carteira de Identidade") !== -1
  );

  const novo = new contexto.Servico({
    id: 99,
    titulo: "Teste",
    categoria: "Teste",
    descricao: "Descrição",
    documentos: [],
    local: "Local",
    fonte: "",
    palavras_chave: [],
    verificado_em: ""
  });
  teste("inserir novo serviço", contexto.lista.inserir(novo) === true);
  teste("recusar ID duplicado", contexto.lista.inserir(novo) === false);
  contexto.lista.atualizar(99, { titulo: "Teste atualizado" });
  teste("atualizar serviço", contexto.lista.buscarPorId(99).titulo === "Teste atualizado");
  teste(
    "remover serviço",
    contexto.lista.remover(99) === true && contexto.lista.buscarPorId(99) === null
  );

  contexto.lista.ordenarPor("titulo");
  const titulos = contexto.lista.percorrer().map((s) => contexto.normalizar(s.titulo));
  let ordenado = true;
  for (let i = 1; i < titulos.length; i++) {
    if (titulos[i - 1] > titulos[i]) ordenado = false;
  }
  teste("Selection Sort por título", ordenado);
  contexto.lista.ordenarPor("id");
  teste("Selection Sort por ID", contexto.lista.percorrer()[0].id === 1);

  teste("dado pessoal detectado", contexto.contemDadoPessoal("meu cpf 12345678901") === true);
  teste("e-mail detectado", contexto.contemDadoPessoal("meu email é a@b.com") === true);
  teste("texto normal não é dado pessoal", contexto.contemDadoPessoal("cartão do sus") === false);

  teste("ditado indisponível no simulador", contexto.ditadoSuportado() === false);
  teste("fala indisponível no simulador", contexto.falaSuportada() === false);
  teste(
    "junta texto do ditado",
    contexto.juntarTextoVoz("Como faço", "o cartão do SUS", "e o") === "Como faço o cartão do SUS e o"
  );
  teste(
    "texto para falar inclui título e documentos",
    contexto.textoParaFalar(contexto.lista.buscarPorId(1)).indexOf("Cartão Nacional") !== -1 &&
      contexto.textoParaFalar(contexto.lista.buscarPorId(1)).indexOf("Documentos e requisitos") !== -1
  );
  teste("leitura automática começa desligada", contexto.prefs.lerRespostas === false);
  teste("voz de leitura começa automática", contexto.prefs.vozLeitura === "");
  teste("motor de voz começa no navegador", contexto.prefs.motorVoz === "navegador");
  teste("voz natural começa na Thalita", contexto.prefs.vozNatural === "pt-BR-ThalitaNeural");
  teste("simulador não tem áudio", contexto.audioSuportado() === false);
  teste(
    "status da voz natural fica offline sem servidor",
    contexto.ttsStatus.carregado === true && contexto.ttsStatus.pronto === false
  );
  teste(
    "nome da voz natural mostra o gênero",
    contexto.nomeVozNatural("pt-BR-ThalitaNeural") === "Thalita (feminina)"
  );
  teste("simulador não tem vozes em português", contexto.vozesPortugues().length === 0 && contexto.vozEscolhida() === null);
  teste(
    "nome da voz mostra o idioma",
    contexto.nomeCurtoVoz({ name: "Luciana", lang: "pt-BR" }) === "Luciana (pt-BR)"
  );

  const vozesFalsas = [
    { name: "Luciana", lang: "pt-BR", voiceURI: "luciana", localService: true },
    { name: "Google português do Brasil", lang: "pt-BR", voiceURI: "google", localService: false },
    { name: "Luciana (Enhanced)", lang: "pt-BR", voiceURI: "luciana-enhanced", localService: true },
    { name: "Alex", lang: "en-US", voiceURI: "alex", localService: true }
  ];
  let falaCriada = null;
  janela.speechSynthesis = {
    getVoices() { return vozesFalsas; },
    speak(fala) { falaCriada = fala; },
    cancel() {}
  };
  janela.SpeechSynthesisUtterance = function (texto) { this.text = texto; };
  teste("filtra vozes em português", contexto.vozesPortugues().length === 3);
  teste("voz natural tem prioridade", contexto.vozEscolhida().name === "Luciana (Enhanced)");
  contexto.prefs.vozLeitura = "luciana-enhanced";
  teste("voz escolhida é respeitada", contexto.vozEscolhida().name === "Luciana (Enhanced)");
  teste(
    "leitura usa a voz escolhida",
    contexto.falarTexto("teste") === true &&
      falaCriada.voice.name === "Luciana (Enhanced)" &&
      falaCriada.lang === "pt-BR"
  );
  contexto.prefs.vozLeitura = "";
  delete janela.speechSynthesis;
  delete janela.SpeechSynthesisUtterance;

  let chamadaTTS = null;
  contexto.fetch = function (url, opcoes) {
    chamadaTTS = { url: url, opcoes: opcoes };
    return new Promise(function () {});
  };
  contexto.prefs.motorVoz = "natural";
  contexto.ttsStatus.pronto = true;
  contexto.ttsStatus.modo = "teste";
  teste(
    "voz natural envia só o texto da resposta",
    contexto.falarTexto("Olá, cidadão") === true &&
      chamadaTTS !== null &&
      chamadaTTS.url === "/api/tts" &&
      JSON.parse(chamadaTTS.opcoes.body).texto === "Olá, cidadão" &&
      JSON.parse(chamadaTTS.opcoes.body).voz === contexto.prefs.vozNatural
  );
  teste(
    "pedido de voz natural não inclui a pergunta",
    Object.keys(JSON.parse(chamadaTTS.opcoes.body)).sort().join(",") === "texto,voz"
  );
  teste("voz natural fica carregando enquanto busca o áudio", contexto.voz.ttsCarregando === true);
  contexto.pararFala();
  teste("parar fala cancela o carregamento", contexto.voz.ttsCarregando === false);
  contexto.prefs.vozNatural = "pt-BR-ThalitaNeural";
  const chaveThalita = contexto.chaveCacheNatural("Olá");
  contexto.prefs.vozNatural = "pt-BR-MacerioNeural";
  teste("cache da voz natural separa as vozes", contexto.chaveCacheNatural("Olá") !== chaveThalita);
  contexto.prefs.vozNatural = "pt-BR-ThalitaNeural";
  contexto.prefs.motorVoz = "navegador";
  contexto.ttsStatus.pronto = false;
  delete contexto.fetch;

  teste("simulador não é Safari", contexto.navegadorPareceSafari() === false);
  teste("simulador não é Mac", contexto.pareceMac() === false);
  teste(
    "erro de rede sugere o Chrome",
    contexto.mensagemErroVoz("network").indexOf("Chrome") !== -1
  );
  teste(
    "erro sem fala sugere tentar de novo",
    contexto.mensagemErroVoz("no-speech").indexOf("Tentar de novo") !== -1
  );

  contexto.perguntar("Como faço o cartão do SUS?");
  teste("resposta encontrada", contexto.ultimaResposta.tipo === "encontrada");
  teste("confiança alta", contexto.ultimaResposta.confianca === "ALTA");
  teste("registro no histórico", contexto.historico.length === 1);
  contexto.responderAjuda(true);
  teste("feedback salvo", contexto.historico[0].ajudou === true);

  contexto.perguntar("assunto inexistente xyz");
  teste("resposta não encontrada", contexto.ultimaResposta.tipo === "nao-encontrada");
  teste("histórico com 2 registros", contexto.historico.length === 2);

  const antesDaPrivacidade = contexto.historico.length;
  contexto.perguntar("meu cpf é 12345678901");
  teste("pergunta com dado pessoal é recusada", contexto.ultimaResposta.tipo === "privacidade");
  teste("pergunta privada não entra no histórico", contexto.historico.length === antesDaPrivacidade);

  const csv = contexto.gerarCSV();
  teste("CSV com cabeçalho", csv.indexOf("data,origem,pergunta") !== -1);
  teste("CSV com pergunta", csv.indexOf("cartão do SUS") !== -1);
  teste("CSV com BOM UTF-8", csv.charCodeAt(0) === 0xfeff);

  const indicadores = contexto.calcularIndicadores();
  teste("indicadores: total 2", indicadores.total === 2);
  teste("indicadores: encontrados 1", indicadores.encontrados === 1);

  ["home", "servicos", "assistente", "categorias", "mais", "analise", "indicadores", "historico", "aparencia", "sobre"].forEach((tela) => {
    contexto.state.screen = tela;
    contexto.state.params = {};
    contexto.render();
    teste("renderiza " + tela, elementos.view.innerHTML.length > 0);
  });

  contexto.state.screen = "assistente";
  contexto.state.params = {};
  contexto.render();
  teste(
    "assistente orienta o microfone do teclado sem ditado",
    elementos.view.innerHTML.indexOf("microfone do teclado") !== -1
  );
  teste("assistente tem botão grande Perguntar", elementos.view.innerHTML.indexOf("btn-lg") !== -1);

  contexto.state.screen = "aparencia";
  contexto.render();
  teste(
    "aparência tem leitura em voz alta",
    elementos.view.innerHTML.indexOf("Leitura em voz alta") !== -1
  );
  teste(
    "aparência tem escolha do motor de voz",
    elementos.view.innerHTML.indexOf("Motor de voz") !== -1 &&
      elementos.view.innerHTML.indexOf("Natural (Azure)") !== -1
  );
  teste(
    "aparência mantém a voz do navegador",
    elementos.view.innerHTML.indexOf("Voz do navegador (offline)") !== -1
  );

  contexto.state.screen = "categoria";
  contexto.state.params = { categoria: "Saúde" };
  contexto.render();
  teste("renderiza categoria", elementos.view.innerHTML.indexOf("Saúde") !== -1);

  contexto.abrirDetalhe(1);
  teste("abre detalhe", elementos["sheet-root"].innerHTML.indexOf("Cartão Nacional") !== -1);
  contexto.fecharSheet();

  contexto.abrirFormulario(null);
  teste("abre formulário", elementos["sheet-root"].innerHTML.indexOf("Novo serviço") !== -1);
  contexto.fecharSheet();

  contexto.state.screen = "servicos";
  contexto.state.params = {};
  contexto.salvarFormulario(
    formularioFalso({
      id: "50",
      titulo: "Serviço de teste",
      categoria: "Teste",
      descricao: "Descrição do teste",
      documentos: "Documento A\nDocumento B",
      local: "Local de teste",
      fonte: "https://example.com",
      palavras: "teste, exemplo",
      verificado: "2026-11-09"
    }),
    null
  );
  const criado = contexto.lista.buscarPorId(50);
  teste("formulário cria serviço", criado !== null && criado.documentos.length === 2);
  teste("formulário salva palavras-chave", criado.palavras_chave.length === 2);

  contexto.salvarFormulario(
    formularioFalso({
      id: "50",
      titulo: "Serviço editado",
      categoria: "Teste",
      descricao: "Descrição editada",
      documentos: "Documento A",
      local: "Local editado",
      fonte: "",
      palavras: "teste",
      verificado: "2026-11-09"
    }),
    50
  );
  teste("formulário edita serviço", contexto.lista.buscarPorId(50).titulo === "Serviço editado");
  contexto.lista.remover(50);
  contexto.salvarServicos();

  contexto.go("servicos");
  teste("navegação muda de tela", contexto.state.screen === "servicos");
  contexto.go("home");
  teste("navegação volta para home", contexto.state.screen === "home");

  contexto.historyOk = false;
  contexto.pilha = [
    { tela: "home", params: {} },
    { tela: "servicos", params: {} }
  ];
  contexto.state.screen = "servicos";
  contexto.state.params = {};
  contexto.voltar();
  teste("voltar usa a pilha quando não há histórico", contexto.state.screen === "home");

  console.log("OK — " + passaram + " verificações passaram.");
} catch (erro) {
  console.error(String(erro && erro.message ? erro.message : erro));
  process.exitCode = 1;
}
