from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import socket
import sys
import threading
import time
from pathlib import Path

try:
    from . import transcricao, tts
except ImportError:
    import transcricao
    import tts

RAIZ = Path(__file__).resolve().parent
LIMITE_CORPO_TTS = 16 * 1024
LIMITE_TTS_POR_MINUTO = 20
JANELA_TTS_SEGUNDOS = 60.0
TTS_REQUISICOES = {}
TTS_REQUISICOES_LOCK = threading.Lock()

LIMITE_CORPO_ASR = transcricao.LIMITE_AUDIO
LIMITE_ASR_POR_MINUTO = 12
JANELA_ASR_SEGUNDOS = 60.0
ASR_REQUISICOES = {}
ASR_REQUISICOES_LOCK = threading.Lock()


def tts_permitido(ip: str) -> bool:
    agora = time.monotonic()
    with TTS_REQUISICOES_LOCK:
        fila = [
            instante
            for instante in TTS_REQUISICOES.get(ip, [])
            if agora - instante < JANELA_TTS_SEGUNDOS
        ]
        if len(fila) >= LIMITE_TTS_POR_MINUTO:
            TTS_REQUISICOES[ip] = fila
            return False
        fila.append(agora)
        TTS_REQUISICOES[ip] = fila
        return True


def asr_permitido(ip: str) -> bool:
    agora = time.monotonic()
    with ASR_REQUISICOES_LOCK:
        fila = [
            instante
            for instante in ASR_REQUISICOES.get(ip, [])
            if agora - instante < JANELA_ASR_SEGUNDOS
        ]
        if len(fila) >= LIMITE_ASR_POR_MINUTO:
            ASR_REQUISICOES[ip] = fila
            return False
        fila.append(agora)
        ASR_REQUISICOES[ip] = fila
        return True


class Handler(http.server.SimpleHTTPRequestHandler):

    def translate_path(self, path: str) -> str:
        caminho = super().translate_path(path)
        try:
            relativo = Path(caminho).resolve().relative_to(RAIZ.resolve())
        except (OSError, ValueError):
            return str(RAIZ / "__arquivo_privado__")
        if any(parte.startswith(".") for parte in relativo.parts):
            return str(RAIZ / "__arquivo_privado__")
        return caminho

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        if self.path.split("?", 1)[0].startswith("/api/"):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Private-Network", "true")
        super().end_headers()

    def log_message(self, formato: str, *args: object) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), formato % args))

    def _enviar_json(self, codigo: int, dados: object) -> None:
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _enviar_erro(self, codigo: int, mensagem: str) -> None:
        self._enviar_json(codigo, {"erro": mensagem})

    def do_OPTIONS(self) -> None:
        if self.path.split("?", 1)[0].startswith("/api/"):
            self.send_response(204)
            self.end_headers()
            return
        self._enviar_erro(404, "Endpoint não encontrado.")

    def do_GET(self) -> None:
        if self.path == "/api/tts/status":
            self._enviar_json(200, tts.status())
            return
        if self.path == "/api/tts/voices":
            self._enviar_json(200, {"vozes": tts.listar_vozes()})
            return
        if self.path == "/api/tts":
            self._enviar_erro(405, "Use POST para gerar a voz.")
            return
        if self.path == "/api/asr/status":
            self._enviar_json(200, transcricao.status())
            return
        if self.path == "/api/asr":
            self._enviar_erro(405, "Use POST para transcrever o áudio.")
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/api/tts":
            self._post_tts()
            return
        if self.path == "/api/asr":
            self._post_asr()
            return
        self._enviar_erro(404, "Endpoint não encontrado.")

    def _post_tts(self) -> None:
        try:
            tamanho = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            tamanho = 0
        if tamanho <= 0:
            self._enviar_erro(400, "Envie um JSON com o campo texto.")
            return
        if tamanho > LIMITE_CORPO_TTS:
            self._enviar_erro(413, "O pedido de voz é grande demais.")
            return

        try:
            dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._enviar_erro(400, "JSON inválido.")
            return

        if not isinstance(dados, dict):
            self._enviar_erro(400, "JSON inválido.")
            return

        texto = dados.get("texto", dados.get("text", ""))
        voz = dados.get("voz", "")
        if not tts_permitido(self.client_address[0]):
            self._enviar_erro(
                429,
                "Muitas solicitações de voz em pouco tempo. Aguarde alguns segundos e tente de novo.",
            )
            return
        try:
            resultado = tts.sintetizar(texto, voz)
        except tts.TTSValidationError as exc:
            self._enviar_erro(400, str(exc))
            return
        except tts.TTSConfigError as exc:
            self._enviar_erro(503, str(exc))
            return
        except tts.TTSError as exc:
            self._enviar_erro(502, str(exc))
            return
        except Exception:
            self._enviar_erro(500, "Não foi possível gerar a voz agora.")
            return

        self.send_response(200)
        self.send_header("Content-Type", resultado.content_type)
        self.send_header("Content-Length", str(len(resultado.audio)))
        self.send_header("X-TTS-Provider", resultado.provedor)
        self.send_header("X-TTS-Mode", resultado.modo)
        self.send_header("X-TTS-Voice", resultado.voz)
        self.send_header("X-TTS-Cache", "hit" if resultado.cache else "miss")
        self.end_headers()
        self.wfile.write(resultado.audio)

    def _post_asr(self) -> None:
        config = transcricao.config_do_ambiente()
        if not config.pronto:
            self._enviar_erro(503, config.aviso or "Transcrição pelo servidor indisponível.")
            return

        try:
            tamanho = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            tamanho = 0
        if tamanho <= 0:
            self._enviar_erro(400, "Nenhum áudio foi recebido.")
            return
        if tamanho > LIMITE_CORPO_ASR:
            self._enviar_erro(413, "O áudio é grande demais. Grave uma frase mais curta.")
            return

        tipo = (self.headers.get("Content-Type", "") or "").split(";", 1)[0].strip()
        if not tipo.lower().startswith("audio/"):
            self._enviar_erro(415, "Envie o áudio com Content-Type de áudio.")
            return

        if not asr_permitido(self.client_address[0]):
            self._enviar_erro(
                429,
                "Muitas transcrições em pouco tempo. Aguarde alguns segundos e tente de novo.",
            )
            return

        try:
            audio = self.rfile.read(tamanho)
        except OSError:
            self._enviar_erro(400, "Não foi possível ler o áudio enviado.")
            return

        try:
            texto = transcricao.transcrever(audio, tipo, config=config)
        except transcricao.ASRValidationError as exc:
            self._enviar_erro(400, str(exc))
            return
        except transcricao.ASRConfigError as exc:
            self._enviar_erro(503, str(exc))
            return
        except transcricao.ASRError as exc:
            self._enviar_erro(502, str(exc))
            return
        except Exception:
            self._enviar_erro(500, "Não foi possível transcrever o áudio agora.")
            return

        self._enviar_json(
            200,
            {
                "texto": texto,
                "provedor": config.provedor,
                "modelo": config.modelo,
            },
        )


