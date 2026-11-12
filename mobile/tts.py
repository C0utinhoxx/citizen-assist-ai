#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import io
import math
import os
import shutil
import struct
import subprocess
import tempfile
import threading
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

LIMITE_CARACTERES = 600
VOZ_PADRAO = "pt-BR-ThalitaNeural"
REGIAO_PADRAO = "brazilsouth"
FORMATO_PADRAO = "audio-24khz-48kbitrate-mono-mp3"

CACHE_LOCK = threading.Lock()

VOZES_AZURE: List[Dict[str, str]] = [
    {"id": "pt-BR-ThalitaNeural", "nome": "Thalita", "genero": "feminina"},
    {"id": "pt-BR-MacerioNeural", "nome": "Macerio", "genero": "masculina"},
    {"id": "pt-BR-FranciscaNeural", "nome": "Francisca", "genero": "feminina"},
    {"id": "pt-BR-AntonioNeural", "nome": "Antonio", "genero": "masculino"},
    {"id": "pt-BR-BrendaNeural", "nome": "Brenda", "genero": "feminina"},
    {"id": "pt-BR-DonatoNeural", "nome": "Donato", "genero": "masculino"},
    {"id": "pt-BR-ElzaNeural", "nome": "Elza", "genero": "feminina"},
    {"id": "pt-BR-FabioNeural", "nome": "Fabio", "genero": "masculino"},
    {"id": "pt-BR-GiovannaNeural", "nome": "Giovanna", "genero": "feminina"},
    {"id": "pt-BR-HumbertoNeural", "nome": "Humberto", "genero": "masculino"},
    {"id": "pt-BR-JulioNeural", "nome": "Julio", "genero": "masculino"},
    {"id": "pt-BR-LeilaNeural", "nome": "Leila", "genero": "feminina"},
    {"id": "pt-BR-LeticiaNeural", "nome": "Leticia", "genero": "feminina"},
    {"id": "pt-BR-ManuelaNeural", "nome": "Manuela", "genero": "feminina"},
    {"id": "pt-BR-NicolauNeural", "nome": "Nicolau", "genero": "masculino"},
    {"id": "pt-BR-YaraNeural", "nome": "Yara", "genero": "feminina"},
]
IDS_VOZES_AZURE = {v["id"] for v in VOZES_AZURE}


class TTSError(Exception):
    pass


class TTSValidationError(TTSError):
    pass


class TTSConfigError(TTSError):
    pass

@dataclass
class ConfigTTS:
    provedor: str
    modo: str
    pronto: bool
    voz: str
    regiao: str = ""
    formato: str = FORMATO_PADRAO
    chave: str = ""
    aviso: str = ""

    def para_status(self) -> Dict[str, object]:
        return {
            "provedor": self.provedor,
            "modo": self.modo,
            "pronto": self.pronto,
            "voz": self.voz,
            "regiao": self.regiao,
            "limite_caracteres": LIMITE_CARACTERES,
            "aviso": self.aviso,
        }

@dataclass
class ResultadoTTS:
    audio: bytes
    content_type: str
    extensao: str
    cache: bool
    provedor: str
    modo: str
    voz: str


def carregar_env(caminho: Path) -> None:
    try:
        linhas = caminho.read_text(encoding="utf-8").splitlines()
    except OSError:
        return

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        if chave and not os.environ.get(chave):
            os.environ[chave] = valor


def config_do_ambiente() -> ConfigTTS:
    provedor = os.environ.get("TTS_PROVIDER", "").strip().lower()
    chave = os.environ.get("AZURE_SPEECH_KEY", "").strip()
    regiao = os.environ.get("AZURE_SPEECH_REGION", REGIAO_PADRAO).strip() or REGIAO_PADRAO
    voz = os.environ.get("AZURE_TTS_VOICE", VOZ_PADRAO).strip() or VOZ_PADRAO
    formato = os.environ.get("AZURE_TTS_FORMAT", FORMATO_PADRAO).strip() or FORMATO_PADRAO

    if provedor in ("", "auto"):
        provedor = "azure" if chave else "mock"

    if provedor == "mock":
        return ConfigTTS(
            provedor="mock",
            modo="teste",
            pronto=True,
            voz=voz if voz in IDS_VOZES_AZURE else VOZ_PADRAO,
            aviso="Modo de teste: sem chave do Azure. O áudio serve apenas para validar o fluxo.",
        )

    if provedor == "azure":
        if not chave:
            return ConfigTTS(
                provedor="mock",
                modo="teste",
                pronto=True,
                voz=voz if voz in IDS_VOZES_AZURE else VOZ_PADRAO,
                aviso="Azure sem AZURE_SPEECH_KEY. Usando o modo de teste.",
            )
        return ConfigTTS(
            provedor="azure",
            modo="real",
            pronto=True,
            voz=voz if voz in IDS_VOZES_AZURE else VOZ_PADRAO,
            regiao=regiao,
            formato=formato,
            chave=chave,
        )

    if provedor == "google":
        return ConfigTTS(
            provedor="google",
            modo="indisponivel",
            pronto=False,
            voz="",
            aviso="O adaptador Google Chirp 3 HD ainda não foi ativado. Use Azure ou o modo de teste.",
        )

    return ConfigTTS(
        provedor=provedor or "mock",
        modo="indisponivel",
        pronto=False,
        voz="",
        aviso="Provedor de voz desconhecido: %s" % (provedor or "(vazio)"),
    )


