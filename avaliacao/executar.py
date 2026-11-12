from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Sequence

from agente import AgenteCidadao
from agente.provedor import ErroProvedor, criar_provedor, descrever_configuracao

from .baseline import AgenteBaseline
from .juiz import (
    Avaliacao,
    JuizDeterministico,
    JuizLLM,
    carregar_dataset,
    resumo,
)

PASTA_RESULTADOS = os.path.join(os.path.dirname(__file__), "resultados")


def _cabecalho(dataset: Dict[str, object], modo: str, juiz: str) -> Dict[str, object]:
    config = descrever_configuracao()
    return {
        "executado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": dataset.get("versao"),
        "dataset_total": dataset.get("total"),
        "modo_agente": modo,
        "juiz": juiz,
        "provedor": f"{config.get('modo')} ({config.get('detalhe')})",
    }


def _executar_modo(
    nome: str,
    agente,
    dataset: Dict[str, object],
    juiz,
) -> List[Avaliacao]:
    avaliacoes: List[Avaliacao] = []
    for caso in dataset["mensagens"]:  # type: ignore[index]
        pergunta = str(caso["mensagem"])
        if nome == "baseline":
            resposta = agente.responder(pergunta)
        else:
            resposta = agente.responder(pergunta).texto
        avaliacoes.append(juiz.avaliar(caso, resposta))
    return avaliacoes


def _tabela(nome: str, avaliacoes: Sequence[Avaliacao]) -> str:
    linhas = [
        f"### Casos avaliados — {nome}",
        "",
        "| # | Tipo | Nota | Fatos faltando | Justificativa |",
        "|---:|---|---:|---|---|",
    ]
    dataset = {m["id"]: m for m in carregar_dataset()["mensagens"]}
    for avaliacao in avaliacoes:
        caso = dataset.get(avaliacao.caso_id, {})
        faltando = ", ".join(avaliacao.faltando) or "—"
        justificativa = avaliacao.justificativa.replace("|", ";")
        linhas.append(
            f"| {avaliacao.caso_id} | {caso.get('tipo', '')} | "
            f"{avaliacao.nota:.1f} | {faltando} | {justificativa} |"
        )
    return "\n".join(linhas)


