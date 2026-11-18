"""Módulo SERS — energia e sustentabilidade no Citizen Assist AI.

O módulo calcula, com premissas explícitas, a economia de duas alternativas
para uma casa de baixa renda: eficiência energética (LED + corte de standby)
e geração solar fotovoltaica. Os resultados alimentam a opção 14 do menu.
"""

from .energia import Premissas, analisar, formatar_relatorio

__all__ = ["Premissas", "analisar", "formatar_relatorio"]
