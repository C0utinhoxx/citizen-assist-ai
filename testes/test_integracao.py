import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from app.assistente import Assistente
from app.base_conhecimento import BaseConhecimento
from app.interface import (
    analise_servicos,
    atualizar,
    cadastrar,
    confirmar,
    consultar,
    executar_menu,
    excluir,
    ler_inteiro,
    ler_lista,
    ler_texto,
    listar,
    ordenar,
    pesquisar,
)
from app.lista_encadeada import ListaEncadeada
from app.persistencia import carregar_servicos
from testes.apoio import criar_servico


class TestValidacaoDeEntradas(unittest.TestCase):

    def test_ler_inteiro_repete_ate_ser_valido(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "99", "5"]):
            with redirect_stdout(saida):
                numero = ler_inteiro("Opção: ", 1, 8)

        self.assertEqual(numero, 5)
        self.assertIn("número inteiro", saida.getvalue())
        self.assertIn("de 1 a 8", saida.getvalue())

    def test_ler_texto_recusa_vazio(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["", "  ", "ok"]):
            with redirect_stdout(saida):
                texto = ler_texto("Texto: ")

        self.assertEqual(texto, "ok")
        self.assertIn("não pode ficar vazio", saida.getvalue())

    def test_confirmar_repete_ate_s_ou_n(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["talvez", "s"]):
            with redirect_stdout(saida):
                resposta = confirmar("Confirma? ")

        self.assertTrue(resposta)
        self.assertIn("Responda com s", saida.getvalue())

    def test_ler_lista_separa_e_remove_vazios(self):
        with patch("builtins.input", side_effect=["Doc A; Doc B; ; Doc C"]):
            self.assertEqual(
                ler_lista("Documentos: ", ";"),
                ["Doc A", "Doc B", "Doc C"],
            )


