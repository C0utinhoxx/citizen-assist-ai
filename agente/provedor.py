"""Acesso opcional a um modelo de linguagem.

O agente funciona em dois modos:

- ``extrativo`` (padrão sem chave): monta a resposta diretamente das seções
  das fichas. É determinístico, offline e serve para testes e demonstração.
- ``llm``: usa um provedor compatível com a API OpenAI (Groq, OpenAI ou
  Ollama local). O modelo recebe apenas o contexto recuperado das fichas e
  deve responder exclusivamente com base nele.

Nenhuma chave é gravada no código. A configuração é lida de variáveis de
ambiente ou do arquivo ``agente/.env`` (ignorado pelo Git).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict, Optional

PASTA_AGENTE = os.path.dirname(__file__)
CAMINHO_ENV = os.path.join(PASTA_AGENTE, ".env")
TEMPO_LIMITE = 60


class ErroProvedor(RuntimeError):
    """Falha de configuração, rede ou resposta do provedor de LLM."""


def carregar_env(caminho: str = CAMINHO_ENV) -> None:
    """Carrega pares KEY=VALUE sem sobrescrever variáveis já definidas."""
    if not os.path.exists(caminho):
        return

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            chave = chave.strip()
            valor = valor.strip().strip('"').strip("'")
            if chave and chave not in os.environ:
                os.environ[chave] = valor


@dataclass
class ConfiguracaoLLM:
    provedor: str
    modelo: str
    base_url: str
    chave: str

    @property
    def descricao(self) -> str:
        return f"{self.provedor}:{self.modelo}"


class Provedor:
    """Interface mínima de um modelo de linguagem."""

    nome = "base"

    def gerar(self, sistema: str, usuario: str) -> str:
        raise NotImplementedError


class ProvedorOpenAICompat(Provedor):
    """Cliente HTTP para APIs compatíveis com ``/chat/completions``."""

    def __init__(self, configuracao: ConfiguracaoLLM):
        self.configuracao = configuracao
        self.nome = configuracao.descricao

    def gerar(self, sistema: str, usuario: str) -> str:
        corpo = {
            "model": self.configuracao.modelo,
            "messages": [
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario},
            ],
            "temperature": 0,
        }
        dados = json.dumps(corpo).encode("utf-8")
        url = self.configuracao.base_url.rstrip("/") + "/chat/completions"

        cabecalhos = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.configuracao.chave:
            cabecalhos["Authorization"] = f"Bearer {self.configuracao.chave}"

        requisicao = urllib.request.Request(
            url, data=dados, headers=cabecalhos, method="POST"
        )

        try:
            with urllib.request.urlopen(requisicao, timeout=TEMPO_LIMITE) as resposta:
                conteudo = resposta.read().decode("utf-8")
        except urllib.error.HTTPError as erro:
            detalhe = erro.read().decode("utf-8", "ignore")[:300]
            raise ErroProvedor(
                f"O provedor respondeu HTTP {erro.code}: {detalhe}"
            ) from erro
        except (urllib.error.URLError, TimeoutError, OSError) as erro:
            raise ErroProvedor(f"Não foi possível falar com o provedor: {erro}") from erro

        try:
            resposta = json.loads(conteudo)
            texto = resposta["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as erro:
            raise ErroProvedor("Resposta do provedor em formato inesperado.") from erro

        texto = (texto or "").strip()
        if not texto:
            raise ErroProvedor("O provedor devolveu uma resposta vazia.")
        return texto


PROVEDORES = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "modelo": "llama-3.1-8b-instant",
        "chave_env": "GROQ_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "modelo": "gpt-4o-mini",
        "chave_env": "OPENAI_API_KEY",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "modelo": "llama3.1",
        "chave_env": "",
    },
}


def _criar_configuracao(nome: str) -> Optional[ConfiguracaoLLM]:
    dados = PROVEDORES.get(nome)
    if not dados:
        return None

    chave = os.environ.get(dados["chave_env"], "") if dados["chave_env"] else ""
    if dados["chave_env"] and not chave:
        return None

    return ConfiguracaoLLM(
        provedor=nome,
        modelo=os.environ.get("CITIZEN_LLM_MODEL", dados["modelo"]),
        base_url=os.environ.get("CITIZEN_LLM_BASE_URL", dados["base_url"]),
        chave=chave,
    )


def criar_provedor() -> Optional[Provedor]:
    """Cria o provedor configurado ou devolve None para o modo extrativo."""
    carregar_env()

    escolhido = os.environ.get("CITIZEN_LLM_PROVIDER", "auto").strip().lower()

    if escolhido in ("extrativo", "nenhum", "none", "offline"):
        return None

    if escolhido == "auto":
        for candidato in ("groq", "openai", "ollama"):
            configuracao = _criar_configuracao(candidato)
            if configuracao:
                # Ollama é local: só é usado quando o modelo foi escolhido
                # explicitamente, para não tentar rede sem necessidade.
                if candidato == "ollama" and not os.environ.get("CITIZEN_LLM_MODEL"):
                    continue
                return ProvedorOpenAICompat(configuracao)
        return None

    configuracao = _criar_configuracao(escolhido)
    if configuracao is None:
        raise ErroProvedor(
            f"Provedor '{escolhido}' sem configuração. "
            "Defina a chave ou use CITIZEN_LLM_PROVIDER=extrativo."
        )

    return ProvedorOpenAICompat(configuracao)


def descrever_configuracao() -> Dict[str, str]:
    """Resumo sem segredos, para exibir no terminal e na documentação."""
    carregar_env()
    escolhido = os.environ.get("CITIZEN_LLM_PROVIDER", "auto").strip().lower()
    if escolhido in ("extrativo", "nenhum", "none", "offline"):
        return {"modo": "extrativo", "detalhe": "sem LLM configurado"}
    if escolhido == "auto":
        return {"modo": "auto", "detalhe": "usa chave disponível, se houver"}
    return {"modo": escolhido, "detalhe": "configurado"}
