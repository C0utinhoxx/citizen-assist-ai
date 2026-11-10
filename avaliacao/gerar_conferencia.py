"""Gera a folha de conferência manual a partir do agente atual.

A folha é pré-preenchida com a resposta observada e a nota do juiz
determinístico. Ela **não** substitui a conferência humana: os campos de
marcação e assinatura ficam em branco para um integrante do grupo preencher.

Uso:
    python3 -m avaliacao.gerar_conferencia
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from agente import AgenteCidadao

from .juiz import JuizDeterministico, carregar_dataset

PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / "conferencia_manual.md"
IDS = [1, 3, 8, 13, 20, 21, 22, 24, 25]


def _casos_por_id(dataset: Dict[str, object]) -> Dict[int, Dict[str, object]]:
    return {int(m["id"]): m for m in dataset["mensagens"]}  # type: ignore[index]


def gerar(saida: Path = SAIDA) -> Path:
    dataset = carregar_dataset()
    casos = _casos_por_id(dataset)
    agente = AgenteCidadao(usar_llm=False)
    juiz = JuizDeterministico()

    linhas: List[str] = [
        "# Conferência manual de amostra",
        "",
        "**Status:** PENDENTE de conferência humana.",
        "",
        "> Esta folha foi pré-preenchida automaticamente com a resposta "
        "observada e a nota do juiz determinístico. O preenchimento técnico "
        "não substitui a conferência manual por um integrante do grupo. "
        "Marque cada caso e assine no final.",
        "",
        "> Para regenerar: `python3 -m avaliacao.gerar_conferencia`.",
        "",
        "Amostra: 9 casos, cobrindo escopo, fora do escopo, entrada inválida, "
        "dados pessoais, prompt injection e aviso de limitação.",
        "",
    ]

    for caso_id in IDS:
        caso = casos[caso_id]
        resposta = agente.responder(str(caso["mensagem"])).texto
        if len(resposta) > 1600:
            resposta = resposta[:1600] + "\n[...]"
        avaliacao = juiz.avaliar(caso, resposta)
        linhas.extend(
            [
                f"## Caso {caso_id} — {caso['tipo']}",
                "",
                f"**Pergunta:** {caso['mensagem']}",
                "",
                f"**Resposta esperada:** {caso['resposta_esperada']}",
                "",
                "**Resposta observada:**",
                "",
                "```text",
                resposta,
                "```",
                "",
                f"**Nota do juiz determinístico:** {avaliacao.nota:.1f}",
                "",
                "**Conferência humana:** ( ) Confere  ( ) Parcial  "
                "( ) Não confere",
                "",
                "**Observações:**",
                "",
                "```text",
                "______________________________________________________________________",
                "```",
                "",
            ]
        )

    linhas.extend(
        [
            "## Resumo da conferência",
            "",
            "| Item | Resultado |",
            "|---|---|",
            "| Casos conferidos | ____ / 9 |",
            "| Conferem | ____ |",
            "| Parciais | ____ |",
            "| Não conferem | ____ |",
            "| Divergências encontradas | ____ |",
            "",
            "**Conferido por (integrante):** ______________________________",
            "",
            "**Data:** ____/____/______",
            "",
            "**Assinatura:** ______________________________",
            "",
            "> Se houver divergência, registre o caso e a correção necessária. "
            "Não altere a resposta esperada para “fazer passar”.",
            "",
        ]
    )

    saida.write_text("\n".join(linhas), encoding="utf-8")
    return saida


if __name__ == "__main__":
    caminho = gerar()
    print(f"Folha gerada em {caminho}")