class TestOperacoesDoMenu(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)
        self.lista = ListaEncadeada()

    def _adicionar_teste(self, id=99):
        servico = criar_servico(
            id,
            "Serviço de teste",
            "Teste",
            descricao="Descrição do serviço de teste",
            documentos=["Doc A", "Doc B"],
            local="Unidade Central",
            palavras_chave=["teste", "ajuda"],
        )
        self.lista.inserir(servico)
        return servico

    def test_cadastrar_completo(self):
        with patch("builtins.input", side_effect=[
            "99",
            "Serviço de teste",
            "Teste",
            "Descrição do serviço de teste",
            "Doc A; Doc B",
            "Unidade Central",
            "https://exemplo.gov.br",
            "teste, ajuda",
            "2026-11-05",
        ]):
            with redirect_stdout(io.StringIO()):
                alterou = cadastrar(self.lista)

        self.assertTrue(alterou)
        servico = self.lista.buscar_por_id(99)
        self.assertIsNotNone(servico)
        self.assertEqual(servico.documentos, ["Doc A", "Doc B"])
        self.assertEqual(servico.palavras_chave, ["teste", "ajuda"])

    def test_cadastrar_id_duplicado(self):
        self._adicionar_teste()
        saida = io.StringIO()

        with patch("builtins.input", side_effect=["99"]):
            with redirect_stdout(saida):
                alterou = cadastrar(self.lista)

        self.assertFalse(alterou)
        self.assertIn("Já existe", saida.getvalue())
        self.assertEqual(self.lista.quantidade, 1)

    def test_consultar_existente_e_inexistente(self):
        self._adicionar_teste()

        saida = io.StringIO()
        with patch("builtins.input", side_effect=["99"]):
            with redirect_stdout(saida):
                consultar(self.lista)
        self.assertIn("Serviço de teste", saida.getvalue())

        saida = io.StringIO()
        with patch("builtins.input", side_effect=["100"]):
            with redirect_stdout(saida):
                consultar(self.lista)
        self.assertIn("não encontrado", saida.getvalue())

    def test_pesquisar_com_e_sem_resultado(self):
        self._adicionar_teste()

        saida = io.StringIO()
        with patch("builtins.input", side_effect=["teste"]):
            with redirect_stdout(saida):
                pesquisar(self.lista)
        self.assertIn("1 resultado", saida.getvalue())

        saida = io.StringIO()
        with patch("builtins.input", side_effect=["inexistente"]):
            with redirect_stdout(saida):
                pesquisar(self.lista)
        self.assertIn("Nenhum registro encontrado", saida.getvalue())

    def test_atualizar_mantendo_campos_com_enter(self):
        self._adicionar_teste()

        with patch("builtins.input", side_effect=[
            "99",
            "Serviço atualizado",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]):
            with redirect_stdout(io.StringIO()):
                alterou = atualizar(self.lista)

        self.assertTrue(alterou)
        servico = self.lista.buscar_por_id(99)
        self.assertEqual(servico.titulo, "Serviço atualizado")
        self.assertEqual(servico.categoria, "Teste")
        self.assertEqual(servico.documentos, ["Doc A", "Doc B"])

    def test_atualizar_inexistente(self):
        with patch("builtins.input", side_effect=["100"]):
            with redirect_stdout(io.StringIO()):
                self.assertFalse(atualizar(self.lista))

    def test_excluir_confirmando_e_cancelando(self):
        self._adicionar_teste()

        with patch("builtins.input", side_effect=["99", "n"]):
            with redirect_stdout(io.StringIO()):
                self.assertFalse(excluir(self.lista))
        self.assertEqual(self.lista.quantidade, 1)

        with patch("builtins.input", side_effect=["99", "s"]):
            with redirect_stdout(io.StringIO()):
                self.assertTrue(excluir(self.lista))
        self.assertTrue(self.lista.vazia())

    def test_excluir_inexistente(self):
        with patch("builtins.input", side_effect=["100"]):
            with redirect_stdout(io.StringIO()):
                self.assertFalse(excluir(self.lista))

    def test_listar(self):
        self._adicionar_teste()
        saida = io.StringIO()
        with redirect_stdout(saida):
            listar(self.lista)

        self.assertIn("Serviço de teste", saida.getvalue())
        self.assertIn("Total: 1", saida.getvalue())

    def test_listar_lista_vazia(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            listar(self.lista)
        self.assertIn("A lista está vazia", saida.getvalue())

    def test_ordenar_e_analisar_lista_vazia(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            self.assertFalse(ordenar(self.lista))
            analise_servicos(self.lista)

        self.assertIn("Não há o que ordenar", saida.getvalue())
        self.assertIn("Nenhum registro cadastrado", saida.getvalue())


class TestMenuUnificado(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)

        self.lista = ListaEncadeada()
        self.lista.inserir(criar_servico(
            1,
            "Fazer o Cartão Nacional de Saúde (Cartão SUS)",
            "Saúde",
            palavras_chave=["cartao sus", "cartao do sus", "sus"],
        ))
        self.base = BaseConhecimento(self.lista)
        self.assistente = Assistente(
            "Citizen Assist AI",
            self.base,
            os.path.join(self.temporaria.name, "historico.json"),
            os.path.join(self.temporaria.name, "atendimentos.csv"),
        )
        self.caminho_servicos = os.path.join(
            self.temporaria.name, "servicos.json"
        )

    def test_fluxo_do_menu_principal(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=[
            "3", "cartao",
            "7", "1",
            "8",
            "11",
            "12",
            "0",
            "5",
        ]):
            with redirect_stdout(saida):
                executar_menu(
                    self.lista, self.assistente, self.caminho_servicos
                )

        texto = saida.getvalue()
        self.assertIn("1 resultado(s)", texto)
        self.assertIn("Selection Sort", texto)
        self.assertIn("Análise dos serviços cadastrados", texto)
        self.assertIn("Indicadores de atendimento", texto)
        self.assertIn("CSV exportado", texto)
        self.assertIn("Obrigado por usar o Citizen Assist AI", texto)

        self.assertEqual(len(carregar_servicos(self.caminho_servicos)), 1)

    def test_menu_recusa_opcao_inexistente(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["14", "0", "5"]):
            with redirect_stdout(saida):
                executar_menu(
                    self.lista, self.assistente, self.caminho_servicos
                )

        self.assertIn("Entrada inválida. Digite um número de 0 a 13.",
                      saida.getvalue())

    def test_menu_abre_o_agente_de_documentos(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["13", "0", "0", "5"]):
            with redirect_stdout(saida):
                executar_menu(
                    self.lista, self.assistente, self.caminho_servicos
                )

        texto = saida.getvalue()
        self.assertIn("Agente de Documentos Pessoais", texto)
        self.assertIn("Sessão encerrada", texto)
        self.assertIn("Nenhuma pergunta foi armazenada", texto)

if __name__ == "__main__":
    unittest.main(verbosity=2)
