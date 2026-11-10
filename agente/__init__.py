"""Agente de orientação sobre documentos pessoais do Citizen Assist AI.

O agente usa exclusivamente as fichas FC-01 a FC-07 como fonte de verdade.
A pasta ``agente/fichas`` contém o material carregado. Enquanto as fichas
oficiais não forem adicionadas, os arquivos existentes são provisórios e
estão marcados como tal.
"""

from .agente import AgenteCidadao, Resposta

__all__ = ["AgenteCidadao", "Resposta"]
