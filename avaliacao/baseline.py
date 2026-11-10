"""Versão "antes da melhoria" usada apenas na comparação do Golden Dataset.

Esta versão é didática: ela simula um primeiro protótipo ingênuo, com busca
por primeira palavra-chave e sem citação, aviso, validação ou proteção de
dados. Não é a versão entregue ao usuário.

A versão melhorada é ``agente.AgenteCidadao``.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from app.texto import contem_palavra, normalizar

from agente.fichas import Ficha, carregar_fichas


class AgenteBaseline:
    """Protótipo ingênuo: primeira ficha que casa, primeira seção."""

    def __init__(self, pasta_fichas: Optional[str] = None):
        self.fichas: Dict[str, Ficha] = (
            carregar_fichas(pasta_fichas) if pasta_fichas else carregar_fichas()
        )
        self.atendimentos = 0

    def responder(self, pergunta: str) -> str:
        self.atendimentos += 1
        texto = normalizar(pergunta)
        if not texto:
            return "Mensagem vazia."

        for ficha in self.fichas.values():
            for palavra in ficha.palavras_chave:
                if contem_palavra(pergunta, normalizar(palavra)):
                    if ficha.secoes:
                        return ficha.secoes[0].texto
                    return ficha.titulo

        return "Não encontrei."

    def categorias(self) -> List[Dict[str, object]]:
        return [ficha.resumo() for ficha in self.fichas.values()]
