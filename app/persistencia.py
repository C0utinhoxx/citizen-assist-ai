"""Leitura e gravação dos arquivos JSON e CSV."""

import csv
import json
import os

from .modelos import Servico

CAMPOS_CSV = [
    "data", "origem", "pergunta", "id_orientacao",
    "encontrou", "ajudou", "tentativas", "tempo",
]


def _garantir_pasta(caminho):
    pasta = os.path.dirname(caminho) or "."
    os.makedirs(pasta, exist_ok=True)


def carregar_servicos(caminho):
    """Lê o catálogo JSON e devolve uma lista de Servico.

    Um registro inválido é ignorado com aviso; o restante continua sendo
    carregado. Arquivo ausente ou corrompido não derruba o programa.
    """
    if not os.path.exists(caminho):
        print(f"Aviso: arquivo de dados não encontrado: {caminho}")
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError) as erro:
        print(f"Aviso: não foi possível ler os dados ({erro}).")
        return []

    if not isinstance(dados, list):
        print("Aviso: o JSON de serviços deve conter uma lista.")
        return []

    servicos = []
    for item in dados:
        try:
            servicos.append(Servico.de_dict(item))
        except (KeyError, TypeError, ValueError) as erro:
            print(f"Aviso: registro ignorado (dados inválidos): {erro}")

    return servicos


def salvar_servicos(caminho, lista):
    """Grava a lista encadeada no JSON, preservando todos os campos."""
    try:
        _garantir_pasta(caminho)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                [servico.para_dict() for servico in lista.percorrer()],
                arquivo,
                ensure_ascii=False,
                indent=2,
            )
        return True
    except OSError as erro:
        print(f"Aviso: não foi possível salvar os dados: {erro}")
        return False


def carregar_historico(caminho):
    """Lê o histórico de atendimentos. Devolve uma lista vazia se falhar."""
    if not os.path.exists(caminho):
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        print("Aviso: não foi possível ler o histórico antigo. Começando um novo.")
        return []

    if not isinstance(dados, list):
        print("Aviso: o histórico deve conter uma lista. Começando um novo.")
        return []

    return dados


def salvar_historico(caminho, historico):
    """Grava o histórico de atendimentos no JSON."""
    try:
        _garantir_pasta(caminho)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(historico, arquivo, ensure_ascii=False, indent=2)
        return True
    except OSError as erro:
        print(f"Aviso: não foi possível salvar o histórico: {erro}")
        return False


def exportar_csv(caminho, historico):
    """Exporta os atendimentos para CSV e devolve True/False."""
    try:
        _garantir_pasta(caminho)
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV)
            escritor.writeheader()

            for registro in historico:
                escritor.writerow({
                    campo: registro.get(campo, "") for campo in CAMPOS_CSV
                })

        print(f"CSV exportado: {caminho} ({len(historico)} atendimentos).")
        return True
    except OSError as erro:
        print(f"Aviso: não foi possível exportar o CSV: {erro}")
        return False
