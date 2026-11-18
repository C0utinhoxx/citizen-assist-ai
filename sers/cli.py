"""Interface de terminal da contribuição SERS no Citizen Assist AI."""

from __future__ import annotations

from typing import Optional

from .energia import FONTES, Premissas, analisar, formatar_relatorio


def _ler_float(mensagem: str, padrao: Optional[float] = None) -> Optional[float]:
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        if not entrada and padrao is not None:
            return padrao
        if entrada in ("0", "voltar"):
            return None
        try:
            valor = float(entrada)
        except ValueError:
            print("Entrada inválida. Digite um número, por exemplo 150.")
            continue
        if valor <= 0:
            print("O valor precisa ser maior que zero.")
            continue
        return valor


def _mostrar_cabecalho() -> None:
    print("\n" + "=" * 62)
    print(" Energia e sustentabilidade (SERS)")
    print(" Estimativas para uma casa de baixa renda")
    print("=" * 62)
    print("1 - Comparar alternativas com o cenário padrão (150 kWh/mês)")
    print("2 - Calcular com o meu consumo")
    print("3 - Fontes, premissas e limitações")
    print("0 - Voltar")
    print("=" * 62)


def _mostrar_fontes() -> None:
    print("\n--- Fontes e premissas ---")
    for fonte in FONTES:
        print(f"\n{fonte['tema']}")
        print(f"Fonte: {fonte['fonte']}")
        print(f"Uso no cálculo: {fonte['uso']}")
        print(f"Link: {fonte['url']}")
        print(f"Consultado em: {fonte['data']}")
    print("\nLimitações:")
    print("- Os valores são estimativas, não garantia de economia.")
    print("- Tarifa, impostos, bandeiras e consumo real mudam o resultado.")
    print("- O solar exige telhado próprio, sem sombra, e aprovação da distribuidora.")
    print("- O cálculo não inclui manutenção, troca de inversor nem financiamento.")
    print("- Este assistente não é um canal oficial.")


def _relatorio(p: Premissas) -> None:
    print()
    print(formatar_relatorio(analisar(p)))


def executar_menu_sers() -> None:
    while True:
        _mostrar_cabecalho()
        entrada = input("Escolha uma opção: ").strip()

        if entrada == "0":
            return

        if entrada == "1":
            _relatorio(Premissas())
            input("\nPressione Enter para voltar ao menu de energia.")
            continue

        if entrada == "2":
            print("\nInforme o consumo da sua conta de luz. Não informe nome, "
                  "CPF, endereço ou número da unidade consumidora.")
            consumo = _ler_float("Consumo em kWh/mês (0 para voltar): ")
            if consumo is None:
                continue
            tarifa = _ler_float(
                "Tarifa em R$/kWh (Enter para usar 0,90): ", padrao=0.90
            )
            if tarifa is None:
                continue
            try:
                _relatorio(Premissas(
                    consumo_mensal_kwh=consumo,
                    tarifa_rs_kwh=tarifa,
                ))
            except ValueError as erro:
                print(f"Não foi possível calcular: {erro}")
            input("\nPressione Enter para voltar ao menu de energia.")
            continue

        if entrada == "3":
            _mostrar_fontes()
            input("\nPressione Enter para voltar ao menu de energia.")
            continue

        print("Entrada inválida. Digite 0, 1, 2 ou 3.")
