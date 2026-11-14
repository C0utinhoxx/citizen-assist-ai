import unittest
from pathlib import Path

from app.base_conhecimento import PONTOS_MEDIA, BaseConhecimento
from app.lista_encadeada import ListaEncadeada
from app.persistencia import carregar_servicos
from testes.apoio import criar_servico

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO_DADOS = RAIZ / "data" / "base_conhecimento.json"


class TestBaseConhecimento(unittest.TestCase):

    def setUp(self):
        self.lista = ListaEncadeada()
        for servico in carregar_servicos(str(ARQUIVO_DADOS)):
            self.lista.inserir(servico)
        self.base = BaseConhecimento(self.lista)

    def test_dados_unificados(self):
        self.assertEqual(self.lista.quantidade, 12)

        ids = [servico.id for servico in self.lista.percorrer()]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, list(range(1, 13)))

        for servico in self.lista.percorrer():
            self.assertTrue(servico.titulo)
            self.assertTrue(servico.categoria)
            self.assertTrue(servico.descricao)
            self.assertTrue(servico.documentos)
            self.assertTrue(servico.local)
            self.assertTrue(servico.fonte)
            self.assertGreaterEqual(len(servico.palavras_chave), 3)
            self.assertTrue(servico.verificado_em)

    def test_categorias_ordenadas(self):
        self.assertEqual(
            self.base.categorias(),
            ["Direitos e Benefícios", "Documentos", "Saúde", "Transporte"],
        )

    def test_por_categoria_ignora_acento_e_maiuscula(self):
        saude = self.base.por_categoria("saude")
        self.assertEqual(len(saude), 3)
        self.assertTrue(all(s.categoria == "Saúde" for s in saude))

    def test_pontuacao_da_duvida_do_cartao_sus(self):
        resultados = self.base.buscar("Como faço o cartão do SUS?")

        self.assertTrue(resultados)
        pontos, servico = resultados[0]
        self.assertEqual(servico.id, 1)
        self.assertEqual(pontos, 7)

    def test_busca_sem_resultado_e_busca_vazia(self):
        self.assertEqual(self.base.buscar("xyz"), [])
        self.assertEqual(self.base.buscar(""), [])
        self.assertEqual(self.base.buscar("   "), [])

    def test_ranking_fica_em_ordem_decrescente(self):
        resultados = self.base.buscar("cartao")

        self.assertTrue(resultados)
        pontos = [item[0] for item in resultados]
        self.assertEqual(pontos, sorted(pontos, reverse=True))

    def test_empate_desempata_pelo_menor_id(self):
        lista = ListaEncadeada()
        lista.inserir(criar_servico(
            2, "Teste de busca", "Geral", palavras_chave=["teste"]
        ))
        lista.inserir(criar_servico(
            1, "Teste de busca", "Geral", palavras_chave=["teste"]
        ))
        base = BaseConhecimento(lista)

        resultados = base.buscar("teste")
        self.assertEqual([servico.id for _, servico in resultados], [1, 2])
        self.assertEqual([pontos for pontos, _ in resultados], [4, 4])

    def test_palavra_chave_nao_casa_pedaco_de_palavra(self):
        servico = criar_servico(
            1, "Outro assunto", "Geral", palavras_chave=["sus"]
        )
        self.assertEqual(self.base.pontuar("suspiro", servico), 0)

    def test_titulo_tambem_pontua(self):
        servico = criar_servico(
            1, "Cartão de Saúde", "Geral", palavras_chave=[]
        )
        self.assertEqual(self.base.pontuar("cartao", servico), 1)
        self.assertLess(
            self.base.pontuar("cartao", servico), PONTOS_MEDIA
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
