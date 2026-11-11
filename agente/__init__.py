"""Agente de orientação sobre documentos pessoais do Citizen Assist AI.

O agente usa exclusivamente as fichas FC-01 a FC-07 como fonte de verdade.
A pasta ``agente/fichas`` contém as sete fichas oficiais do exercício,
versão de 01/10/2026, convertidas para o formato Markdown do carregador.
"""

from .agente import AgenteCidadao, Resposta

__all__ = ["AgenteCidadao", "Resposta"]
