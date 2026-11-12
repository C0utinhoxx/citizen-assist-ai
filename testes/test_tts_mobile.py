import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from mobile import servir, tts


class RespostaFalsa:
    def __init__(self, dados=b"ID3audio"):
        self.dados = dados

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.dados


class TestConfigTTS(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)
        self.ambiente = patch.dict(
            os.environ,
            {"TTS_CACHE_DIR": self.temporaria.name, "TTS_MOCK_FORCAR_TOM": "1"},
            clear=True,
        )
        self.ambiente.start()
        self.addCleanup(self.ambiente.stop)

    def test_sem_chave_usa_modo_de_teste(self):
        config = tts.config_do_ambiente()
        self.assertEqual(config.provedor, "mock")
        self.assertEqual(config.modo, "teste")
        self.assertTrue(config.pronto)
        self.assertIn("teste", config.aviso.lower())

    def test_chave_ativa_azure(self):
        os.environ["AZURE_SPEECH_KEY"] = "chave-teste"
        os.environ["AZURE_SPEECH_REGION"] = "brazilsouth"
        config = tts.config_do_ambiente()
        self.assertEqual(config.provedor, "azure")
        self.assertEqual(config.modo, "real")
        self.assertTrue(config.pronto)
        self.assertEqual(config.regiao, "brazilsouth")
        self.assertEqual(config.voz, tts.VOZ_PADRAO)

    def test_provider_mock_ignora_chave(self):
        os.environ["AZURE_SPEECH_KEY"] = "chave-teste"
        os.environ["TTS_PROVIDER"] = "mock"
        config = tts.config_do_ambiente()
        self.assertEqual(config.provedor, "mock")

    def test_azure_sem_chave_cai_no_modo_de_teste(self):
        os.environ["TTS_PROVIDER"] = "azure"
        config = tts.config_do_ambiente()
        self.assertEqual(config.provedor, "mock")
        self.assertIn("AZURE_SPEECH_KEY", config.aviso)

    def test_google_fica_indisponivel_por_enquanto(self):
        os.environ["TTS_PROVIDER"] = "google"
        config = tts.config_do_ambiente()
        self.assertFalse(config.pronto)
        self.assertIn("Google", config.aviso)

    def test_status_nao_expoe_chave(self):
        os.environ["AZURE_SPEECH_KEY"] = "segredo-que-nao-pode-vazar"
        dados = tts.status()
        self.assertNotIn("chave", dados)
        self.assertNotIn("segredo-que-nao-pode-vazar", str(dados))

    def test_voz_invalida_volta_para_thalita(self):
        self.assertEqual(tts.normalizar_voz("voz-inexistente"), tts.VOZ_PADRAO)
        self.assertEqual(tts.normalizar_voz("pt-BR-MacerioNeural"), "pt-BR-MacerioNeural")

    def test_lista_de_vozes_tem_thalita_como_padrao(self):
        vozes = tts.listar_vozes()
        self.assertTrue(any(v["id"] == "pt-BR-ThalitaNeural" for v in vozes))
        thalita = next(v for v in vozes if v["id"] == "pt-BR-ThalitaNeural")
        self.assertTrue(thalita["padrao"])

    def test_formato_define_o_tipo_de_audio(self):
        base = dict(provedor="azure", modo="real", pronto=True, voz=tts.VOZ_PADRAO)
        self.assertEqual(
            tts._tipo_saida(tts.ConfigTTS(formato="riff-24khz-16bit-mono-pcm", **base)),
            ("audio/wav", "wav"),
        )
        self.assertEqual(
            tts._tipo_saida(tts.ConfigTTS(formato="ogg-16khz-16bit-mono-opus", **base)),
            ("audio/ogg", "ogg"),
        )
        self.assertEqual(
            tts._tipo_saida(tts.ConfigTTS(formato=tts.FORMATO_PADRAO, **base)),
            ("audio/mpeg", "mp3"),
        )


class TestTextoTTS(unittest.TestCase):

    def test_limpa_espacos(self):
        self.assertEqual(tts.limpar_texto("  Olá \n  mundo  "), "Olá mundo")

    def test_recusa_texto_vazio(self):
        with self.assertRaises(tts.TTSValidationError):
            tts.limpar_texto("   ")

    def test_recusa_texto_longo(self):
        with self.assertRaises(tts.TTSValidationError):
            tts.limpar_texto("a" * (tts.LIMITE_CARACTERES + 1))

    def test_ssml_escapa_caracteres(self):
        ssml = tts._montar_ssml("Tom & Jerry <3", "pt-BR-ThalitaNeural")
        self.assertIn("Tom &amp; Jerry &lt;3", ssml)
        self.assertIn('name="pt-BR-ThalitaNeural"', ssml)

    def test_ssml_nao_aceita_voz_arbitraria(self):
        ssml = tts._montar_ssml("Olá", '"><script>alert(1)</script>')
        self.assertIn('name="%s"' % tts.VOZ_PADRAO, ssml)
        self.assertNotIn("script", ssml)


