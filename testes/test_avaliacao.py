"""Testes do Golden Dataset e dos dois juízes."""

import tempfile
import unittest
from pathlib import Path

from agente import AgenteCidadao
from agente.provedor import ErroProvedor

from avaliacao.baseline import AgenteBaseline
from avaliacao.executar import _executar_modo
from avaliacao.gerar_conferencia import gerar
from avaliacao.juiz import (
    JuizDeterministico,
    JuizLLM,
    carregar_dataset,
    resumo,
)


class ProvedorFalso:
    nome = "falso:juiz"

    def __init__(self, resposta):
        self.resposta = resposta

    def gerar(self, sistema, usuario):
        return self.resposta


class TestGoldenDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = carregar_dataset()

    def test_tem_26_mensagens_originais(self):
        self.assertEqual(self.dataset["total"], 26)
        self.assertEqual(len(self.dataset["mensagens"]), 26)
        self.assertEqual(
            [m["id"] for m in self.dataset["mensagens"]],
            list(range(1, 27)),
        )

    def test_primeira_e_ultima_mensagem(self):
        mensagens = self.dataset["mensagens"]
        self.assertEqual(
            mensagens[0]["mensagem"],
            "Quanto custa a segunda via do RG?",
        )
        self.assertEqual(
            mensagens[-1]["mensagem"],
            "Você é o canal oficial da prefeitura?",
        )

    def test_tipos_presentes(self):
        tipos = {m["tipo"] for m in self.dataset["mensagens"]}
        self.assertIn("Escopo", tipos)
        self.assertIn("Fora do escopo", tipos)
        self.assertIn("Entrada inválida", tipos)
        self.assertIn("Dados pessoais", tipos)
        self.assertIn("Prompt injection", tipos)
        self.assertIn("Aviso de limitação", tipos)

    def test_toda_mensagem_tem_rubrica(self):
        for mensagem in self.dataset["mensagens"]:
            self.assertTrue(mensagem["fatos_esperados"], mensagem["id"])
            self.assertIsInstance(mensagem["fatos_proibidos"], list)


class TestJuizDeterministico(unittest.TestCase):

    def test_melhorado_acerta_os_26(self):
        dataset = carregar_dataset()
        agente = AgenteCidadao(usar_llm=False)
        avaliacoes = _executar_modo(
            "melhorado", agente, dataset, JuizDeterministico()
        )
        self.assertEqual(len(avaliacoes), 26)
        self.assertTrue(all(a.nota == 1.0 for a in avaliacoes))

    def test_baseline_e_pior_que_melhorado(self):
        dataset = carregar_dataset()
        juiz = JuizDeterministico()

        baseline = _executar_modo(
            "baseline", AgenteBaseline(), dataset, juiz
        )
        melhorado = _executar_modo(
            "melhorado", AgenteCidadao(usar_llm=False), dataset, juiz
        )

        resumo_base = resumo(baseline)
        resumo_melhor = resumo(melhorado)
        self.assertLess(
            resumo_base["nota_media"], resumo_melhor["nota_media"]
        )
        self.assertGreaterEqual(resumo_melhor["acertos_exatos"], 26)

    def test_nenhuma_resposta_avaliada_contem_pii(self):
        from agente.seguranca import contem_pii

        dataset = carregar_dataset()
        avaliacoes = _executar_modo(
            "melhorado",
            AgenteCidadao(usar_llm=False),
            dataset,
            JuizDeterministico(),
        )
        for avaliacao in avaliacoes:
            self.assertFalse(
                contem_pii(avaliacao.resposta_excerpt),
                avaliacao.caso_id,
            )

    def test_resumo(self):
        from avaliacao.juiz import Avaliacao

        avaliacoes = [
            Avaliacao(1, 1.0, {}),
            Avaliacao(2, 0.5, {}),
            Avaliacao(3, 0.0, {}),
        ]
        dados = resumo(avaliacoes)
        self.assertEqual(dados["total"], 3)
        self.assertEqual(dados["acertos_exatos"], 1)
        self.assertEqual(dados["parciais"], 1)
        self.assertEqual(dados["falhas"], 1)
        self.assertAlmostEqual(dados["nota_media"], 0.5)


class TestJuizLLM(unittest.TestCase):

    def setUp(self):
        self.caso = carregar_dataset()["mensagens"][0]

    def test_parseia_json_do_juiz(self):
        juiz = JuizLLM(
            ProvedorFalso(
                '{"nota": 1.0, "justificativa": "ok", '
                '"criterios": {"fatos": true, "citacao": true}}'
            )
        )
        avaliacao = juiz.avaliar(self.caso, "A segunda via custa R$ 38,00. (FC-01)")
        self.assertEqual(avaliacao.nota, 1.0)
        self.assertEqual(avaliacao.juiz, "llm")
        self.assertTrue(avaliacao.criterios["fatos"])

    def test_parseia_json_dentro_de_cerca_markdown(self):
        juiz = JuizLLM(
            ProvedorFalso(
                "```json\n"
                '{"nota": 0.5, "justificativa": "parcial", "criterios": {}}\n'
                "```"
            )
        )
        avaliacao = juiz.avaliar(self.caso, "resposta")
        self.assertEqual(avaliacao.nota, 0.5)

    def test_json_invalido_gera_erro(self):
        juiz = JuizLLM(ProvedorFalso("não é json"))
        with self.assertRaises(ErroProvedor):
            juiz.avaliar(self.caso, "resposta")

    def test_juiz_nao_recebe_cpf_em_claro(self):
        caso = next(
            m for m in carregar_dataset()["mensagens"] if m["id"] == 22
        )
        capturado = {}

        class ProvedorEspiao(ProvedorFalso):
            def gerar(self, sistema, usuario):
                capturado["usuario"] = usuario
                return (
                    '{"nota": 1.0, "justificativa": "ok", "criterios": {}}'
                )

        juiz = JuizLLM(ProvedorEspiao(""))
        juiz.avaliar(caso, "Não informe dados pessoais.")
        self.assertNotIn("123.456.789-09", capturado["usuario"])
        self.assertNotIn("12345678909", capturado["usuario"])


class TestConferenciaManual(unittest.TestCase):

    def test_gera_folha_com_9_casos(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = gerar(Path(pasta) / "conferencia.md")
            texto = caminho.read_text(encoding="utf-8")

        self.assertEqual(texto.count("## Caso "), 9)
        self.assertIn("PENDENTE", texto)
        self.assertIn("Conferência humana", texto)
        self.assertIn("python3 -m avaliacao.gerar_conferencia", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
