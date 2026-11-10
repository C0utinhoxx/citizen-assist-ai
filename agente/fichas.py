"""Carregamento e validação das fichas de referência FC-01 a FC-07.

Formato aceito (Markdown simples):

    # FC-01 — Título da ficha

    - **Fonte:** ...
    - **Data de verificação:** ...
    - **Palavras-chave:** rg, identidade, segunda via

    ## Nome da seção | palavra-chave 1, palavra-chave 2
    Texto da seção.

O trecho depois de ``|`` no título é opcional e serve para melhorar a busca.
A ficha é a única fonte de verdade do agente. O carregador não completa
lacunas e não inventa conteúdo.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from app.texto import normalizar

PASTA_PADRAO = os.path.join(os.path.dirname(__file__), "fichas")
IDS_OBRIGATORIOS = ("FC-01", "FC-02", "FC-03", "FC-04", "FC-05", "FC-06", "FC-07")

_METADADO = re.compile(r"^-\s*\*\*(?P<chave>[^*]+)\*\*\s*:?\s*(?P<valor>.*)$")
_SECAO = re.compile(r"^##\s+(?P<titulo>.+)$")


@dataclass
class Secao:
    """Uma seção temática de uma ficha."""

    titulo: str
    texto: str
    palavras_chave: List[str] = field(default_factory=list)

    @property
    def titulo_exibicao(self) -> str:
        return self.titulo.split("|", 1)[0].strip()


@dataclass
class Ficha:
    """Uma ficha de referência completa."""

    id: str
    titulo: str
    arquivo: str
    fonte: str
    verificado_em: str
    palavras_chave: List[str]
    secoes: List[Secao]
    provisoria: bool = False

    def texto_completo(self) -> str:
        partes = [self.titulo, " ".join(self.palavras_chave)]
        partes.extend(secao.texto for secao in self.secoes)
        return "\n".join(partes)

    def vocabulario(self) -> set:
        texto = self.texto_completo().lower()
        return set(normalizar(texto).split())

    def resumo(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fonte": self.fonte,
            "verificado_em": self.verificado_em,
            "provisoria": self.provisoria,
        }


class ErroFicha(ValueError):
    """Indica uma ficha ausente ou fora do formato mínimo."""


def _separar_palavras(valor: str) -> List[str]:
    return [
        parte.strip()
        for parte in re.split(r"[,;]", valor or "")
        if parte.strip()
    ]


def _limpar_corpo(linhas: Iterable[str]) -> str:
    """Remove citações de status e espaços sobrando do corpo da seção."""
    uteis = []
    for linha in linhas:
        if linha.lstrip().startswith(">"):
            continue
        uteis.append(linha.rstrip())

    texto = "\n".join(uteis).strip()
    return re.sub(r"\n{3,}", "\n\n", texto)


def carregar_ficha(caminho: str) -> Ficha:
    """Lê um arquivo Markdown e devolve uma ``Ficha`` validada."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.read().splitlines()

    if not linhas or not linhas[0].startswith("# "):
        raise ErroFicha(f"{caminho}: a primeira linha deve ser '# FC-XX — Título'.")

    cabecalho = linhas[0][2:].strip()
    if "—" in cabecalho:
        identificador, titulo = cabecalho.split("—", 1)
    elif "-" in cabecalho:
        identificador, titulo = cabecalho.split("-", 1)
    else:
        raise ErroFicha(f"{caminho}: cabeçalho sem identificador FC-XX.")

    identificador = identificador.strip().upper()
    titulo = titulo.strip()

    metadados: Dict[str, str] = {}
    secoes: List[Secao] = []
    secao_atual: Optional[str] = None
    chaves_atuais: List[str] = []
    corpo: List[str] = []

    def fechar_secao() -> None:
        if secao_atual is not None:
            texto = _limpar_corpo(corpo)
            if texto:
                secoes.append(
                    Secao(
                        titulo=secao_atual,
                        texto=texto,
                        palavras_chave=chaves_atuais,
                    )
                )

    for linha in linhas[1:]:
        encontrada = _SECAO.match(linha)
        if encontrada:
            fechar_secao()
            bruto = encontrada.group("titulo").strip()
            if "|" in bruto:
                nome, chaves = bruto.split("|", 1)
                secao_atual = nome.strip()
                chaves_atuais = _separar_palavras(chaves)
            else:
                secao_atual = bruto
                chaves_atuais = []
            corpo = []
            continue

        if secao_atual is None:
            meta = _METADADO.match(linha.strip())
            if meta:
                chave = normalizar(meta.group("chave"))
                metadados[chave] = meta.group("valor").strip()
            continue

        corpo.append(linha)

    fechar_secao()

    fonte = metadados.get("fonte", "").strip()
    verificado = metadados.get(
        "data de verificacao", metadados.get("verificado em", "")
    ).strip()
    palavras = _separar_palavras(metadados.get("palavras chave", ""))

    if not re.match(r"^FC-\d{2}$", identificador):
        raise ErroFicha(f"{caminho}: identificador inválido: {identificador}")
    if not titulo:
        raise ErroFicha(f"{caminho}: título vazio.")
    if not fonte:
        raise ErroFicha(f"{caminho}: metadado 'Fonte' obrigatório.")
    if not verificado:
        raise ErroFicha(
            f"{caminho}: metadado 'Data de verificação' obrigatório."
        )
    if not secoes:
        raise ErroFicha(f"{caminho}: a ficha não tem nenhuma seção '##'.")

    provisoria = "provis" in normalizar(titulo + " " + fonte + " " + verificado)
    if not provisoria:
        # O aviso de status fica no topo, antes da primeira seção.
        provisoria = any(
            "provis" in normalizar(linha)
            for linha in linhas[:12]
        )

    return Ficha(
        id=identificador,
        titulo=titulo,
        arquivo=os.path.basename(caminho),
        fonte=fonte,
        verificado_em=verificado,
        palavras_chave=palavras,
        secoes=secoes,
        provisoria=provisoria,
    )


def carregar_fichas(pasta: str = PASTA_PADRAO) -> Dict[str, Ficha]:
    """Carrega todas as fichas da pasta e valida a presença das sete."""
    if not os.path.isdir(pasta):
        raise ErroFicha(f"Pasta de fichas não encontrada: {pasta}")

    fichas: Dict[str, Ficha] = {}
    for nome in sorted(os.listdir(pasta)):
        if not nome.lower().endswith(".md"):
            continue
        if not nome.upper().startswith("FC-"):
            continue

        ficha = carregar_ficha(os.path.join(pasta, nome))
        if ficha.id in fichas:
            raise ErroFicha(f"Ficha duplicada: {ficha.id}")
        fichas[ficha.id] = ficha

    faltando = [fid for fid in IDS_OBRIGATORIOS if fid not in fichas]
    if faltando:
        raise ErroFicha(
            "Fichas obrigatórias ausentes: " + ", ".join(faltando)
        )

    return fichas
