"""Busca por pontuação nas fichas, sem bibliotecas externas.

A busca é propositalmente simples e explicável:

- palavra-chave da ficha encontrada na pergunta: +6;
- palavra-chave da seção encontrada na pergunta: +6;
- palavra do assunto da pergunta no título da seção: +3;
- palavra do assunto no texto da seção: +1.

Uma seção só entra no resultado se a pergunta tiver uma âncora de assunto
(uma palavra que realmente aparece nas fichas). Isso evita responder
"R$ 38,00" para uma pergunta sobre passaporte só porque a palavra
"quanto custa" aparece em uma ficha.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from app.texto import contem_palavra, normalizar

from .fichas import Ficha, Secao
from .seguranca import PALAVRAS_GENERICAS

PONTOS_PALAVRA_CHAVE_FICHA = 6
PONTOS_PALAVRA_CHAVE_SECAO = 6
PONTOS_TITULO = 3
PONTOS_TEXTO = 1
PONTOS_MINIMOS = 3


@dataclass
class Ocorrencia:
    """Uma seção que pode responder à pergunta."""

    ficha: Ficha
    secao: Secao
    pontos: int

    @property
    def referencia(self) -> str:
        return f"{self.ficha.id} — {self.secao.titulo_exibicao}"


@dataclass
class _SecaoIndexada:
    ficha: Ficha
    secao: Secao
    titulo_tokens: set
    texto_tokens: set
    chaves: List[str]


class Recuperador:
    """Índice em memória das fichas."""

    def __init__(self, fichas: Dict[str, Ficha]):
        self.fichas = fichas
        self._indice: List[_SecaoIndexada] = []
        self._vocabulario = set(PALAVRAS_GENERICAS)

        for ficha in fichas.values():
            self._vocabulario.update(ficha.vocabulario())
            for secao in ficha.secoes:
                titulo_tokens = set(normalizar(secao.titulo_exibicao).split())
                texto_tokens = set(normalizar(secao.texto).split())
                self._indice.append(
                    _SecaoIndexada(
                        ficha=ficha,
                        secao=secao,
                        titulo_tokens=titulo_tokens,
                        texto_tokens=texto_tokens,
                        chaves=[normalizar(k) for k in secao.palavras_chave],
                    )
                )
                self._vocabulario.update(titulo_tokens)
                self._vocabulario.update(texto_tokens)

    @property
    def vocabulario(self) -> set:
        return set(self._vocabulario)

    def _tokens_de_assunto(self, pergunta: str) -> List[str]:
        tokens = normalizar(pergunta).split()
        return [
            token
            for token in tokens
            if len(token) >= 3 and token not in PALAVRAS_GENERICAS
        ]

    def buscar(self, pergunta: str, limite: int = 8) -> List[Ocorrencia]:
        """Devolve as ocorrências mais prováveis, da maior para a menor."""
        if not normalizar(pergunta):
            return []

        tokens_assunto = self._tokens_de_assunto(pergunta)
        ocorrencias: List[Ocorrencia] = []

        for item in self._indice:
            ficha = item.ficha
            secao = item.secao

            pontos = 0
            for palavra in ficha.palavras_chave:
                if contem_palavra(pergunta, normalizar(palavra)):
                    pontos += PONTOS_PALAVRA_CHAVE_FICHA

            for chave in item.chaves:
                if contem_palavra(pergunta, chave):
                    pontos += PONTOS_PALAVRA_CHAVE_SECAO

            for token in tokens_assunto:
                if token in item.chaves:
                    pontos += PONTOS_TITULO
                if token in item.titulo_tokens:
                    pontos += PONTOS_TITULO
                if token in item.texto_tokens:
                    pontos += PONTOS_TEXTO

            if pontos < PONTOS_MINIMOS:
                continue

            # Âncora: a pergunta precisa falar de algo que existe nesta ficha.
            # Sem isso, "quanto custa o passaporte?" casaria com "quanto custa"
            # de uma ficha de RG e produziria uma resposta errada.
            tem_ancora = any(
                token in ficha.vocabulario() for token in tokens_assunto
            ) or any(
                contem_palavra(pergunta, normalizar(palavra))
                for palavra in ficha.palavras_chave
            )
            if not tem_ancora:
                continue

            ocorrencias.append(Ocorrencia(ficha, secao, pontos))

        ocorrencias.sort(
            key=lambda o: (-o.pontos, o.ficha.id, o.secao.titulo_exibicao)
        )

        # Remove seções repetidas mantendo a melhor pontuação.
        vistos = set()
        unicas: List[Ocorrencia] = []
        for ocorrencia in ocorrencias:
            chave = (ocorrencia.ficha.id, ocorrencia.secao.titulo_exibicao)
            if chave in vistos:
                continue
            vistos.add(chave)
            unicas.append(ocorrencia)
            if len(unicas) >= limite:
                break

        return unicas

    def selecionar_contexto(
        self, ocorrencias: Sequence[Ocorrencia], maximo: int = 3
    ) -> List[Ocorrencia]:
        """Escolhe as seções que entram na resposta.

        Regra: mantém a melhor seção e as que empataram com ela. Assim a
        resposta fica curta e não mistura, por exemplo, o preço do RG com o
        preço da certidão só porque as duas seções falam em "segunda via".
        Empates acontecem em perguntas que realmente precisam de duas seções,
        como "perdi o RG: preciso de boletim?".
        """
        if not ocorrencias:
            return []

        melhor = ocorrencias[0].pontos
        escolhidas: List[Ocorrencia] = []
        por_ficha: Dict[str, int] = {}

        for ocorrencia in ocorrencias:
            if ocorrencia.pontos < melhor:
                break
            if por_ficha.get(ocorrencia.ficha.id, 0) >= 2:
                continue
            escolhidas.append(ocorrencia)
            por_ficha[ocorrencia.ficha.id] = por_ficha.get(ocorrencia.ficha.id, 0) + 1
            if len(escolhidas) >= maximo:
                break

        return escolhidas

    def fichas_citadas(self, ocorrencias: Iterable[Ocorrencia]) -> List[str]:
        vistas: List[str] = []
        for ocorrencia in ocorrencias:
            if ocorrencia.ficha.id not in vistas:
                vistas.append(ocorrencia.ficha.id)
        return vistas
