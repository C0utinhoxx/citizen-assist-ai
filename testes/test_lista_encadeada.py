"""Testes da lista encadeada, da busca, da remoção e do Selection Sort."""

import unittest

from app.lista_encadeada import ListaEncadeada
from testes.apoio import criar_servico


class TestListaEncadeada(unittest.TestCase):

    def setUp(self):
        self.lista = ListaEncadeada()
        self.lista.inserir(criar_servico(2, "Vacina", "Saúde"))
        self.lista.inserir(criar_servico(1, "Cartão SUS", "Saúde"))
        self.lista.inserir(criar_servico(3, "CPF", "Documentos"))

    def _ids(self):
        return [servico.id for servico in self.lista.percorrer()]

    def _tamanho_da_corrente(self):
        atual = self.lista.inicio
        visitados = 0
        while atual is not None:
            visitados += 1
            atual = atual.proximo
        return visitados

    def test_lista_vazia(self):
        lista = ListaEncadeada()

        self.assertTrue(lista.vazia())
        self.assertEqual(lista.quantidade, 0)
        self.assertEqual(lista.listar(), [])
        self.assertIsNone(lista.buscar_por_id(1))
        self.assertFalse(lista.remover(1))
        self.assertEqual(lista.pesquisar("qualquer"), [])

    def test_inserir_no_fim_e_buscar_por_id(self):
        self.assertEqual(self._ids(), [2, 1, 3])
        self.assertEqual(self.lista.quantidade, 3)

        servico = self.lista.buscar_por_id(3)
        self.assertIsNotNone(servico)
        self.assertEqual(servico.titulo, "CPF")
        self.assertIsNone(self.lista.buscar_por_id(99))

    def test_estrutura_encadeada_fica_integra(self):
        self.assertEqual(self._tamanho_da_corrente(), self.lista.quantidade)
        self.assertEqual(self._ids(), [2, 1, 3])

    def test_id_duplicado_e_recusado(self):
        resultado = self.lista.inserir(criar_servico(1, "Repetido"))

        self.assertFalse(resultado)
        self.assertEqual(self.lista.quantidade, 3)
        self.assertEqual(self.lista.buscar_por_id(1).titulo, "Cartão SUS")

    def test_pesquisar_titulo_categoria_e_descricao(self):
        self.assertEqual(len(self.lista.pesquisar("vacina")), 1)
        self.assertEqual(len(self.lista.pesquisar("documentos")), 1)
        self.assertEqual(len(self.lista.pesquisar("saude")), 2)
        self.assertEqual(len(self.lista.pesquisar("descricao")), 3)
        self.assertEqual(self.lista.pesquisar("inexistente"), [])
        self.assertEqual(self.lista.pesquisar("   "), [])

    def test_atualizar(self):
        servico = self.lista.atualizar(2, titulo="Vacina da gripe", local="Posto")

        self.assertEqual(servico.titulo, "Vacina da gripe")
        self.assertEqual(servico.local, "Posto")
        self.assertIsNone(self.lista.atualizar(99, titulo="Nada"))
        self.assertEqual(self.lista.buscar_por_id(2).local, "Posto")

    def test_atualizar_campo_invalido(self):
        with self.assertRaises(ValueError):
            self.lista.atualizar(1, desconhecido="valor")

    def test_remover_inicio_meio_fim(self):
        self.assertTrue(self.lista.remover(2))
        self.assertEqual(self._ids(), [1, 3])
        self.assertEqual(self._tamanho_da_corrente(), 2)

        self.assertTrue(self.lista.remover(3))
        self.assertEqual(self._ids(), [1])
        self.assertEqual(self._tamanho_da_corrente(), 1)

        self.assertTrue(self.lista.remover(1))
        self.assertTrue(self.lista.vazia())
        self.assertEqual(self.lista.quantidade, 0)

    def test_remover_inexistente(self):
        self.assertFalse(self.lista.remover(99))
        self.assertEqual(self.lista.quantidade, 3)

    def test_ordenar_por_titulo(self):
        self.lista.ordenar_por("titulo")
        titulos = [servico.titulo for servico in self.lista.percorrer()]

        self.assertEqual(titulos, ["Cartão SUS", "CPF", "Vacina"])

    def test_ordenar_por_categoria_e_id(self):
        self.lista.ordenar_por("categoria")
        categorias = [servico.categoria for servico in self.lista.percorrer()]
        self.assertEqual(categorias, ["Documentos", "Saúde", "Saúde"])

        self.lista.ordenar_por("id")
        self.assertEqual(self._ids(), [1, 2, 3])

    def test_ordenar_lista_vazia(self):
        lista = ListaEncadeada()
        lista.ordenar_por("titulo")
        self.assertTrue(lista.vazia())

    def test_ordenar_campo_invalido(self):
        with self.assertRaises(ValueError):
            self.lista.ordenar_por("local")

    def test_contar_por_categoria(self):
        contagem = self.lista.contar_por_categoria()

        self.assertEqual(contagem["Saúde"], 2)
        self.assertEqual(contagem["Documentos"], 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
