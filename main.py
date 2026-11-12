"""Ponto de entrada do Citizen Assist AI.

Execute com: python3 main.py
"""

from pathlib import Path

from app.assistente import Assistente
from app.base_conhecimento import BaseConhecimento
from app.interface import executar_menu
from app.lista_encadeada import ListaEncadeada
from app.persistencia import carregar_servicos

PASTA_DADOS = Path(__file__).resolve().parent / "data"
CAMINHO_SERVICOS = PASTA_DADOS / "servicos.json"
CAMINHO_HISTORICO = PASTA_DADOS / "historico.json"
CAMINHO_CSV = PASTA_DADOS / "atendimentos.csv"


def main():
    """Carrega o catálogo, monta a lista encadeada e abre o menu."""
    lista = ListaEncadeada()

    for servico in carregar_servicos(str(CAMINHO_SERVICOS)):
        if not lista.inserir(servico):
            print(f"Aviso: ID duplicado ignorado: {servico.id}")

    base = BaseConhecimento(lista)
    assistente = Assistente(
        "Citizen Assist AI",
        base,
        str(CAMINHO_HISTORICO),
        str(CAMINHO_CSV),
    )

    executar_menu(lista, assistente, str(CAMINHO_SERVICOS))

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
