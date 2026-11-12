from __future__ import annotations

from typing import Optional

from .agente import AgenteCidadao


def _ler_inteiro(mensagem: str, maximo: int) -> Optional[int]:
    try:
        entrada = input(mensagem).strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not entrada.isdigit():
        print("Entrada inválida. Digite um número.")
        return -1

    numero = int(entrada)
    if numero < 0 or numero > maximo:
        print(f"Entrada inválida. Digite um número de 0 a {maximo}.")
        return -1
    return numero


def _mostrar_cabecalho(agente: AgenteCidadao) -> None:
    print("\n" + "=" * 62)
    print(" Citizen Assist AI — Agente de Documentos Pessoais")
    print(" Fonte exclusiva: fichas FC-01 a FC-07")
    print("=" * 62)
    if agente.modo == "llm":
        print(f"Modo: LLM ({agente.provedor.nome})")
    else:
        print("Modo: extrativo (offline, sem LLM configurado)")
    provisorias = [
        ficha.id for ficha in agente.fichas.values() if ficha.provisoria
    ]
    if provisorias:
        print(
            "Aviso acadêmico: fichas provisórias "
            + ", ".join(provisorias)
            + ". Substitua pelas oficiais antes da entrega."
        )
    print("Privacidade: não digite CPF, RG, telefone, e-mail ou endereço.")
    print("-" * 62)
    print("1 - Fazer uma pergunta")
    print("2 - Navegar por categorias (fichas)")
    print("3 - Privacidade, fontes e limitações")
    print("0 - Voltar")
    print("=" * 62)


def _navegar(agente: AgenteCidadao) -> None:
    fichas = agente.categorias()
    if not fichas:
        print("Nenhuma ficha carregada.")
        return

    print("\n--- Categorias de documentos ---")
    for indice, ficha in enumerate(fichas, start=1):
        marca = " (provisória)" if ficha["provisoria"] else ""
        print(f"{indice} - {ficha['id']}: {ficha['titulo']}{marca}")
    print("0 - Voltar")

    opcao = _ler_inteiro("Categoria: ", len(fichas))
    if opcao is None or opcao <= 0:
        return

    escolhida = fichas[opcao - 1]
    resposta = agente.responder_por_ficha(str(escolhida["id"]))
    if resposta is None:
        print("Ficha não encontrada.")
        return
    print()
    print(resposta.texto)


def _privacidade() -> None:
    print(
        "\n--- Privacidade, fontes e limitações ---\n"
        "- O agente usa apenas as fichas FC-01 a FC-07 como fonte de verdade.\n"
        "- As fichas são material didático fictício do exercício, "
        "versão de 01/10/2026.\n"
        "- Nenhuma pergunta é gravada em arquivo, banco ou histórico.\n"
        "- CPF, RG, CNH, título, telefone, e-mail e endereço são recusados e "
        "ocultados.\n"
        "- O agente não consulta sistemas do governo e não acompanha processos.\n"
        "- O agente não é um canal oficial. Confirme sempre no órgão competente.\n"
        "- Em caso de emergência, ligue 190; para denúncias, ligue 100.\n"
    )


def executar_menu_agente(agente: Optional[AgenteCidadao] = None) -> None:
    if agente is None:
        try:
            agente = AgenteCidadao()
        except Exception as erro:
            print(f"Não foi possível carregar o agente: {erro}")
            return

    while True:
        _mostrar_cabecalho(agente)
        opcao = _ler_inteiro("Escolha uma opção: ", 3)
        if opcao is None:
            break
        if opcao == 0:
            break
        if opcao == 1:
            print("\n--- Fazer uma pergunta ---")
            try:
                pergunta = input("Digite sua dúvida (0 para voltar): ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if pergunta == "0":
                continue
            resposta = agente.responder(pergunta)
            print("\n" + resposta.texto)
            if resposta.detalhe and not resposta.usou_llm:
                print(f"\n(Nota técnica: {resposta.detalhe})")
        elif opcao == 2:
            _navegar(agente)
        elif opcao == 3:
            _privacidade()
        elif opcao == -1:
            continue

    print(
        "\nSessão encerrada. Atendimentos: "
        f"{agente.atendimentos} | respostas encontradas: "
        f"{agente.respostas_encontradas} | recusas de segurança: "
        f"{agente.respostas_seguras} | sem resultado: "
        f"{agente.respostas_sem_resultado}."
    )
    print("Nenhuma pergunta foi armazenada.")


def main() -> None:
    try:
        executar_menu_agente()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")

if __name__ == "__main__":
    main()
