import io
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from mobile import servir, transcricao


class RespostaFalsa:
    def __init__(self, dados=b'{"text": "Como fa\u00e7o o cart\u00e3o do SUS?"}'):
        self.dados = dados

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.dados


class TestConfigASR(unittest.TestCase):

    def setUp(self):
        self.ambiente = patch.dict(os.environ, {}, clear=True)
        self.ambiente.start()
        self.addCleanup(self.ambiente.stop)

    def test_sem_chave_fica_indisponivel(self):
        config = transcricao.config_do_ambiente()
        self.assertFalse(config.pronto)
        self.assertIn("OPENAI_API_KEY", config.aviso)

    def test_openai_ativa(self):
        os.environ["OPENAI_API_KEY"] = "chave-teste"
        config = transcricao.config_do_ambiente()
        self.assertTrue(config.pronto)
        self.assertEqual(config.provedor, "openai")
        self.assertEqual(config.modelo, transcricao.MODELO_PADRAO_OPENAI)

    def test_groq_ativa_quando_nao_ha_openai(self):
        os.environ["GROQ_API_KEY"] = "chave-teste"
        config = transcricao.config_do_ambiente()
        self.assertTrue(config.pronto)
        self.assertEqual(config.provedor, "groq")

    def test_openai_tem_prioridade_no_auto(self):
        os.environ["OPENAI_API_KEY"] = "chave-openai"
        os.environ["GROQ_API_KEY"] = "chave-groq"
        config = transcricao.config_do_ambiente()
        self.assertEqual(config.provedor, "openai")

    def test_provider_off_desativa(self):
        os.environ["OPENAI_API_KEY"] = "chave-teste"
        os.environ["ASR_PROVIDER"] = "off"
        config = transcricao.config_do_ambiente()
        self.assertFalse(config.pronto)
        self.assertIn("desativada", config.aviso.lower())

    def test_provider_desconhecido_nao_quebra(self):
        os.environ["ASR_PROVIDER"] = "inexistente"
        config = transcricao.config_do_ambiente()
        self.assertFalse(config.pronto)
        self.assertIn("desconhecido", config.aviso.lower())

    def test_status_nao_expoe_chave(self):
        os.environ["OPENAI_API_KEY"] = "segredo-que-nao-pode-vazar"
        dados = transcricao.status()
        self.assertNotIn("chave", dados)
        self.assertNotIn("segredo-que-nao-pode-vazar", str(dados))
        self.assertTrue(dados["pronto"])


class TestTranscricao(unittest.TestCase):

    def setUp(self):
        self.ambiente = patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "chave-teste",
                "OPENAI_TRANSCRIBE_MODEL": "whisper-1",
                "OPENAI_BASE_URL": "https://api.openai.com/v1",
            },
            clear=True,
        )
        self.ambiente.start()
        self.addCleanup(self.ambiente.stop)

    def test_envia_audio_e_devolve_texto(self):
        with patch.object(transcricao, "urlopen", return_value=RespostaFalsa()) as chamada:
            texto = transcricao.transcrever(b"audio-falso", "audio/webm")

        self.assertIn("cartão do SUS", texto)
        requisicao = chamada.call_args.args[0]
        self.assertEqual(
            requisicao.full_url,
            "https://api.openai.com/v1/audio/transcriptions",
        )
        self.assertEqual(requisicao.headers["Authorization"], "Bearer chave-teste")
        self.assertIn("multipart/form-data", requisicao.headers["Content-type"])
        corpo = requisicao.data
        self.assertIn(b'name="model"', corpo)
        self.assertIn(b"whisper-1", corpo)
        self.assertIn(b'name="language"', corpo)
        self.assertIn(b"audio-falso", corpo)
        self.assertIn(b'filename="audio.webm"', corpo)

    def test_extensao_m4a(self):
        with patch.object(transcricao, "urlopen", return_value=RespostaFalsa()) as chamada:
            transcricao.transcrever(b"audio", "audio/mp4")
        self.assertIn(b'filename="audio.m4a"', chamada.call_args.args[0].data)

    def test_recusa_audio_vazio(self):
        with self.assertRaises(transcricao.ASRValidationError):
            transcricao.transcrever(b"")

    def test_recusa_audio_grande(self):
        with self.assertRaises(transcricao.ASRValidationError):
            transcricao.transcrever(b"a" * (transcricao.LIMITE_AUDIO + 1))

    def test_recusa_tipo_que_nao_e_audio(self):
        with self.assertRaises(transcricao.ASRValidationError):
            transcricao.transcrever(b"texto", "text/plain")

    def test_chave_recusada_vira_mensagem_clara(self):
        erro = HTTPError(
            "https://api.openai.com/v1/audio/transcriptions",
            401,
            "Unauthorized",
            {},
            io.BytesIO(b"erro"),
        )
        with patch.object(transcricao, "urlopen", side_effect=erro):
            with self.assertRaises(transcricao.ASRError) as contexto:
                transcricao.transcrever(b"audio")
        self.assertIn("chave", str(contexto.exception).lower())

    def test_limite_de_requisicoes_vira_mensagem_clara(self):
        erro = HTTPError(
            "https://api.openai.com/v1/audio/transcriptions",
            429,
            "Too Many Requests",
            {},
            io.BytesIO(b"erro"),
        )
        with patch.object(transcricao, "urlopen", side_effect=erro):
            with self.assertRaises(transcricao.ASRError) as contexto:
                transcricao.transcrever(b"audio")
        self.assertIn("aguarde", str(contexto.exception).lower())

    def test_falha_de_rede_vira_mensagem_clara(self):
        with patch.object(transcricao, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(transcricao.ASRError) as contexto:
                transcricao.transcrever(b"audio")
        self.assertIn("internet", str(contexto.exception).lower())

    def test_resposta_sem_texto_vira_erro(self):
        with patch.object(
            transcricao, "urlopen", return_value=RespostaFalsa(b'{"text": ""}')
        ):
            with self.assertRaises(transcricao.ASRError):
                transcricao.transcrever(b"audio")


class TestLimiteDoServidorASR(unittest.TestCase):

    def setUp(self):
        servir.ASR_REQUISICOES.clear()
        self.addCleanup(servir.ASR_REQUISICOES.clear)

    def test_limita_requisicoes_por_ip(self):
        for _ in range(servir.LIMITE_ASR_POR_MINUTO):
            self.assertTrue(servir.asr_permitido("127.0.0.1"))
        self.assertFalse(servir.asr_permitido("127.0.0.1"))
        self.assertTrue(servir.asr_permitido("192.168.0.2"))


if __name__ == "__main__":
    unittest.main()
