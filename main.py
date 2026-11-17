from pathlib import Path

from app.assistente import Assistente
from app.base_conhecimento import BaseConhecimento
from app.interface import executar_menu

PASTA_DADOS = Path(__file__).resolve().parent / "data"
CAMINHO_BASE = PASTA_DADOS / "base_conhecimento.json"
CAMINHO_HISTORICO = PASTA_DADOS / "historico.json"
CAMINHO_CSV = PASTA_DADOS / "atendimentos.csv"


def main():
 
    base = BaseConhecimento(str(CAMINHO_BASE))
    base.carregar()

    assistente = Assistente(
        "Citizen Assist AI",
        base,
        str(CAMINHO_HISTORICO),
        str(CAMINHO_CSV),
    )


    executar_menu(base.lista, assistente, str(CAMINHO_BASE))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
