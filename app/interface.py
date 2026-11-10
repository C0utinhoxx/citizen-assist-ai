"""Menu interativo, validação de entradas e operações do catálogo."""

from .modelos import Servico
from .persistencia import salvar_servicos
from .texto import normalizar


# ----------------------------------------------------------------------
# Entrada de dados
# ----------------------------------------------------------------------
def ler_inteiro(mensagem, minimo, maximo):
    """Lê um número inteiro dentro da faixa. Repete enquanto for inválido."""
    while True:
        entrada = input(mensagem).strip()
        try:
            numero = int(entrada)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue

        if numero < minimo or numero > maximo:
            print(f"Entrada inválida. Digite um número de {minimo} a {maximo}.")
            continue

        return numero


def ler_texto(mensagem):
    """Lê um texto não vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo não pode ficar vazio.")


def ler_opcional(mensagem, valor_atual):
    """Enter mantém o valor atual; qualquer texto substitui."""
    texto = input(f"{mensagem} [{valor_atual}]: ").strip()
    return texto if texto else None


def ler_lista(mensagem, separador):
    """Lê uma lista separada por um caractere. Texto vazio vira lista vazia."""
    texto = input(mensagem).strip()
    if not texto:
        return []
    return [parte.strip() for parte in texto.split(separador) if parte.strip()]


def ler_lista_opcional(mensagem, valor_atual, separador):
    """Enter mantém a lista atual; qualquer texto substitui a lista."""
    atual = separador.join(valor_atual)
    texto = input(f"{mensagem} [{atual}]: ").strip()
    if not texto:
        return None
    return [parte.strip() for parte in texto.split(separador) if parte.strip()]


def confirmar(mensagem):
    """Lê s ou n, repetindo se a resposta for inválida."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == "s":
            return True
        if resposta == "n":
            return False
        print("Responda com s (sim) ou n (não).")


# ----------------------------------------------------------------------
# Operações do menu
# ----------------------------------------------------------------------
def cadastrar(lista):
    """Cadastra um serviço. Devolve True quando a lista foi alterada."""
    print("\n--- Cadastrar serviço ---")
    id = ler_inteiro("ID (número positivo): ", 1, 999999)

    if lista.buscar_por_id(id) is not None:
        print("Já existe um serviço com esse ID. Cadastro cancelado.")
        return False

    titulo = ler_texto("Título: ")
    categoria = ler_texto("Categoria: ")
    descricao = ler_texto("Descrição: ")
    documentos = ler_lista(
        "Documentos/requisitos (separados por ;, opcional): ", ";"
    )
    local = ler_texto("Local de atendimento: ")
    fonte = input("Fonte oficial (opcional): ").strip()
    palavras_chave = ler_lista(
        "Palavras-chave (separadas por vírgula, opcional): ", ","
    )
    verificado_em = input("Data de verificação (AAAA-MM-DD, opcional): ").strip()

    servico = Servico(
        id=id,
        titulo=titulo,
        categoria=categoria,
        descricao=descricao,
        documentos=documentos,
        local=local,
        fonte=fonte,
        palavras_chave=palavras_chave,
        verificado_em=verificado_em,
    )

    if lista.inserir(servico):
        print("Serviço cadastrado com sucesso.")
        return True

    print("Não foi possível cadastrar: ID duplicado.")
    return False


def consultar(lista):
    """Consulta um serviço pelo identificador."""
    print("\n--- Consultar por ID ---")
    id = ler_inteiro("ID: ", 1, 999999)
    servico = lista.buscar_por_id(id)

    if servico is None:
        print("Serviço não encontrado.")
    else:
        servico.exibir()


def pesquisar(lista):
    """Pesquisa por título, categoria ou descrição."""
    print("\n--- Pesquisar por atributo ---")
    texto = ler_texto("Digite título, categoria ou palavra da descrição: ")
    resultados = lista.pesquisar(texto)

    if not resultados:
        print("Nenhum registro encontrado.")
        return

    print(f"\n{len(resultados)} resultado(s):")
    for servico in resultados:
        servico.exibir()


def atualizar(lista):
    """Atualiza um serviço. Devolve True quando a lista foi alterada."""
    print("\n--- Atualizar serviço ---")
    id = ler_inteiro("ID do serviço: ", 1, 999999)
    servico = lista.buscar_por_id(id)

    if servico is None:
        print("Serviço não encontrado.")
        return False

    print("Pressione Enter para manter o valor atual.")
    titulo = ler_opcional("Título", servico.titulo)
    categoria = ler_opcional("Categoria", servico.categoria)
    descricao = ler_opcional("Descrição", servico.descricao)
    documentos = ler_lista_opcional(
        "Documentos/requisitos (separados por ;)", servico.documentos, ";"
    )
    local = ler_opcional("Local", servico.local)
    fonte = ler_opcional("Fonte", servico.fonte)
    palavras_chave = ler_lista_opcional(
        "Palavras-chave (separadas por vírgula)", servico.palavras_chave, ","
    )
    verificado_em = ler_opcional("Data de verificação", servico.verificado_em)

    lista.atualizar(
        id,
        titulo=titulo,
        categoria=categoria,
        descricao=descricao,
        documentos=documentos,
        local=local,
        fonte=fonte,
        palavras_chave=palavras_chave,
        verificado_em=verificado_em,
    )
    print("Serviço atualizado com sucesso.")
    return True