def status() -> Dict[str, object]:
    return config_do_ambiente().para_status()


def listar_vozes() -> List[Dict[str, str]]:
    config = config_do_ambiente()
    if config.provedor not in ("mock", "azure"):
        return []
    vozes = []
    for item in VOZES_AZURE:
        copia = dict(item)
        copia["padrao"] = item["id"] == config.voz
        vozes.append(copia)
    return vozes


def limpar_texto(texto: object) -> str:
    conteudo = " ".join(str(texto or "").split())
    if not conteudo:
        raise TTSValidationError("O texto da resposta está vazio.")
    if len(conteudo) > LIMITE_CARACTERES:
        raise TTSValidationError(
            "O texto tem %s caracteres; o limite é %s."
            % (len(conteudo), LIMITE_CARACTERES)
        )
    return conteudo


def normalizar_voz(voz: Optional[str]) -> str:
    voz = str(voz or "").strip()
    return voz if voz in IDS_VOZES_AZURE else VOZ_PADRAO


def _tipo_saida(config: ConfigTTS) -> Tuple[str, str]:
    if config.provedor == "mock":
        return "audio/wav", "wav"
    formato = (config.formato or "").lower()
    if formato.startswith("riff-") or "pcm" in formato:
        return "audio/wav", "wav"
    if formato.startswith("ogg-"):
        return "audio/ogg", "ogg"
    if formato.startswith("webm-"):
        return "audio/webm", "webm"
    return "audio/mpeg", "mp3"


def _hash_cache(config: ConfigTTS, texto: str, voz: str) -> str:
    base = "\n".join([config.provedor, config.modo, voz, config.formato, texto])
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def _caminho_cache(config: ConfigTTS, texto: str, voz: str) -> Path:
    configurada = os.environ.get("TTS_CACHE_DIR", "").strip()
    if configurada:
        raiz = Path(configurada)
        if not raiz.is_absolute():
            raiz = Path(__file__).resolve().parent / raiz
    else:
        raiz = Path(__file__).resolve().parent / ".cache" / "tts"
    raiz.mkdir(parents=True, exist_ok=True)
    extensao = _tipo_saida(config)[1]
    return raiz / ("%s.%s" % (_hash_cache(config, texto, voz), extensao))


def sintetizar(texto: object, voz: Optional[str] = None) -> ResultadoTTS:
    config = config_do_ambiente()
    if not config.pronto:
        raise TTSConfigError(config.aviso or "A voz natural não está configurada.")

    conteudo = limpar_texto(texto)
    voz_escolhida = normalizar_voz(voz or config.voz)
    caminho = _caminho_cache(config, conteudo, voz_escolhida)

    with CACHE_LOCK:
        if caminho.exists():
            try:
                dados = caminho.read_bytes()
                if dados:
                    return ResultadoTTS(
                        audio=dados,
                        content_type=_tipo_saida(config)[0],
                        extensao=caminho.suffix.lstrip("."),
                        cache=True,
                        provedor=config.provedor,
                        modo=config.modo,
                        voz=voz_escolhida,
                    )
            except OSError:
                pass

    if config.provedor == "mock":
        audio, content_type, extensao = _sintetizar_mock(conteudo)
    elif config.provedor == "azure":
        audio, content_type, extensao = _sintetizar_azure(config, conteudo, voz_escolhida)
    else:
        raise TTSConfigError(config.aviso or "Provedor de voz não configurado.")

    if not audio:
        raise TTSError("O provedor de voz devolveu um áudio vazio.")

    try:
        temporario = caminho.with_suffix(caminho.suffix + ".tmp")
        temporario.write_bytes(audio)
        temporario.replace(caminho)
    except OSError:
        pass

    return ResultadoTTS(
        audio=audio,
        content_type=content_type,
        extensao=extensao,
        cache=False,
        provedor=config.provedor,
        modo=config.modo,
        voz=voz_escolhida,
    )


