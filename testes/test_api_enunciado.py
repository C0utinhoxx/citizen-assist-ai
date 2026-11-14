"""Verifica a API descrita no enunciado de PCP.

Cobre os atalhos da raiz (orientacao.py, base_conhecimento.py,
assistente.py) e o uso ``BaseConhecimento(caminho).carregar()``.
"""

import json
import unittest
from pathlib import Path

import assistente as assistente_raiz
import base_conhecimento as base_raiz
import orientacao as orientacao_raiz
from app.assistente import Assistente
from app.base_conhecimento import BaseConhecimento
from app.modelos import Orientacao, Servico

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO = RAIZ / "data" / "base_conhecimento.json"

CAMPOS_OBRIGATORIOS = [
    "id", "categoria", "titulo", "palavras_chave", "resposta",
    "documentos", "onde", "fonte", "verificado_em",
]


class TestApiDoEnunciado(unittest.TestCase):

    def test_atalhos_da_raiz_apontam_para_as_classes_reais(self):
        self.assertIs(orientacao_raiz.Orientacao, Orientacao)
        self.assertIs(base_raiz.BaseConhecimento, BaseConhecimento)
        self.assertIs(assistente_raiz.Assistente, Assistente)
        self.assertIs(Servico, Orientacao)

    def test_base_carrega_arquivo_e_cria_objetos_orientacao(self):
        base = BaseConhecimento(str(ARQUIVO))

        self.assertEqual(base.carregar(), 12)
        self.assertEqual(len(base.orientacoes), 12)
        self.assertTrue(all(isinstance(o, Orientacao) for o in base.orientacoes))
        self.assertEqual(base.caminho, str(ARQUIVO))

    def test_arquivo_ausente_nao_derruba_o_programa(self):
        base = BaseConhecimento(str(RAIZ / "data" / "nao_existe.json"))

        self.assertEqual(base.carregar(), 0)
        self.assertEqual(base.orientacoes, [])

    def test_json_tem_os_campos_obrigatorios_do_enunciado(self):
        with open(ARQUIVO, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.assertGreaterEqual(len(dados), 10)
        self.assertGreaterEqual(len({item["categoria"] for item in dados}), 3)

        for item in dados:
            for campo in CAMPOS_OBRIGATORIOS:
                self.assertIn(campo, item, f"id {item.get('id')} sem {campo}")
                self.assertTrue(item[campo], f"id {item.get('id')} com {campo} vazio")
            self.assertGreaterEqual(len(item["palavras_chave"]), 3)
            self.assertNotIn("descricao", item)
            self.assertNotIn("local", item)

    def test_apelidos_descricao_e_local_continuam_funcionando(self):
        base = BaseConhecimento(str(ARQUIVO))
        base.carregar()
        orientacao = base.orientacoes[0]

        self.assertEqual(orientacao.descricao, orientacao.resposta)
        self.assertEqual(orientacao.local, orientacao.onde)

        orientacao.descricao = "Novo texto"
        orientacao.local = "Novo local"
        self.assertEqual(orientacao.resposta, "Novo texto")
        self.assertEqual(orientacao.onde, "Novo local")


if __name__ == "__main__":
    unittest.main(verbosity=2)
