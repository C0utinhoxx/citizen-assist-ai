"""Camada de segurança do agente.

Responsabilidades:

- detectar e ocultar dados pessoais (CPF, RG, CNH, título, telefone, e-mail,
  endereço e números longos);
- detectar tentativas de prompt injection;
- recusar entradas vazias, muito longas ou sem sentido;
- nunca guardar a pergunta original.

A pergunta é tratada como **dado**, nunca como instrução. As regras do
agente vêm apenas do código e das fichas FC-01 a FC-07.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Set

from app.texto import normalizar

LIMITE_CARACTERES = 500
MINIMO_CARACTERES = 2

PADROES_PII = [
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", re.IGNORECASE)),
    ("cpf", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")),
    ("telefone", re.compile(
        r"(?:\+?55[\s-]?)?(?:\(?\d{2}\)?[\s-]?)?9?\d{4}[\s-]?\d{4}\b"
    )),
    ("cep", re.compile(r"\b\d{5}-\d{3}\b")),
    ("numero_longo", re.compile(r"\b\d{8,}\b")),
    ("documento_com_pontos", re.compile(
        r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dXx]\b"
    )),
]

FRASES_PII = [
    r"\bmeu\s+nome\b",
    r"\bmeu\s+(telefone|endereco|e-?mail|pis|nis)\b",
    r"\bmeus\s+dados\b",
    r"\bmeu\s+endereco\s+e\s+telefone\b",
    r"\bvou\s+(te\s+)?passar\s+(meu|meus)\b",
    r"\bmoro\s+na\s+(rua|avenida|travessa|alameda)\b",
]

PADROES_INJECAO = [
    r"\bignore\s+(as\s+)?instru",
    r"\bignore\s+(all\s+)?(previous|above)\s+instructions?\b",
    r"\bdesconsidere\s+(as\s+)?instru",
    r"\besqueca\s+(as\s+)?instru",
    r"\bprompt\s+(de\s+)?sistema\b",
    r"\bsystem\s+prompt\b",
    r"\brevele?\s+(seu|as|o)\s+(prompt|instru)",
    r"\bmostre\s+(seu|as|o)\s+(prompt|instru)",
    r"\[sistema\]",
    r"\bnova\s+regra\b",
    r"\bnovas?\s+instru",
    r"\bvoce\s+agora\s+(e|sera)\b",
    r"\bfinja\s+(que|ser)\b",
    r"\bmodo\s+(desenvolvedor|dev|admin|administrador)\b",
    r"\bjailbreak\b",
    r"\boverride\b",
    r"\baja\s+como\b",
    r"\bpretenda\s+ser\b",
    r"\bsuas\s+instru",
    r"\bregras?\s+anteriores\b",
    r"\ba\s+partir\s+de\s+agora\b",
    r"\bdesative\s+(as\s+)?regras\b",
    r"\bmodo\s+sem\s+restric",
]

PADROES_LIMITACAO = [
    r"\bcanal\s+oficial\b",
    r"\bvoce\s+e\s+(o\s+)?canal\b",
    r"\bassistente\s+oficial\b",
    r"\bprototipo\b",
    r"\bquem\s+e\s+voce\b",
    r"\bvoce\s+e\s+um\s+robo\b",
]

_RE_PII = [(nome, padrao) for nome, padrao in PADROES_PII]
_RE_FRASES_PII = [re.compile(padrao, re.IGNORECASE) for padrao in FRASES_PII]
_RE_INJECAO = [re.compile(padrao, re.IGNORECASE) for padrao in PADROES_INJECAO]
_RE_LIMITACAO = [re.compile(padrao, re.IGNORECASE) for padrao in PADROES_LIMITACAO]

PALAVRAS_GENERICAS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "por", "para", "pra", "com", "sem",
    "e", "ou", "que", "se", "como", "qual", "quais", "quando", "onde",
    "quanto", "quantos", "quanta", "quantas", "quem", "porque", "por",
    "eu", "me", "meu", "minha", "meus", "minhas", "voce", "voces",
    "posso", "pode", "preciso", "precisa", "tenho", "tem", "faco", "fazer",
    "faz", "tirar", "tiro", "pegar", "levar", "levo", "ir", "vou",
    "custa", "custo", "valor", "taxa", "paga", "pago", "gratuito",
    "gratuita", "demora", "tempo", "prazo", "documentos", "documento",
    "necessario", "necessaria", "obrigatorio", "obrigatoria", "sim", "nao",
    "e", "sao", "ser", "esta", "estou", "aqui", "ali", "isso", "isto",
    "mais", "menos", "muito", "pouco", "ja", "ainda", "tambem", "so",
    "sobre", "atendimento", "atendem", "atende", "falar", "fala",
    "ola", "oi", "bom", "boa", "dia", "tarde", "noite", "ajuda",
    "informacao", "informacoes", "duvida", "pergunta", "gostaria",
}


@dataclass


class AnaliseEntrada:
    """Resultado da análise de segurança de uma pergunta."""

    tipo: str
    motivo: str = ""
    texto_seguro: str = ""
    pii: List[str] = field(default_factory=list)
    injecao: bool = False

    @property
    def bloqueada(self) -> bool:
        return self.tipo != "ok"


def contem_pii(texto: str) -> bool:
    """True quando o texto contém um dado pessoal reconhecível."""
    if not texto:
        return False
    for _, padrao in _RE_PII:
        if padrao.search(texto):
            return True
    return any(padrao.search(texto) for padrao in _RE_FRASES_PII)


def mascarar_pii(texto: str) -> str:
    """Substitui dados pessoais por um marcador, sem repetir o valor."""
    seguro = texto or ""
    for _, padrao in _RE_PII:
        seguro = padrao.sub("[dado pessoal ocultado]", seguro)
    for padrao in _RE_FRASES_PII:
        seguro = padrao.sub("[dado pessoal ocultado]", seguro)
    return seguro


def contem_injecao(texto: str) -> bool:
    """True quando há indício de prompt injection."""
    if not texto:
        return False
    normalizado = normalizar(texto)
    minusculo = texto.lower()
    return any(
        padrao.search(normalizado) or padrao.search(minusculo)
        for padrao in _RE_INJECAO
    )


def contem_limitacao(texto: str) -> bool:
    """True quando a pessoa pergunta se o assistente é um canal oficial."""
    if not texto:
        return False
    normalizado = normalizar(texto)
    return any(padrao.search(normalizado) for padrao in _RE_LIMITACAO)


class Seguranca:
    """Analisa a entrada antes de qualquer busca ou chamada ao modelo."""

    def __init__(self, vocabulario: Optional[Iterable[str]] = None):
        self.vocabulario: Set[str] = set(vocabulario or ())
        self.vocabulario.update(PALAVRAS_GENERICAS)

    def _parece_sem_sentido(self, texto: str) -> bool:
        normalizado = normalizar(texto)
        tokens = [t for t in normalizado.split() if len(t) >= 3]
        if not tokens:
            return True

        conhecidos = sum(1 for t in tokens if t in self.vocabulario)
        if conhecidos == 0:
            return True

        simbolos = len(re.findall(r"[^\w\s]", texto))
        if simbolos >= 5 and conhecidos <= 1:
            return True

        if re.search(r"(.)\1{4,}", texto):
            return True

        return False

    def analisar(self, pergunta: str) -> AnaliseEntrada:
        """Classifica a pergunta e devolve uma versão mascarada."""
        original = (pergunta or "").strip()
        seguro = mascarar_pii(original)

        if not original:
            return AnaliseEntrada("vazia", "a mensagem está vazia", seguro)

        if len(original) < MINIMO_CARACTERES:
            return AnaliseEntrada("curta", "a mensagem é curta demais", seguro)

        if len(original) > LIMITE_CARACTERES:
            return AnaliseEntrada(
                "longa",
                f"a mensagem passa de {LIMITE_CARACTERES} caracteres",
                seguro,
            )

        if contem_pii(original):
            return AnaliseEntrada(
                "dados_pessoais",
                "a mensagem contém um dado pessoal",
                seguro,
                pii=["dado pessoal"],
            )

        if contem_injecao(original):
            return AnaliseEntrada(
                "injecao",
                "a mensagem tenta alterar as regras do assistente",
                seguro,
                injecao=True,
            )

        if contem_limitacao(original):
            return AnaliseEntrada(
                "limitacao",
                "a mensagem pergunta sobre o papel do assistente",
                seguro,
            )

        if self._parece_sem_sentido(original):
            return AnaliseEntrada(
                "invalida",
                "não foi possível entender a mensagem",
                seguro,
            )

        return AnaliseEntrada("ok", texto_seguro=seguro)
