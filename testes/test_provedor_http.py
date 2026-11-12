import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

from agente.provedor import ErroProvedor, criar_provedor
from avaliacao.juiz import JuizLLM


class _Handler(BaseHTTPRequestHandler):
    resposta_texto = "resposta do modelo"
    ultimo_corpo = None
    ultimo_cabecalho = None
    forcar_erro = False

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", "0"))
        corpo = self.rfile.read(tamanho).decode("utf-8")
        type(self).ultimo_corpo = json.loads(corpo)
        type(self).ultimo_cabecalho = dict(self.headers)

        if type(self).forcar_erro:
            conteudo = json.dumps({"error": "falha simulada"}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(conteudo)))
            self.end_headers()
            self.wfile.write(conteudo)
            return

        dados = {
            "choices": [
                {"message": {"content": type(self).resposta_texto}}
            ]
        }
        conteudo = json.dumps(dados).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)

    def log_message(self, formato, *args):
        pass


class TestProvedorHTTP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.servidor = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.porta = cls.servidor.server_address[1]
        cls.thread = threading.Thread(
            target=cls.servidor.serve_forever, daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()
        cls.thread.join(timeout=2)

    def _ambiente(self):
        return {
            "CITIZEN_LLM_PROVIDER": "openai",
            "OPENAI_API_KEY": "chave-de-teste",
            "CITIZEN_LLM_BASE_URL": f"http://127.0.0.1:{self.porta}/v1",
            "CITIZEN_LLM_MODEL": "modelo-de-teste",
        }

    def test_gerar_envia_mensagens_e_le_resposta(self):
        _Handler.resposta_texto = "R$ 38,00 (FC-01)"
        with patch.dict("os.environ", self._ambiente(), clear=False):
            provedor = criar_provedor()
            self.assertIsNotNone(provedor)
            texto = provedor.gerar("sistema", "pergunta")

        self.assertEqual(texto, "R$ 38,00 (FC-01)")
        corpo = _Handler.ultimo_corpo
        self.assertEqual(corpo["model"], "modelo-de-teste")
        self.assertEqual(corpo["messages"][0]["role"], "system")
        self.assertEqual(corpo["messages"][1]["content"], "pergunta")
        self.assertEqual(
            _Handler.ultimo_cabecalho.get("Authorization"),
            "Bearer chave-de-teste",
        )

    def test_erro_http_vira_erro_provedor(self):
        with patch.dict("os.environ", self._ambiente(), clear=False):
            provedor = criar_provedor()

        _Handler.forcar_erro = True
        try:
            with self.assertRaises(ErroProvedor):
                provedor.gerar("sistema", "pergunta")
        finally:
            _Handler.forcar_erro = False

    def test_juiz_llm_com_provedor_http(self):
        _Handler.resposta_texto = (
            '{"nota": 0.5, "justificativa": "parcial", '
            '"criterios": {"fatos": true}}'
        )
        with patch.dict("os.environ", self._ambiente(), clear=False):
            provedor = criar_provedor()

        juiz = JuizLLM(provedor)
        caso = {
            "id": 1,
            "tipo": "Escopo",
            "mensagem": "Quanto custa a segunda via do RG?",
            "resposta_esperada": "R$ 38,00 (FC-01)",
            "ficha_obrigatoria": "FC-01",
            "fatos_esperados": ["38 00"],
            "fatos_proibidos": [],
        }
        avaliacao = juiz.avaliar(caso, "Custa R$ 38,00. (FC-01)")
        self.assertEqual(avaliacao.nota, 0.5)
        self.assertEqual(avaliacao.juiz, "llm")

if __name__ == "__main__":
    unittest.main(verbosity=2)
