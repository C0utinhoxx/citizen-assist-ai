"""Testes do carregamento das fichas FC-01 a FC-07."""

import os
import tempfile
import unittest

from agente.fichas import (
    IDS_OBRIGATORIOS,
    ErroFicha,
    carregar_ficha,
    carregar_fichas,
)


class TestFichas(unittest.TestCase):

    def test_carrega_as_sete_fichas(self):
        fichas = carregar_fichas()
        self.assertEqual(sorted(fichas), list(IDS_OBRIGATORIOS))

    def test_toda_ficha_tem_fonte_e_verificacao(self):
        for ficha in carregar_fichas().values():
            self.assertTrue(ficha.fonte, ficha.id)
            self.assertTrue(ficha.verificado_em, ficha.id)
            self.assertTrue(ficha.palavras_chave, ficha.id)
            self.assertGreaterEqual(len(ficha.secoes), 1, ficha.id)

    def test_fichas_atuais_estao_marcadas_como_provisorias(self):
        # Quando as fichas oficiais forem adicionadas, este teste deve ser
        # ajustado para refletir o novo material.
        for ficha in carregar_fichas().values():
            self.assertTrue(ficha.provisoria, ficha.id)

    def test_nenhuma_ficha_tem_dado_pessoal(self):
        from agente.seguranca import contem_pii

        for ficha in carregar_fichas().values():
            self.assertFalse(contem_pii(ficha.texto_completo()), ficha.id)

    def test_rejeita_ficha_sem_fonte(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "FC-01_teste.md")
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(
                    "# FC-01 — Teste\n\n- **Data de verificação:** 2026-01-01\n\n"
                    "## Seção\nTexto.\n"
                )
            with self.assertRaises(ErroFicha):
                carregar_ficha(caminho)

    def test_rejeita_ficha_sem_secao(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "FC-01_teste.md")
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(
                    "# FC-01 — Teste\n\n- **Fonte:** teste\n"
                    "- **Data de verificação:** 2026-01-01\n"
                )
            with self.assertRaises(ErroFicha):
                carregar_ficha(caminho)

    def test_rejeita_pasta_sem_as_sete(self):
        with tempfile.TemporaryDirectory() as pasta:
            with self.assertRaises(ErroFicha):
                carregar_fichas(pasta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