def _montar_ssml(texto: str, voz: str) -> str:
    voz_segura = normalizar_voz(voz)
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xml:lang="pt-BR"><voice name="%s">%s</voice></speak>'
        % (voz_segura, escape(texto))
    )


def _sintetizar_azure(config: ConfigTTS, texto: str, voz: str) -> Tuple[bytes, str, str]:
    if not config.chave:
        raise TTSConfigError("A chave do Azure não foi configurada.")

    url = "https://%s.tts.speech.microsoft.com/cognitiveservices/v1" % config.regiao
    corpo = _montar_ssml(texto, voz).encode("utf-8")
    requisicao = Request(
        url,
        data=corpo,
        method="POST",
        headers={
            "Ocp-Apim-Subscription-Key": config.chave,
            "Content-Type": "application/ssml+xml; charset=utf-8",
            "X-Microsoft-OutputFormat": config.formato,
            "User-Agent": "CitizenAssistMobile/2.0",
        },
    )

    try:
        with urlopen(requisicao, timeout=15) as resposta:
            audio = resposta.read()
    except HTTPError as exc:
        detalhe = ""
        try:
            detalhe = exc.read().decode("utf-8", "replace")[:300]
        except Exception:
            detalhe = ""
        if exc.code in (401, 403):
            raise TTSError("A chave do Azure não foi aceita. Confira AZURE_SPEECH_KEY e a região.") from exc
        if exc.code == 429:
            raise TTSError("Muitas solicitações de voz em pouco tempo. Aguarde alguns segundos e tente de novo.") from exc
        if exc.code == 400:
            raise TTSError("O Azure recusou o texto ou a voz escolhida. Tente outra voz.") from exc
        raise TTSError("O serviço de voz do Azure falhou (HTTP %s). %s" % (exc.code, detalhe)) from exc
    except URLError as exc:
        raise TTSError("Não consegui falar com o Azure. Verifique a internet e tente de novo.") from exc
    except OSError as exc:
        raise TTSError("A conexão com o Azure foi interrompida. Tente de novo.") from exc

    if not audio:
        raise TTSError("O Azure devolveu um áudio vazio.")
    content_type, extensao = _tipo_saida(config)
    return audio, content_type, extensao


def _sintetizar_mock(texto: str) -> Tuple[bytes, str, str]:
    if os.environ.get("TTS_MOCK_FORCAR_TOM") == "1":
        return _tom_wav(), "audio/wav", "wav"

    if not (shutil.which("say") and shutil.which("afconvert")):
        return _tom_wav(), "audio/wav", "wav"

    with tempfile.TemporaryDirectory(prefix="citizenassist-tts-") as pasta:
        aiff = Path(pasta) / "voz.aiff"
        wav = Path(pasta) / "voz.wav"

        tentativas = [
            ["say", "-v", "Luciana", "-r", "170", "-o", str(aiff), texto],
            ["say", "-r", "170", "-o", str(aiff), texto],
        ]
        falou = False
        for comando in tentativas:
            try:
                subprocess.run(
                    comando,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=12,
                )
                falou = True
                break
            except (OSError, subprocess.SubprocessError):
                continue

        if not falou:
            return _tom_wav(), "audio/wav", "wav"

        try:
            subprocess.run(
                ["afconvert", "-f", "WAVE", "-d", "LEI16@22050", str(aiff), str(wav)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=12,
            )
            audio = wav.read_bytes()
            if audio:
                return audio, "audio/wav", "wav"
        except (OSError, subprocess.SubprocessError):
            pass

    return _tom_wav(), "audio/wav", "wav"


def _tom_wav() -> bytes:
    buffer = io.BytesIO()
    taxa = 22050
    with wave.open(buffer, "wb") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(taxa)
        for i in range(int(taxa * 0.6)):
            amostra = int(9000 * math.sin(2 * math.pi * 440 * i / taxa))
            arquivo.writeframes(struct.pack("<h", amostra))
    return buffer.getvalue()
