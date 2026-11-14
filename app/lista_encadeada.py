from .texto import normalizar


class No:

    def __init__(self, servico):
        self.servico = servico
        self.proximo = None


class ListaEncadeada:

    CAMPOS_ORDENACAO = ("id", "titulo", "categoria")

    def __init__(self):
        self.inicio = None
        self.quantidade = 0

    def vazia(self):
        return self.inicio is None

    def inserir(self, servico):
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
        atual = self.inicio
        while atual is not None:
            yield atual.servico
            atual = atual.proximo

    def listar(self):
        return list(self.percorrer())

    def buscar_por_id(self, id):
        for servico in self.percorrer():
            if servico.id == id:
                return servico
        return None

    def pesquisar(self, texto):
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
        servico = self.buscar_por_id(id)
        if servico is None:
            return None

        permitidos = {
            "titulo", "categoria", "resposta", "descricao", "documentos",
            "onde", "local", "fonte", "palavras_chave", "verificado_em",
        }

        for nome, valor in campos.items():
            if nome not in permitidos:
                raise ValueError(f"Campo não pode ser atualizado: {nome}")
            if valor is not None:
                setattr(servico, nome, valor)

        return servico

    def remover(self, id):
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
        valor = getattr(servico, campo)
        return valor if campo == "id" else normalizar(valor)

    def contar_por_categoria(self):
        contagem = {}
        for servico in self.percorrer():
            contagem[servico.categoria] = contagem.get(servico.categoria, 0) + 1
        return contagem
