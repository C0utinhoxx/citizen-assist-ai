from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

LIMITE_AUDIO = 10 * 1024 * 1024
MODELO_PADRAO_OPENAI = "whisper-1"
MODELO_PADRAO_GROQ = "whisper-large-v3-turbo"
BASE_PADRAO_OPENAI = "https://api.openai.com/v1"
BASE_PADRAO_GROQ = "https://api.groq.com/openai/v1"
TEMPO_LIMITE_SEGUNDOS = 90


class ASRError(Exception):
    pass


class ASRValidationError(ASRError):
    pass


class ASRConfigError(ASRError):
    pass


@dataclass
class ConfigASR:

    provedor: str
    modelo: str
    base_url: str
    pronto: bool
    aviso: str
    chave: str = ""

    def para_status(self) -> Dict[str, object]:
        return {
            "provedor": self.provedor,
            "modelo": self.modelo,
            "pronto": self.pronto,
            "aviso": self.aviso,
            "limite_bytes": LIMITE_AUDIO,
        }


def config_do_ambiente() -> ConfigASR:
    escolhido = (os.environ.get("ASR_PROVIDER", "auto") or "auto").strip().lower()
    if escolhido in ("off", "none", "desativado", "desligado"):
        return ConfigASR(
            provedor="",
            modelo="",
            base_url="",
            pronto=False,
            aviso="Transcrição pelo servidor desativada.",
        )

    if escolhido == "auto":
        if os.environ.get("OPENAI_API_KEY", "").strip():
            escolhido = "openai"
        elif os.environ.get("GROQ_API_KEY", "").strip():
            escolhido = "groq"
        else:
            return ConfigASR(
                provedor="",
                modelo="",
                base_url="",
                pronto=False,
                aviso=(
                    "Configure OPENAI_API_KEY ou GROQ_API_KEY no mobile/.env "
                    "para usar o ditado pelo computador."
                ),
            )

    if escolhido == "openai":
        chave = os.environ.get("OPENAI_API_KEY", "").strip()
        modelo = os.environ.get(
            "OPENAI_TRANSCRIBE_MODEL", MODELO_PADRAO_OPENAI
        ).strip() or MODELO_PADRAO_OPENAI
        base_url = os.environ.get(
            "OPENAI_BASE_URL", BASE_PADRAO_OPENAI
        ).strip() or BASE_PADRAO_OPENAI
        if not chave:
            return ConfigASR(
                provedor="openai",
                modelo=modelo,
                base_url=base_url,
                pronto=False,
                aviso="Configure OPENAI_API_KEY no mobile/.env para transcrever pelo servidor.",
            )
        return ConfigASR("openai", modelo, base_url, True, "", chave)

    if escolhido == "groq":
        chave = os.environ.get("GROQ_API_KEY", "").strip()
        modelo = os.environ.get(
            "GROQ_TRANSCRIBE_MODEL", MODELO_PADRAO_GROQ
        ).strip() or MODELO_PADRAO_GROQ
        base_url = os.environ.get(
            "GROQ_BASE_URL", BASE_PADRAO_GROQ
        ).strip() or BASE_PADRAO_GROQ
        if not chave:
            return ConfigASR(
                provedor="groq",
                modelo=modelo,
                base_url=base_url,
                pronto=False,
                aviso="Configure GROQ_API_KEY no mobile/.env para transcrever pelo servidor.",
            )
        return ConfigASR("groq", modelo, base_url, True, "", chave)

    return ConfigASR(
        provedor=escolhido,
        modelo="",
        base_url="",
        pronto=False,
        aviso="Provedor de transcrição desconhecido. Use openai, groq ou off.",
    )


def status() -> Dict[str, object]:
    return config_do_ambiente().para_status()


def _extensao(tipo: str) -> str:
    tipo = (tipo or "").lower().split(";", 1)[0].strip()
    mapa = {
        "audio/webm": "webm",
        "audio/ogg": "ogg",
        "audio/mp4": "m4a",
        "audio/x-m4a": "m4a",
        "audio/m4a": "m4a",
        "audio/mpeg": "mp3",
        "audio/mp3": "mp3",
        "audio/wav": "wav",
        "audio/wave": "wav",
        "audio/x-wav": "wav",
    }
    return mapa.get(tipo, "webm")


