"""Lista encadeada simples implementada pela equipe.

A estrutura guarda os serviços do catálogo. Cada nó tem um serviço e uma
referência para o próximo nó. As operações de CRUD, busca e ordenação são
feitas percorrendo os nós, sem usar listas prontas para armazenar os dados.
"""

from .texto import normalizar


class No:
    """Um nó da lista: guarda um serviço e aponta para o próximo."""

    def __init__(self, servico):
        self.servico = servico
        self.proximo = None


class ListaEncadeada:
    """Lista encadeada com inserção, percurso, busca, remoção e ordenação."""

    CAMPOS_ORDENACAO = ("id", "titulo", "categoria")

    def __init__(self):
        self.inicio = None
        self.quantidade = 0

    def vazia(self):
        """Devolve True quando a lista não tem nenhum nó."""
        return self.inicio is None

    def inserir(self, servico):
        """Insere no fim da lista. Devolve False se o ID já existir."""
        if self.buscar_por_id(servico.id) is not None:
            return False

        novo = No(servico)

        if self.inicio is None:
            self.inicio = novo
        else:
            atual = self.inicio
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo

        self.quantidade += 1
        return True

    def percorrer(self):
        """Percorre a lista do início ao fim, nó por nó."""
        atual = self.inicio
        while atual is not None:
            yield atual.servico
            atual = atual.proximo

    def listar(self):
        """Devolve os serviços em uma lista Python, apenas para exibição."""
        return list(self.percorrer())

    def buscar_por_id(self, id):
        """Busca linear pelo ID. Devolve None quando não encontra."""
        for servico in self.percorrer():
            if servico.id == id:
                return servico
        return None

    def pesquisar(self, texto):
        """Busca linear por título, categoria ou descrição.

        Ignora maiúsculas/minúsculas e acentos. Devolve uma lista vazia
        quando nenhum registro corresponde ao texto.
        """
        termo = normalizar(texto)
        if not termo:
            return []

        encontrados = []
        for servico in self.percorrer():
            campos = (servico.titulo, servico.categoria, servico.descricao)
            if any(termo in normalizar(campo) for campo in campos):
                encontrados.append(servico)

        return encontrados

    def atualizar(self, id, **campos):
        """Atualiza os campos informados. Devolve None se o ID não existir."""
        servico = self.buscar_por_id(id)
        if servico is None:
            return None

        permitidos = {
            "titulo", "categoria", "descricao", "documentos",
            "local", "fonte", "palavras_chave", "verificado_em",
        }

        for nome, valor in campos.items():
            if nome not in permitidos:
                raise ValueError(f"Campo não pode ser atualizado: {nome}")
            if valor is not None:
                setattr(servico, nome, valor)

        return servico

    def remover(self, id):
        """Remove pelo ID, ajustando o ponteiro do nó anterior."""
        anterior = None
        atual = self.inicio

        while atual is not None:
            if atual.servico.id == id:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                self.quantidade -= 1
                return True

            anterior = atual
            atual = atual.proximo

        return False

    def ordenar_por(self, campo):
        """Ordena a lista com Selection Sort, trocando os dados dos nós.

        Não usa sorted() nem list.sort(), pois a ordenação precisa ser
        implementada pela equipe.
        """
        if campo not in self.CAMPOS_ORDENACAO:
            raise ValueError("Campo de ordenação inválido.")

        atual = self.inicio
        while atual is not None:
            menor = atual
            procura = atual.proximo

            while procura is not None:
                if self._chave(procura.servico, campo) < self._chave(menor.servico, campo):
                    menor = procura
                procura = procura.proximo

            if menor is not atual:
                atual.servico, menor.servico = menor.servico, atual.servico

            atual = atual.proximo

    @staticmethod
    def _chave(servico, campo):
        """Devolve o valor usado na comparação da ordenação."""
        valor = getattr(servico, campo)
        return valor if campo == "id" else normalizar(valor)

    def contar_por_categoria(self):
        """Conta quantos serviços existem em cada categoria."""
        contagem = {}
        for servico in self.percorrer():
            contagem[servico.categoria] = contagem.get(servico.categoria, 0) + 1
        return contagem
