from __future__ import annotations

from typing import Any, Dict, TypedDict

try:  # pragma: no cover - depende do ambiente
    from langgraph.graph import END, StateGraph

    LANGGRAPH_DISPONIVEL = True
except ImportError:  # pragma: no cover - caminho sem a dependência
    END = "__end__"  # type: ignore[assignment]
    StateGraph = None  # type: ignore[assignment]
    LANGGRAPH_DISPONIVEL = False


class EstadoAgente(TypedDict, total=False):

    pergunta: str
    analise: Any
    ocorrencias: list
    selecionadas: list
    resposta: Any


class FluxoAgente:

    def __init__(self, agente: "AgenteCidadao"):
        self.agente = agente
        self._grafo = self._construir_grafo() if LANGGRAPH_DISPONIVEL else None

    @property
    def framework(self) -> str:
        return "langgraph" if self._grafo is not None else "sequencial"

    def _no_analisar(self, estado: EstadoAgente) -> Dict[str, Any]:
        analise = self.agente.seguranca.analisar(estado.get("pergunta", ""))
        return {"analise": analise}

    def _rota_analise(self, estado: EstadoAgente) -> str:
        analise = estado.get("analise")
        if analise is not None and analise.bloqueada:
            return "bloqueio"
        return "recuperar"

    def _no_recuperar(self, estado: EstadoAgente) -> Dict[str, Any]:
        analise = estado["analise"]
        ocorrencias = self.agente.recuperador.buscar(analise.texto_seguro)
        selecionadas = self.agente.recuperador.selecionar_contexto(ocorrencias)
        return {
            "ocorrencias": ocorrencias,
            "selecionadas": selecionadas,
        }

    def _rota_busca(self, estado: EstadoAgente) -> str:
        if not estado.get("selecionadas"):
            return "sem_resultado"
        return "responder"

    def _no_responder(self, estado: EstadoAgente) -> Dict[str, Any]:
        analise = estado["analise"]
        selecionadas = estado["selecionadas"]
        if self.agente.provedor is not None:
            resposta = self.agente._responder_com_llm(
                analise.texto_seguro, selecionadas
            )
        else:
            resposta = self.agente._responder_extrativo(selecionadas)
        return {"resposta": resposta}

    def _no_bloqueio(self, estado: EstadoAgente) -> Dict[str, Any]:
        return {"resposta": self.agente._responder_bloqueio(estado["analise"])}

    def _no_sem_resultado(self, estado: EstadoAgente) -> Dict[str, Any]:
        return {"resposta": self.agente._resposta_fora_escopo()}

    def _construir_grafo(self):
        grafo = StateGraph(EstadoAgente)
        grafo.add_node("analisar", self._no_analisar)
        grafo.add_node("recuperar", self._no_recuperar)
        grafo.add_node("responder", self._no_responder)
        grafo.add_node("bloqueio", self._no_bloqueio)
        grafo.add_node("sem_resultado", self._no_sem_resultado)

        grafo.set_entry_point("analisar")
        grafo.add_conditional_edges(
            "analisar",
            self._rota_analise,
            {"bloqueio": "bloqueio", "recuperar": "recuperar"},
        )
        grafo.add_conditional_edges(
            "recuperar",
            self._rota_busca,
            {"sem_resultado": "sem_resultado", "responder": "responder"},
        )
        grafo.add_edge("responder", END)
        grafo.add_edge("bloqueio", END)
        grafo.add_edge("sem_resultado", END)
        return grafo.compile()

    def executar(self, pergunta: str) -> "Resposta":
        if self._grafo is not None:
            estado = self._grafo.invoke({"pergunta": pergunta})
            return estado["resposta"]

        estado: EstadoAgente = {"pergunta": pergunta}
        estado.update(self._no_analisar(estado))
        if self._rota_analise(estado) == "bloqueio":
            estado.update(self._no_bloqueio(estado))
            return estado["resposta"]

        estado.update(self._no_recuperar(estado))
        if self._rota_busca(estado) == "sem_resultado":
            estado.update(self._no_sem_resultado(estado))
            return estado["resposta"]

        estado.update(self._no_responder(estado))
        return estado["resposta"]