def _corpo_multipart(
    campos: Dict[str, str],
    nome_arquivo: str,
    audio: bytes,
    tipo: str,
) -> Tuple[bytes, str]:
    fronteira = "----CitizenAssistASR" + uuid.uuid4().hex
    partes = []
    for chave, valor in campos.items():
        partes.append(
            (
                "--%s\r\n"
                'Content-Disposition: form-data; name="%s"\r\n\r\n'
                "%s\r\n" % (fronteira, chave, valor)
            ).encode("utf-8")
        )
    partes.append(
        (
            "--%s\r\n"
            'Content-Disposition: form-data; name="file"; filename="%s"\r\n'
            "Content-Type: %s\r\n\r\n"
            % (fronteira, nome_arquivo, tipo or "audio/webm")
        ).encode("utf-8")
    )
    partes.append(audio)
    partes.append(("\r\n--%s--\r\n" % fronteira).encode("utf-8"))
    return b"".join(partes), fronteira


def _detalhe_erro(exc: HTTPError) -> str:
    try:
        bruto = exc.read().decode("utf-8", "replace")
        dados = json.loads(bruto)
        if isinstance(dados, dict):
            erro = dados.get("error")
            if isinstance(erro, dict):
                return str(erro.get("message") or erro.get("code") or "")
            return str(erro or dados.get("message") or "")
    except Exception:
        pass
    return ""


def transcrever(
    audio: bytes,
    tipo: str = "audio/webm",
    idioma: str = "pt",
    config: Optional[ConfigASR] = None,
) -> str:
    if not isinstance(audio, (bytes, bytearray)) or not audio:
        raise ASRValidationError("Nenhum áudio foi recebido. Grave novamente.")
    if len(audio) > LIMITE_AUDIO:
        raise ASRValidationError(
            "O áudio é grande demais. Grave uma frase mais curta e tente de novo."
        )

    config = config or config_do_ambiente()
    if not config.pronto or not config.chave:
        raise ASRConfigError(config.aviso or "Transcrição pelo servidor indisponível.")

    tipo = (tipo or "audio/webm").lower().split(";", 1)[0].strip()
    if not tipo.startswith("audio/"):
        raise ASRValidationError("O arquivo enviado não é um áudio.")

    campos = {
        "model": config.modelo,
        "language": idioma or "pt",
        "response_format": "json",
    }
    corpo, fronteira = _corpo_multipart(
        campos, "audio." + _extensao(tipo), bytes(audio), tipo
    )
    url = config.base_url.rstrip("/") + "/audio/transcriptions"
    requisicao = Request(
        url,
        data=corpo,
        method="POST",
        headers={
            "Authorization": "Bearer " + config.chave,
            "Content-Type": "multipart/form-data; boundary=" + fronteira,
            "Accept": "application/json",
            "User-Agent": "CitizenAssistAI/1.0",
        },
    )

    try:
        with urlopen(requisicao, timeout=TEMPO_LIMITE_SEGUNDOS) as resposta:
            bruto = resposta.read()
    except HTTPError as exc:
        detalhe = _detalhe_erro(exc)
        if exc.code in (401, 403):
            raise ASRError(
                "A chave de transcrição foi recusada. Confira a chave no mobile/.env."
            ) from exc
        if exc.code == 429:
            raise ASRError(
                "Muitas transcrições em pouco tempo. Aguarde alguns segundos e tente de novo."
            ) from exc
        if exc.code == 413:
            raise ASRValidationError(
                "O áudio é grande demais. Grave uma frase mais curta e tente de novo."
            ) from exc
        mensagem = "O serviço de transcrição não respondeu corretamente."
        if detalhe:
            mensagem += " Detalhe: " + detalhe[:200]
        raise ASRError(mensagem) from exc
    except URLError as exc:
        raise ASRError(
            "Não foi possível falar com o serviço de transcrição. Verifique a internet e tente de novo."
        ) from exc
    except OSError as exc:
        raise ASRError("A conexão com o serviço de transcrição foi interrompida.") from exc

    try:
        dados = json.loads(bruto.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ASRError("O serviço de transcrição devolveu uma resposta inválida.") from exc

    texto = ""
    if isinstance(dados, dict):
        texto = str(dados.get("text") or dados.get("texto") or "").strip()
    if not texto:
        raise ASRError(
            "Não consegui entender o áudio. Fale mais perto do microfone e tente de novo."
        )
    return texto
