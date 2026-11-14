"""Atalho de importação para a estrutura pedida no enunciado de PCP.

O código real fica em ``app/modelos.py``. Este módulo existe para que
``from orientacao import Orientacao`` funcione a partir da raiz do projeto.
"""

from app.modelos import Orientacao, Servico

__all__ = ["Orientacao", "Servico"]