class TestSinteseMock(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)
        self.ambiente = patch.dict(
            os.environ,
            {"TTS_CACHE_DIR": self.temporaria.name, "TTS_MOCK_FORCAR_TOM": "1"},
            clear=True,
        )
        self.ambiente.start()
        self.addCleanup(self.ambiente.stop)

    def test_gera_wav_e_usa_cache(self):
        primeiro = tts.sintetizar("Olá, cidadão.", "pt-BR-ThalitaNeural")
        self.assertEqual(primeiro.content_type, "audio/wav")
        self.assertEqual(primeiro.provedor, "mock")
        self.assertFalse(primeiro.cache)
        self.assertGreater(len(primeiro.audio), 44)

        segundo = tts.sintetizar("Olá, cidadão.", "pt-BR-ThalitaNeural")
        self.assertTrue(segundo.cache)
        self.assertEqual(segundo.audio, primeiro.audio)

    def test_cache_separa_vozes(self):
        primeiro = tts.sintetizar("Olá", "pt-BR-ThalitaNeural")
        segundo = tts.sintetizar("Olá", "pt-BR-MacerioNeural")
        self.assertFalse(segundo.cache)
        self.assertEqual(segundo.voz, "pt-BR-MacerioNeural")
        self.assertGreater(len(primeiro.audio), 44)
        self.assertGreater(len(segundo.audio), 44)


class TestSinteseAzure(unittest.TestCase):

    def setUp(self):
        self.temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaria.cleanup)
        self.ambiente = patch.dict(
            os.environ,
            {
                "TTS_CACHE_DIR": self.temporaria.name,
                "TTS_PROVIDER": "azure",
                "AZURE_SPEECH_KEY": "chave-teste",
                "AZURE_SPEECH_REGION": "brazilsouth",
                "AZURE_TTS_VOICE": "pt-BR-ThalitaNeural",
            },
            clear=True,
        )
        self.ambiente.start()
        self.addCleanup(self.ambiente.stop)

    def test_envia_ssml_e_devolve_mp3(self):
        with patch.object(tts, "urlopen", return_value=RespostaFalsa()) as chamada:
            resultado = tts.sintetizar("Olá & bem-vindo", "pt-BR-MacerioNeural")

        requisicao = chamada.call_args.args[0]
        self.assertEqual(
            requisicao.full_url,
            "https://brazilsouth.tts.speech.microsoft.com/cognitiveservices/v1",
        )
        self.assertEqual(
            requisicao.headers["Ocp-apim-subscription-key"], "chave-teste"
        )
        self.assertEqual(
            requisicao.headers["X-microsoft-outputformat"],
            tts.FORMATO_PADRAO,
        )
        corpo = requisicao.data.decode("utf-8")
        self.assertIn('name="pt-BR-MacerioNeural"', corpo)
        self.assertIn("Olá &amp; bem-vindo", corpo)
        self.assertEqual(resultado.content_type, "audio/mpeg")
        self.assertEqual(resultado.extensao, "mp3")
        self.assertEqual(resultado.provedor, "azure")
        self.assertFalse(resultado.cache)

    def test_chave_recusada_vira_mensagem_clara(self):
        erro = HTTPError(
            "https://brazilsouth.tts.speech.microsoft.com/cognitiveservices/v1",
            401,
            "Unauthorized",
            {},
            io.BytesIO(b"erro"),
        )
        with patch.object(tts, "urlopen", side_effect=erro):
            with self.assertRaises(tts.TTSError) as contexto:
                tts.sintetizar("Olá")
        self.assertIn("chave", str(contexto.exception).lower())

    def test_limite_de_requisicoes_vira_mensagem_clara(self):
        erro = HTTPError(
            "https://brazilsouth.tts.speech.microsoft.com/cognitiveservices/v1",
            429,
            "Too Many Requests",
            {},
            io.BytesIO(b"erro"),
        )
        with patch.object(tts, "urlopen", side_effect=erro):
            with self.assertRaises(tts.TTSError) as contexto:
                tts.sintetizar("Olá")
        self.assertIn("aguarde", str(contexto.exception).lower())


class TestLimiteDoServidor(unittest.TestCase):

    def setUp(self):
        servir.TTS_REQUISICOES.clear()
        self.addCleanup(servir.TTS_REQUISICOES.clear)

    def test_limita_requisicoes_por_ip(self):
        for _ in range(servir.LIMITE_TTS_POR_MINUTO):
            self.assertTrue(servir.tts_permitido("127.0.0.1"))
        self.assertFalse(servir.tts_permitido("127.0.0.1"))
        self.assertTrue(servir.tts_permitido("192.168.0.2"))

    def test_bloqueia_download_de_env_e_cache(self):
        handler = servir.Handler.__new__(servir.Handler)
        handler.directory = str(servir.RAIZ)
        self.assertIn("__arquivo_privado__", handler.translate_path("/.env"))
        self.assertIn("__arquivo_privado__", handler.translate_path("/.cache/tts/a.wav"))
        self.assertIn("__arquivo_privado__", handler.translate_path("/%2e%2e/.env"))
        self.assertTrue(handler.translate_path("/index.html").endswith("index.html"))


class TestCarregarEnv(unittest.TestCase):

    def test_le_arquivo_env_sem_sobrescrever_ambiente(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / ".env"
            caminho.write_text(
                "AZURE_SPEECH_KEY=do-arquivo\nTTS_PROVIDER=azure\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"AZURE_SPEECH_KEY": "do-sistema"}, clear=True):
                tts.carregar_env(caminho)
                self.assertEqual(os.environ["AZURE_SPEECH_KEY"], "do-sistema")
                self.assertEqual(os.environ["TTS_PROVIDER"], "azure")

if __name__ == "__main__":
    unittest.main()
