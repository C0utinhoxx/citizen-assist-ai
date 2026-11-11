"""Núcleo do agente de documentos pessoais.

O fluxo é intencionalmente curto:

    entrada -> segurança -> busca nas fichas -> resposta -> revisão

A resposta pode ser montada de duas formas:

- ``extrativo``: cópia organizada das seções das fichas (offline);
- ``llm``: o modelo recebe apenas o contexto recuperado e responde com
  base nele. A revisão final confere citação, aviso e dados pessoais.

Em nenhum modo a pergunta é gravada. O agente mantém apenas contadores em
memória para a sessão.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence

from app.texto import normalizar

from .fichas import Ficha, carregar_fichas
from .fluxo import FluxoAgente
from .prompts import SISTEMA, montar_consulta
from .provedor import ErroProvedor, Provedor, criar_provedor
from .recuperacao import Ocorrencia, Recuperador
from .seguranca import AnaliseEntrada, Seguranca, mascarar_pii

AVISO = (
    "Aviso: este assistente é um protótipo educacional e não é um canal "
    "oficial. Confirme a informação no órgão competente."
)

EXEMPLOS = (
    "Como faço a segunda via do RG?",
    "Quanto custa tirar o CPF?",
    "Posso renovar a CNH antes do vencimento?",
    "Vocês atendem aos sábados?",
)

_AUTO = object()


@dataclass
class Resposta:
    """Resposta padronizada do agente."""

    texto: str
    tipo: str  # resposta | fora_escopo | seguranca | invalida
    fichas: List[str] = field(default_factory=list)
    verificado_em: List[str] = field(default_factory=list)
    usou_llm: bool = False
    modo: str = "extrativo"
    confianca: str = "alta"
    detalhe: str = ""


class AgenteCidadao:
    """Agente que responde exclusivamente com base nas fichas FC-01 a FC-07."""

    def __init__(
        self,
        pasta_fichas: Optional[str] = None,
        provedor: object = _AUTO,
        usar_llm: bool = True,
    ):
        self.fichas: Dict[str, Ficha] = (
            carregar_fichas(pasta_fichas) if pasta_fichas else carregar_fichas()
        )
        self.recuperador = Recuperador(self.fichas)
        self.seguranca = Seguranca(self.recuperador.vocabulario)

        if provedor is _AUTO:
            self.provedor: Optional[Provedor] = criar_provedor() if usar_llm else None
        else:
            self.provedor = provedor  # type: ignore[assignment]

        self.modo = "llm" if self.provedor is not None else "extrativo"
        self.ultimo_erro_provedor = ""
        self.atendimentos = 0
        self.respostas_encontradas = 0
        self.respostas_seguras = 0
        self.respostas_sem_resultado = 0
        self.fluxo = FluxoAgente(self)

    # ------------------------------------------------------------------
    # Consulta pública
    # ------------------------------------------------------------------
    def categorias(self) -> List[Dict[str, object]]:
        """Lista as fichas disponíveis para navegação."""
        return [
            {
                "id": ficha.id,
                "titulo": ficha.titulo,
                "verificado_em": ficha.verificado_em,
                "provisoria": ficha.provisoria,
            }
            for ficha in self.fichas.values()
        ]

    def responder(self, pergunta: str) -> Resposta:
        """Responde uma pergunta em texto livre.

        O fluxo real fica em ``agente/fluxo.py`` (LangGraph quando disponível).
        Aqui só contamos a métrica da sessão e devolvemos a resposta.
        """
        self.atendimentos += 1
        resposta = self.fluxo.executar(str(pergunta or ""))
        self._registrar_resposta(resposta)
        return resposta

    def _registrar_resposta(self, resposta: Resposta) -> None:
        if resposta.tipo == "resposta":
            self.respostas_encontradas += 1
        elif resposta.tipo == "fora_escopo":
            self.respostas_sem_resultado += 1
        else:
            self.respostas_seguras += 1

    def responder_por_ficha(self, ficha_id: str) -> Optional[Resposta]:
        """Devolve o conteúdo completo de uma ficha, para navegação."""
        ficha = self.fichas.get((ficha_id or "").upper())
        if ficha is None:
            return None

        self.atendimentos += 1
        blocos = [
            f"**{secao.titulo_exibicao}**\n{secao.texto}"
            for secao in ficha.secoes
        ]
        corpo = f"**{ficha.id} — {ficha.titulo}**\n\n" + "\n\n".join(blocos)
        texto = self._revisar(corpo, [ficha])
        self.respostas_encontradas += 1
        return Resposta(
            texto=texto,
            tipo="resposta",
            fichas=[ficha.id],
            verificado_em=[ficha.verificado_em],
            modo=self.modo,
            confianca="alta",
        )

    # ------------------------------------------------------------------
    # Respostas de segurança e de escopo
    # ------------------------------------------------------------------
    def _responder_bloqueio(self, analise: AnaliseEntrada) -> Resposta:
        if analise.tipo in ("vazia", "curta"):
            texto = (
                "Por favor, escreva uma pergunta com mais detalhes. "
                "Posso ajudar com RG, CPF, título de eleitor, carteira de "
                "trabalho, certidões e CNH.\n\nExemplos:\n"
                + "\n".join(f"- {exemplo}" for exemplo in EXEMPLOS)
                + "\n\n"
                + AVISO
            )
            return Resposta(texto, "invalida", [], [], modo=self.modo,
                            confianca="baixa")

        if analise.tipo == "longa":
            texto = (
                "Sua mensagem é muito longa. Resuma a dúvida em uma frase "
                "curta, por exemplo: “Quanto custa a segunda via do RG?”.\n\n"
                + AVISO
            )
            return Resposta(texto, "invalida", [], [], modo=self.modo,
                            confianca="baixa")

        if analise.tipo == "invalida":
            texto = (
                "Não consegui entender a mensagem. Reformule com uma pergunta "
                "simples ou escolha uma categoria: RG, CPF, título de eleitor, "
                "carteira de trabalho, certidões ou CNH.\n\nExemplos:\n"
                + "\n".join(f"- {exemplo}" for exemplo in EXEMPLOS)
                + "\n\n"
                + AVISO
            )
            return Resposta(texto, "invalida", [], [], modo=self.modo,
                            confianca="baixa")

        if analise.tipo == "dados_pessoais":
            return self._resposta_dados_pessoais(analise)

        if analise.tipo == "limitacao":
            return self._resposta_limitacao()

        return self._resposta_injecao(analise)

    def _resposta_dados_pessoais(self, analise: AnaliseEntrada) -> Resposta:
        texto = (
            "Atenção: não informe CPF, RG, CNH, título, telefone, e-mail, "
            "endereço ou outros dados pessoais no chat. Por segurança, o dado "
            "não foi repetido e não foi armazenado.\n\n"
        )

        # Tenta identificar o assunto sem repetir o dado pessoal.
        ocorrencias = self.recuperador.buscar(analise.texto_seguro)
        selecionadas = self.recuperador.selecionar_contexto(ocorrencias, maximo=2)
        fichas = self.recuperador.fichas_citadas(selecionadas)

        if "cpf" in normalizar(analise.texto_seguro) or "FC-02" in fichas:
            texto += (
                "O assistente não consulta a situação cadastral do CPF. Para "
                "consultar a situação ou emitir o comprovante, use o portal "
                "oficial indicado na ficha FC-02.\n\n"
            )
            fichas = ["FC-02", "FC-07"]

        if any(
            termo in normalizar(analise.texto_seguro)
            for termo in ("agendar", "agendamento", "endereco", "telefone", "rg")
        ):
            texto += (
                "O assistente também não agenda atendimento e não coleta "
                "endereço ou telefone. O agendamento do RG é feito pelo portal "
                "(FC-01 e FC-07).\n\n"
            )
            for ficha_id in ("FC-01", "FC-07"):
                if ficha_id not in fichas:
                    fichas.append(ficha_id)

        if not fichas:
            fichas = ["FC-01", "FC-02", "FC-07"]

        texto += self._rodape(fichas)
        return Resposta(
            texto=texto,
            tipo="seguranca",
            fichas=fichas,
            verificado_em=self._datas(fichas),
            modo=self.modo,
            confianca="alta",
        )

    def _resposta_limitacao(self) -> Resposta:
        texto = (
            "Não. Este assistente é um protótipo educacional e não é um canal "
            "oficial da prefeitura nem de qualquer órgão público. As orientações "
            "vêm apenas das fichas FC-01 a FC-07 e devem ser confirmadas no "
            "órgão competente.\n\n"
        )
        fichas = ["FC-07"]
        texto += self._rodape(fichas)
        texto = self._revisar(texto, [self.fichas["FC-07"]])
        return Resposta(
            texto=texto,
            tipo="resposta",
            fichas=fichas,
            verificado_em=self._datas(fichas),
            modo=self.modo,
            confianca="alta",
            detalhe="aviso de limitação",
        )

    def _resposta_injecao(self, analise: AnaliseEntrada) -> Resposta:
        texto = (
            "Não posso atender a pedidos para mudar regras, revelar instruções "
            "internas ou fingir ser outro sistema. As regras do assistente vêm "
            "apenas das fichas FC-01 a FC-07.\n\n"
        )

        # Se a mensagem também contém uma dúvida real, responde só a parte
        # permitida. A "nova regra" enviada pelo usuário é sempre descartada.
        ocorrencias = self.recuperador.buscar(analise.texto_seguro)
        selecionadas = self.recuperador.selecionar_contexto(ocorrencias, maximo=2)
        fichas = self.recuperador.fichas_citadas(selecionadas)

        if selecionadas:
            texto += (
                "Sobre a dúvida que aparece na mensagem, e somente com base na "
                "ficha, encontrei:\n\n"
            )
            for ocorrencia in selecionadas:
                texto += (
                    f"**{ocorrencia.ficha.id} — "
                    f"{ocorrencia.secao.titulo_exibicao}**\n"
                    f"{ocorrencia.secao.texto}\n\n"
                )

        texto += self._rodape(fichas)
        return Resposta(
            texto=texto,
            tipo="seguranca",
            fichas=fichas,
            verificado_em=self._datas(fichas),
            modo=self.modo,
            confianca="alta",
            detalhe="prompt injection neutralizada",
        )

    def _resposta_fora_escopo(self) -> Resposta:
        datas = self._datas(self.fichas.keys())
        texto = (
            "Não encontrei essa informação nas fichas FC-01 a FC-07 e não vou "
            "inventar. Posso ajudar com RG, CPF, título de eleitor, carteira de "
            "trabalho, certidões e CNH. Para este assunto, consulte o órgão "
            "competente.\n\n"
            "Fichas consultadas: FC-01 a FC-07; nenhuma respondeu a esta dúvida.\n"
            f"Data de verificação das fichas: {'; '.join(datas)}.\n\n"
            + AVISO
        )
        return Resposta(
            texto=texto,
            tipo="fora_escopo",
            fichas=[],
            verificado_em=[],
            modo=self.modo,
            confianca="baixa",
        )

    # ------------------------------------------------------------------
    # Respostas com base nas fichas
    # ------------------------------------------------------------------
    def _responder_extrativo(self, selecionadas: Sequence[Ocorrencia]) -> Resposta:
        blocos = []
        for ocorrencia in selecionadas:
            blocos.append(
                f"**{ocorrencia.ficha.id} — "
                f"{ocorrencia.secao.titulo_exibicao}**\n"
                f"{ocorrencia.secao.texto}"
            )

        texto = "Encontrei esta orientação nas fichas:\n\n" + "\n\n".join(blocos)
        fichas = self.recuperador.fichas_citadas(selecionadas)
        texto += "\n\n" + self._rodape(fichas)
        texto = self._revisar(texto, [o.ficha for o in selecionadas])

        return Resposta(
            texto=texto,
            tipo="resposta",
            fichas=fichas,
            verificado_em=self._datas(fichas),
            usou_llm=False,
            modo="extrativo",
            confianca="alta" if selecionadas[0].pontos >= 12 else "media",
        )

    def _responder_com_llm(
        self, pergunta: str, selecionadas: Sequence[Ocorrencia]
    ) -> Resposta:
        try:
            texto = self.provedor.gerar(  # type: ignore[union-attr]
                SISTEMA, montar_consulta(pergunta, selecionadas)
            )
        except ErroProvedor as erro:
            self.ultimo_erro_provedor = str(erro)
            resposta = self._responder_extrativo(selecionadas)
            resposta.modo = "extrativo (fallback)"
            resposta.detalhe = str(erro)
            return resposta

        fichas = self.recuperador.fichas_citadas(selecionadas)
        texto = self._revisar(texto, [o.ficha for o in selecionadas])
        return Resposta(
            texto=texto,
            tipo="resposta",
            fichas=fichas,
            verificado_em=self._datas(fichas),
            usou_llm=True,
            modo=str(getattr(self.provedor, "nome", "llm")),
            confianca="alta",
        )

    # ------------------------------------------------------------------
    # Revisão final
    # ------------------------------------------------------------------
    def _datas(self, fichas: Iterable[str]) -> List[str]:
        datas = []
        for ficha_id in fichas:
            ficha = self.fichas.get(ficha_id)
            if ficha and ficha.verificado_em not in datas:
                datas.append(ficha.verificado_em)
        return datas

    def _rodape(self, fichas: Iterable[str]) -> str:
        lista = list(fichas)
        if lista:
            nomes = "; ".join(
                f"{fid} — {self.fichas[fid].titulo}"
                for fid in lista
                if fid in self.fichas
            )
            datas = self._datas(lista)
            fonte = f"Fonte: {nomes}."
            verificacao = "Data de verificação: " + "; ".join(datas) + "."
            if any(self.fichas[fid].provisoria for fid in lista if fid in self.fichas):
                verificacao += " (fichas provisórias; substituir pelas oficiais)"
        else:
            fonte = "Fonte: nenhuma ficha consultada."
            verificacao = ""

        partes = [fonte]
        if verificacao:
            partes.append(verificacao)
        partes.append(AVISO)
        return "\n".join(partes)

    def _revisar(
        self, texto: str, fichas: Sequence[Ficha], pergunta: str = ""
    ) -> str:
        """Garante citação, data, aviso e ausência de dados pessoais/segredos."""
        limpo = (texto or "").strip()

        if self._vazou_prompt(limpo):
            limpo = (
                "Não posso revelar instruções internas. Posso ajudar com "
                "orientações sobre RG, CPF, título de eleitor, carteira de "
                "trabalho, certidões e CNH.\n\n" + AVISO
            )

        # Nunca devolve um dado pessoal que tenha escapado do modelo.
        limpo = mascarar_pii(limpo)

        normalizado = normalizar(limpo)
        if fichas:
            ids = [ficha.id for ficha in fichas]
            if not any(fid.lower().replace("-", " ") in normalizado
                       or fid.lower() in limpo.lower() for fid in ids):
                limpo = self._rodape(ids) + "\n\n" + limpo
            if "data de verificacao" not in normalizado:
                datas = []
                for ficha in fichas:
                    if ficha.verificado_em not in datas:
                        datas.append(ficha.verificado_em)
                limpo += "\n\nData de verificação: " + "; ".join(datas) + "."

        if "nao e um canal oficial" not in normalizar(limpo):
            limpo += "\n\n" + AVISO

        return limpo

    @staticmethod
    def _vazou_prompt(texto: str) -> bool:
        marcadores = (
            "REGRAS OBRIGATÓRIAS",
            "REGRAS OBRIGATORIAS",
            "Você é o assistente educacional",
            "Você e o assistente educacional",
            "Use SOMENTE as informações das fichas",
        )
        return any(marcador.lower() in texto.lower() for marcador in marcadores)