def excluir(lista):
    """Exclui um serviço. Devolve True quando a lista foi alterada."""
    print("\n--- Excluir serviço ---")
    id = ler_inteiro("ID do serviço: ", 1, 999999)
    servico = lista.buscar_por_id(id)

    if servico is None:
        print("Serviço não encontrado.")
        return False

    if confirmar(f"Excluir '{servico.titulo}'? (s/n): "):
        lista.remover(id)
        print("Serviço excluído.")
        return True

    print("Operação cancelada.")
    return False


def listar(lista):
    """Lista todos os serviços na ordem atual da lista."""
    print("\n--- Todos os serviços ---")
    if lista.vazia():
        print("A lista está vazia.")
        return

    for servico in lista.percorrer():
        servico.exibir()

    print(f"\nTotal: {lista.quantidade} serviço(s).")


def ordenar(lista):
    """Ordena com Selection Sort. Devolve True quando a lista foi alterada."""
    if lista.vazia():
        print("\nA lista está vazia. Não há o que ordenar.")
        return False

    print("\n--- Ordenar ---")
    print("1 - Título")
    print("2 - Categoria")
    print("3 - ID")
    opcao = ler_inteiro("Critério: ", 1, 3)

    campo = {1: "titulo", 2: "categoria", 3: "id"}[opcao]
    lista.ordenar_por(campo)

    print(f"\nLista ordenada por {campo} (Selection Sort):")
    for servico in lista.percorrer():
        print(f"{servico.id:>3} | {servico.categoria:<20} | {servico.titulo}")

    return True


def _ordenar_contagem(itens):
    """Ordena (categoria, quantidade) por quantidade desc e nome asc."""
    for indice in range(1, len(itens)):
        atual = itens[indice]
        posicao = indice - 1

        while posicao >= 0:
            categoria, quantidade = itens[posicao]
            atual_categoria, atual_quantidade = atual

            deve_descer = (
                quantidade < atual_quantidade
                or (
                    quantidade == atual_quantidade
                    and normalizar(categoria) > normalizar(atual_categoria)
                )
            )
            if not deve_descer:
                break

            itens[posicao + 1] = itens[posicao]
            posicao -= 1

        itens[posicao + 1] = atual

    return itens


def analise_servicos(lista):
    """Apresenta a análise dos dados cadastrados no catálogo."""
    print("\n--- Análise dos serviços cadastrados ---")
    if lista.vazia():
        print("Nenhum registro cadastrado.")
        return

    contagem = _ordenar_contagem(list(lista.contar_por_categoria().items()))
    total = lista.quantidade

    print(f"Total de registros: {total}")
    print("Serviços por categoria:")

    for categoria, quantidade in contagem:
        porcentagem = 100 * quantidade / total
        print(f" - {categoria}: {quantidade} ({porcentagem:.1f}%)")

    print(f"Categoria com mais serviços: {contagem[0][0]}")

    sem_palavras = 0
    sem_fonte = 0
    total_palavras = 0

    for servico in lista.percorrer():
        if not servico.palavras_chave:
            sem_palavras += 1
        if not servico.fonte:
            sem_fonte += 1
        total_palavras += len(servico.palavras_chave)

    media_palavras = total_palavras / total
    print(f"Registros sem palavras-chave: {sem_palavras}")
    print(f"Registros sem fonte: {sem_fonte}")
    print(f"Palavras-chave cadastradas: {total_palavras} "
          f"(média de {media_palavras:.1f} por registro)")


# ----------------------------------------------------------------------
# Menu principal
# ----------------------------------------------------------------------
def mostrar_menu(lista, assistente):
    """Mostra o menu e um resumo do catálogo."""
    categorias = assistente.base.categorias()

    print("\n" + "=" * 60)
    print(f" {assistente.nome}")
    print(" Assistente Digital de Orientação ao Cidadão")
    print("=" * 60)
    print(f"Serviços cadastrados: {lista.quantidade}")
    if categorias:
        print(f"Categorias: {', '.join(categorias)}")
    else:
        print("Categorias: nenhuma")
    print("-" * 60)
    print("1 - Cadastrar serviço")
    print("2 - Consultar por ID")
    print("3 - Pesquisar por título/categoria/descrição")
    print("4 - Atualizar serviço")
    print("5 - Excluir serviço")
    print("6 - Listar todos")
    print("7 - Ordenar e listar")
    print("8 - Análise dos serviços")
    print("9 - Fazer uma pergunta")
    print("10 - Navegar por categorias")
    print("11 - Indicadores de atendimento")
    print("12 - Exportar atendimentos para CSV")
    print("0 - Salvar e sair")
    print("=" * 60)


def executar_menu(lista, assistente, caminho_servicos):
    """Executa o menu interativo até a opção 0."""
    while True:
        mostrar_menu(lista, assistente)
        opcao = ler_inteiro("Escolha uma opção: ", 0, 12)

        if opcao == 0:
            if salvar_servicos(caminho_servicos, lista):
                print("\nDados salvos com sucesso.")
            assistente.finalizar()
            break

        alterou = False

        if opcao == 1:
            alterou = cadastrar(lista)
        elif opcao == 2:
            consultar(lista)
        elif opcao == 3:
            pesquisar(lista)
        elif opcao == 4:
            alterou = atualizar(lista)
        elif opcao == 5:
            alterou = excluir(lista)
        elif opcao == 6:
            listar(lista)
        elif opcao == 7:
            alterou = ordenar(lista)
        elif opcao == 8:
            analise_servicos(lista)
        elif opcao == 9:
            assistente.perguntar()
        elif opcao == 10:
            assistente.navegar()
        elif opcao == 11:
            assistente.indicadores()
        elif opcao == 12:
            assistente.exportar_csv()

        if alterou:
            salvar_servicos(caminho_servicos, lista)