def _relatorio(
    metadados: Dict[str, object],
    resultados: Dict[str, List[Avaliacao]],
) -> str:
    partes = [
        "# Resultados do Golden Dataset",
        "",
        f"- Executado em: **{metadados['executado_em']}**",
        f"- Dataset: **{metadados['dataset']}** ({metadados['dataset_total']} mensagens originais)",
        f"- Juiz: **{metadados['juiz']}**",
        f"- Provedor: **{metadados['provedor']}**",
        f"- Fluxo do agente: **{metadados.get('fluxos', {})}**",
        "",
        "> As 26 mensagens são as originais do enunciado. Nenhuma foi substituída.",
        "",
    ]

    for nome, avaliacoes in resultados.items():
        dados = resumo(avaliacoes)
        partes.append(f"## {nome}")
        partes.append("")
        partes.append(
            f"Acertos exatos: **{dados['acertos_exatos']}/{dados['total']}** · "
            f"parciais: **{dados['parciais']}** · falhas: **{dados['falhas']}** · "
            f"nota média: **{dados['nota_media']}** · "
            f"aproveitamento: **{dados['percentual_acerto']}%**"
        )
        partes.append("")
        partes.append(_tabela(nome, avaliacoes))
        partes.append("")

    if metadados["juiz"] == "deterministico":
        partes.extend([
            "## Observação sobre o juiz",
            "",
            "Esta execução usou o **juiz determinístico** de rubrica explícita. "
            "O pipeline **LLM as a Judge** está implementado em `avaliacao/juiz.py` "
            "e pode ser executado com `--juiz llm` quando um provedor estiver "
            "configurado. Nenhum resultado de LLM é inventado neste relatório.",
            "",
        ])

    return "\n".join(partes)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Executa o agente no Golden Dataset e gera os resultados antes/depois."
    )
    parser.add_argument(
        "--modo",
        choices=("baseline", "melhorado", "ambos"),
        default="ambos",
        help="Qual versão do agente executar.",
    )
    parser.add_argument(
        "--juiz",
        choices=("deterministico", "llm"),
        default="deterministico",
        help="Juiz usado na avaliação.",
    )
    parser.add_argument(
        "--agente",
        choices=("extrativo", "llm", "auto"),
        default="auto",
        help="Modo do agente melhorado (auto usa LLM se houver provedor).",
    )
    parser.add_argument(
        "--fluxo",
        choices=("auto", "langgraph", "sequencial"),
        default="auto",
        help=(
            "Orquestracao do agente. 'auto' usa LangGraph quando a biblioteca "
            "esta instalada; 'sequencial' forca o fallback sem precisar "
            "desinstalar nada."
        ),
    )
    parser.add_argument(
        "--saida",
        default=PASTA_RESULTADOS,
        help="Pasta de saída dos resultados.",
    )
    args = parser.parse_args(argv)

    dataset = carregar_dataset()
    os.makedirs(args.saida, exist_ok=True)

    provedor = None
    if args.juiz == "llm" or args.agente == "llm":
        try:
            provedor = criar_provedor()
        except ErroProvedor as erro:
            print(f"Erro de configuração: {erro}", file=sys.stderr)
            return 2
        if provedor is None:
            print(
                "Nenhum provedor configurado. Defina GROQ_API_KEY, "
                "OPENAI_API_KEY ou use Ollama em agente/.env, ou rode com "
                "--juiz deterministico --agente extrativo.",
                file=sys.stderr,
            )
            return 2

    juiz = JuizLLM(provedor) if args.juiz == "llm" else JuizDeterministico()

    modos: List[str] = []
    if args.modo in ("baseline", "ambos"):
        modos.append("baseline")
    if args.modo in ("melhorado", "ambos"):
        modos.append("melhorado")

    resultados: Dict[str, List[Avaliacao]] = {}
    fluxos: Dict[str, str] = {}
    for modo in modos:
        if modo == "baseline":
            agente = AgenteBaseline()
            fluxos[modo] = "sequencial (baseline)"
        else:
            usar_llm = args.agente == "llm" or (
                args.agente == "auto" and provedor is not None
            )
            usar_langgraph = args.fluxo != "sequencial"
            agente = AgenteCidadao(
                usar_llm=usar_llm,
                usar_langgraph=usar_langgraph,
            )
            fluxos[modo] = agente.fluxo.framework
        resultados[modo] = _executar_modo(modo, agente, dataset, juiz)

    metadados = _cabecalho(dataset, args.modo, args.juiz)
    metadados["fluxos"] = fluxos
    metadados["resultados"] = {
        modo: resumo(avaliacoes) for modo, avaliacoes in resultados.items()
    }

    with open(os.path.join(args.saida, "resultados.json"), "w",
              encoding="utf-8") as arquivo:
        json.dump(
            {
                "metadados": metadados,
                "avaliacoes": {
                    modo: [a.para_dict() for a in avaliacoes]
                    for modo, avaliacoes in resultados.items()
                },
            },
            arquivo,
            ensure_ascii=False,
            indent=2,
        )

    with open(os.path.join(args.saida, "relatorio.md"), "w",
              encoding="utf-8") as arquivo:
        arquivo.write(_relatorio(metadados, resultados))

    for modo, avaliacoes in resultados.items():
        dados = resumo(avaliacoes)
        print(
            f"{modo}: {dados['acertos_exatos']}/{dados['total']} exatos, "
            f"{dados['parciais']} parciais, {dados['falhas']} falhas, "
            f"média {dados['nota_media']} ({dados['percentual_acerto']}%)."
        )

    print(f"Resultados salvos em {args.saida}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