def ip_local() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "127.0.0.1"
    finally:
        sock.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Serve o Citizen Assist AI Mobile na rede local."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="porta HTTP (padrão: 8000; use 0 para escolher uma livre)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="endereço de escuta (padrão: 0.0.0.0, toda a rede local)",
    )
    args = parser.parse_args()

    tts.carregar_env(RAIZ / ".env")
    if not (
        os.environ.get("OPENAI_API_KEY", "").strip()
        or os.environ.get("GROQ_API_KEY", "").strip()
    ):
        tts.carregar_env(RAIZ.parent / "agente" / ".env")
    config_voz = tts.config_do_ambiente()
    config_asr = transcricao.config_do_ambiente()

    handler = functools.partial(Handler, directory=str(RAIZ))
    try:
        servidor = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as exc:
        print("Não foi possível abrir a porta %s: %s" % (args.port, exc))
        print("Tente outra porta, por exemplo: python3 servir.py --port 8080")
        return 1

    porta = servidor.server_address[1]
    ip = ip_local()

    print("=" * 62)
    print(" Citizen Assist AI - servidor local")
    print("=" * 62)
    print(" Pasta:      %s" % RAIZ)
    print(" Computador: http://localhost:%s/" % porta)
    if args.host in ("0.0.0.0", "::"):
        print(" Celular:    http://%s:%s/" % (ip, porta))
        print()
        print(" Deixe o celular na mesma rede Wi-Fi do computador.")
        print(" Se não abrir, libere a porta no firewall do computador.")
        print(" Use apenas em rede local de confiança; não exponha à internet.")
    else:
        print(" Endereço:   http://%s:%s/" % (args.host, porta))
    print()
    if config_voz.provedor == "azure" and config_voz.pronto:
        print(" Voz natural: Azure · %s · %s" % (config_voz.voz, config_voz.regiao))
    elif config_voz.pronto:
        print(" Voz natural: modo de teste (sem chave do Azure)")
        print(" Configure mobile/.env para usar a voz real.")
    else:
        print(" Voz natural: indisponível")
        if config_voz.aviso:
            print(" %s" % config_voz.aviso)
    if config_asr.pronto:
        print(
            " Ditado pelo servidor: %s · %s"
            % (config_asr.provedor, config_asr.modelo)
        )
    else:
        print(" Ditado pelo servidor: indisponível")
        if config_asr.aviso:
            print(" %s" % config_asr.aviso)
    print()
    print(" Ctrl+C para parar.")
    print("=" * 62)

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
