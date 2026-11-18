import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from sers.cli import executar_menu_sers
from sers.energia import Premissas, analisar, formatar_relatorio

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO_DADOS = RAIZ / "data" / "base_conhecimento.json"


class TestCalculosEnergia(unittest.TestCase):

    def setUp(self):
        self.resultado = analisar()

    def test_eficiencia_calcula_kwh_investimento_e_payback(self):
        eficiencia = self.resultado["eficiencia"]

        self.assertAlmostEqual(eficiencia["economia_led_kwh_mes"], 15.3, places=2)
        self.assertAlmostEqual(eficiencia["economia_standby_kwh_mes"], 5.76, places=2)
        self.assertAlmostEqual(eficiencia["economia_kwh_mes"], 21.06, places=2)
        self.assertAlmostEqual(eficiencia["investimento_rs"], 135.0, places=2)
        self.assertLess(eficiencia["payback_meses"], 12)

    def test_solar_dimensiona_para_o_consumo_anual(self):
        solar = self.resultado["solar"]

        self.assertAlmostEqual(solar["potencia_kwp"], 1.5, places=1)
        self.assertAlmostEqual(solar["geracao_kwh_ano"], 1800.0, places=1)
        self.assertAlmostEqual(solar["investimento_rs"], 7500.0, places=2)
        self.assertAlmostEqual(solar["economia_rs_ano"], 1377.0, places=2)
        self.assertAlmostEqual(solar["payback_anos"], 5.4, places=1)

    def test_eficiencia_tem_payback_menor_que_solar(self):
        self.assertLess(
            self.resultado["eficiencia"]["payback_anos"],
            self.resultado["solar"]["payback_anos"],
        )

    def test_cenario_combinado_reduz_o_investimento_do_solar(self):
        solar = self.resultado["solar"]
        combinado = self.resultado["combinado"]

        self.assertLess(combinado["investimento_rs"], solar["investimento_rs"])
        self.assertEqual(combinado["solar"]["potencia_kwp"], 1.3)
        self.assertAlmostEqual(combinado["investimento_rs"], 6635.0, places=2)

    def test_validacao_recusa_premissas_invalidas(self):
        with self.assertRaises(ValueError):
            Premissas(consumo_mensal_kwh=0).validar()

        with self.assertRaises(ValueError):
            Premissas(potencia_led_w=70).validar()

        with self.assertRaises(ValueError):
            Premissas(fator_compensacao=1.5).validar()

    def test_relatorio_tem_alternativas_fontes_e_aviso(self):
        texto = formatar_relatorio(self.resultado)

        self.assertIn("ALTERNATIVA A", texto)
        self.assertIn("ALTERNATIVA B", texto)
        self.assertIn("CENÁRIO COMBINADO", texto)
        self.assertIn("ANEEL", texto)
        self.assertIn("MCTI", texto)
        self.assertIn("não é um canal oficial", texto)
        self.assertIn("estimativas", texto)


class TestIntegracaoSersNoAssistente(unittest.TestCase):

    def test_base_tem_orientacoes_de_energia_com_fonte_e_data(self):
        with open(ARQUIVO_DADOS, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        energia = [item for item in dados if item["categoria"] == "Energia"]
        self.assertEqual(len(energia), 3)

        for item in energia:
            self.assertGreaterEqual(len(item["palavras_chave"]), 3)
            self.assertTrue(item["fonte"].startswith("https://www."))
            self.assertTrue(item["verificado_em"])
            self.assertIn("SERS", item["resposta"])

    def test_menu_sers_compoe_o_relatorio(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["1", "", "0"]):
            with redirect_stdout(saida):
                executar_menu_sers()

        texto = saida.getvalue()
        self.assertIn("Energia e sustentabilidade (SERS)", texto)
        self.assertIn("R$ 1377.00", texto)
        self.assertIn("FONTES E CONDIÇÕES", texto)

    def test_menu_sers_aceita_consumo_personalizado(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["2", "300", "0,95", "", "0"]):
            with redirect_stdout(saida):
                executar_menu_sers()

        texto = saida.getvalue()
        self.assertIn("Consumo considerado: 300.0 kWh/mês", texto)
        self.assertIn("Tarifa considerada: R$ 0.95/kWh", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
