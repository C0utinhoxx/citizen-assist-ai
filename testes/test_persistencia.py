import csv
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from app.lista_encadeada import ListaEncadeada
from app.modelos import Servico
from app.persistencia import (
    CAMPOS_CSV,
    carregar_historico,
    carregar_servicos,
    exportar_csv,
    salvar_historico,
    salvar_servicos,
)
from testes.apoio import criar_servico


class TestPersistencia(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)
        self.pasta = self.temporaria.name

    def _caminho(self, nome):
        return os.path.join(self.pasta, nome)

    def test_roundtrip_do_catalogo(self):
        lista = ListaEncadeada()
        lista.inserir(criar_servico(1, "Cartão SUS", "Saúde"))
        lista.inserir(criar_servico(
            2, "CPF", "Documentos",
            documentos=["Documento com foto", "CPF"],
            palavras_chave=["cpf", "receita federal"],
        ))

        caminho = self._caminho("servicos.json")
        self.assertTrue(salvar_servicos(caminho, lista))

        carregados = carregar_servicos(caminho)
        self.assertEqual(
            [servico.para_dict() for servico in carregados],
            [servico.para_dict() for servico in lista.percorrer()],
        )

    def test_arquivo_ausente_nao_derruba_o_programa(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            servicos = carregar_servicos(self._caminho("nao_existe.json"))

        self.assertEqual(servicos, [])
        self.assertIn("não encontrado", saida.getvalue())

    def test_json_corrompido_nao_derruba_o_programa(self):
        caminho = self._caminho("corrompido.json")
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("{ isso não é json")

        saida = io.StringIO()
        with redirect_stdout(saida):
            servicos = carregar_servicos(caminho)

        self.assertEqual(servicos, [])
        self.assertIn("não foi possível ler", saida.getvalue())

    def test_registro_invalido_e_ignorado(self):
        caminho = self._caminho("misto.json")
        dados = [
            criar_servico(1).para_dict(),
            {"id": 2, "titulo": "Incompleto"},
        ]
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False)

        saida = io.StringIO()
        with redirect_stdout(saida):
            servicos = carregar_servicos(caminho)

        self.assertEqual(len(servicos), 1)
        self.assertEqual(servicos[0].id, 1)
        self.assertIn("registro ignorado", saida.getvalue())

    def test_compatibilidade_com_os_dois_formatos_antigos(self):
        servico = Servico.de_dict({
            "id": "7",
            "titulo": "Certidão",
            "categoria": "Documentos",
            "resposta": "Texto do catálogo",
            "requisitos": "Documento com foto; CPF",
            "onde": "Cartório",
            "fonte": "https://exemplo.gov.br",
            "palavras_chave": ["certidao"],
            "verificado_em": "2026-11-05",
        })

        self.assertEqual(servico.id, 7)
        self.assertEqual(servico.descricao, "Texto do catálogo")
        self.assertEqual(servico.documentos, ["Documento com foto", "CPF"])
        self.assertEqual(servico.local, "Cartório")

    def test_historico_roundtrip(self):
        caminho = self._caminho("historico.json")
        historico = [
            {
                "data": "2026-11-05 10:00:00",
                "origem": "pergunta",
                "pergunta": "cartao sus",
                "id_orientacao": 1,
                "encontrou": True,
                "ajudou": True,
                "tentativas": 1,
                "tempo": 1.2,
            }
        ]

        self.assertTrue(salvar_historico(caminho, historico))
        self.assertEqual(carregar_historico(caminho), historico)

    def test_historico_ausente_devolve_lista_vazia(self):
        self.assertEqual(
            carregar_historico(self._caminho("nao_existe.json")), []
        )

    def test_exportar_csv(self):
        caminho = self._caminho("atendimentos.csv")
        historico = [
            {
                "data": "2026-11-05 10:00:00",
                "origem": "categoria",
                "pergunta": "Saúde",
                "id_orientacao": 1,
                "encontrou": True,
                "ajudou": False,
                "tentativas": 1,
                "tempo": 2.5,
            }
        ]

        with redirect_stdout(io.StringIO()):
            self.assertTrue(exportar_csv(caminho, historico))

        with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo))

        self.assertEqual(len(linhas), 1)
        self.assertEqual(list(linhas[0].keys()), CAMPOS_CSV)
        self.assertEqual(linhas[0]["pergunta"], "Saúde")

if __name__ == "__main__":
    unittest.main(verbosity=2)
