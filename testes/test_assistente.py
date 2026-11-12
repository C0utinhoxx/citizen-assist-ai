import csv
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from app.assistente import Assistente
from app.base_conhecimento import BaseConhecimento
from app.lista_encadeada import ListaEncadeada
from testes.apoio import criar_servico


class TestAssistente(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)

        self.lista = ListaEncadeada()
        self.lista.inserir(criar_servico(
            1,
            "Fazer o Cartão Nacional de Saúde (Cartão SUS)",
            "Saúde",
            palavras_chave=[
                "cartao sus", "cartao do sus", "sus", "cns",
                "cartao nacional de saude",
            ],
        ))

        self.base = BaseConhecimento(self.lista)
        self.caminho_historico = os.path.join(
            self.temporaria.name, "historico.json"
        )
        self.caminho_csv = os.path.join(
            self.temporaria.name, "atendimentos.csv"
        )
        self.assistente = Assistente(
            "Citizen Assist AI",
            self.base,
            self.caminho_historico,
            self.caminho_csv,
        )

    def test_contem_dado_pessoal(self):
        casos = [
            ("meu cpf é 12345678900", True),
            ("meu telefone 11999999999", True),
            ("meu email teste@exemplo.com", True),
            ("como tirar o cartao sus", False),
            ("meu numero curto 1234567", False),
        ]

        for texto, esperado in casos:
            with self.subTest(texto=texto):
                self.assertEqual(
                    self.assistente.contem_dado_pessoal(texto), esperado
                )

    def test_perguntar_encontrou(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=[
            "Como faço o cartão do SUS?", "s"
        ]):
            with redirect_stdout(saida):
                self.assistente.perguntar()

        self.assertEqual(len(self.assistente.historico), 1)
        registro = self.assistente.historico[0]
        self.assertTrue(registro["encontrou"])
        self.assertTrue(registro["ajudou"])
        self.assertEqual(registro["id_orientacao"], 1)
        self.assertIn("Confiança da resposta: ALTA", saida.getvalue())
        self.assertIn("7 pontos", saida.getvalue())

    def test_perguntar_bloqueia_dado_pessoal(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=[
            "meu cpf é 12345678900", "0"
        ]):
            with redirect_stdout(saida):
                self.assistente.perguntar()

        self.assertEqual(self.assistente.historico, [])
        self.assertIn("não digite CPF", saida.getvalue())

    def test_perguntar_sem_resultado(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["assunto inexistente", "n"]):
            with redirect_stdout(saida):
                self.assistente.perguntar()

        self.assertEqual(len(self.assistente.historico), 1)
        registro = self.assistente.historico[0]
        self.assertFalse(registro["encontrou"])
        self.assertFalse(registro["ajudou"])
        self.assertIsNone(registro["id_orientacao"])
        self.assertIn("Não encontrei", saida.getvalue())

    def test_perguntar_com_zero_na_primeira_entrada(self):
        with patch("builtins.input", side_effect=["0"]):
            with redirect_stdout(io.StringIO()):
                self.assistente.perguntar()

        self.assertEqual(self.assistente.historico, [])

    def test_navegar_por_categoria(self):
        with patch("builtins.input", side_effect=["1", "1", "s", "0"]):
            with redirect_stdout(io.StringIO()):
                self.assistente.navegar()

        self.assertEqual(len(self.assistente.historico), 1)
        registro = self.assistente.historico[0]
        self.assertEqual(registro["origem"], "categoria")
        self.assertEqual(registro["id_orientacao"], 1)
        self.assertTrue(registro["ajudou"])

    def test_calcular_indicadores(self):
        self.assistente.historico = [
            {
                "pergunta": "cartao sus",
                "encontrou": True,
                "ajudou": True,
                "tentativas": 1,
                "tempo": 2.0,
                "nota_facilidade": 4,
            },
            {
                "pergunta": "xyz",
                "encontrou": False,
                "ajudou": False,
                "tentativas": 2,
                "tempo": 0,
            },
        ]

        dados = self.assistente.calcular_indicadores()

        self.assertEqual(dados["total"], 2)
        self.assertEqual(dados["encontrados"], 1)
        self.assertEqual(dados["ajudaram"], 1)
        self.assertEqual(dados["percentual_encontrados"], 50.0)
        self.assertEqual(dados["percentual_ajudaram"], 50.0)
        self.assertEqual(dados["tempo_medio"], 2.0)
        self.assertEqual(dados["tentativas_medias"], 1.5)
        self.assertEqual(dados["facilidade"], "4.0 (1 a 5)")
        self.assertEqual(dados["sem_solucao"], ["xyz"])

    def test_indicadores_sem_atendimentos(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            self.assistente.indicadores()

        self.assertIn("Nenhum atendimento registrado", saida.getvalue())
        self.assertIn("não avaliada", saida.getvalue())

    def test_registrar_persiste_no_json(self):
        self.assistente.registrar(
            "pergunta", "cartao sus", 1, True, True, 1, 1.5
        )

        with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["pergunta"], "cartao sus")

    def test_exportar_csv(self):
        self.assistente.registrar(
            "pergunta", "cartao sus", 1, True, True, 1, 1.5
        )
        with redirect_stdout(io.StringIO()):
            self.assertTrue(self.assistente.exportar_csv())

        with open(self.caminho_csv, "r", encoding="utf-8", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo))

        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0]["id_orientacao"], "1")

    def test_finalizar_salva_nota_e_exporta(self):
        self.assistente.registrar(
            "categoria", "Saúde", 1, True, True, 1, 1.0
        )

        with patch("builtins.input", side_effect=["5"]):
            with redirect_stdout(io.StringIO()):
                self.assistente.finalizar()

        self.assertEqual(self.assistente.nota_facilidade, 5)
        self.assertEqual(
            self.assistente.historico[-1]["nota_facilidade"], 5
        )
        self.assertTrue(os.path.exists(self.caminho_csv))

if __name__ == "__main__":
    unittest.main(verbosity=2)
