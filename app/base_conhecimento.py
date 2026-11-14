import os

from .lista_encadeada import ListaEncadeada
from .persistencia import carregar_servicos
from .texto import contem_palavra, normalizar

PONTOS_ALTA = 6
PONTOS_MEDIA = 3


def _ordenar_categorias(nomes):
    for indice in range(1, len(nomes)):
        atual = nomes[indice]
        posicao = indice - 1

        while posicao >= 0 and normalizar(nomes[posicao]) > normalizar(atual):
            nomes[posicao + 1] = nomes[posicao]
            posicao -= 1

        nomes[posicao + 1] = atual

    return nomes


def _vem_antes(item, outro):
    pontos, servico = item
    outros_pontos, outro_servico = outro

    if pontos != outros_pontos:
        return pontos > outros_pontos
    return servico.id < outro_servico.id


def _ordenar_resultados(resultados):
    for indice in range(1, len(resultados)):
        atual = resultados[indice]
        posicao = indice - 1

        while posicao >= 0 and _vem_antes(atual, resultados[posicao]):
            resultados[posicao + 1] = resultados[posicao]
            posicao -= 1

        resultados[posicao + 1] = atual

    return resultados


class BaseConhecimento:

    def __init__(self, origem=None, caminho=None):
        """Aceita um caminho de JSON ou uma ListaEncadeada já montada.

        Forma do enunciado:
            base = BaseConhecimento("data/base_conhecimento.json")
            base.carregar()

        Forma usada pelo catálogo:
            base = BaseConhecimento(lista_encadeada)
        """
        if isinstance(origem, os.PathLike):
            origem = os.fspath(origem)

        if isinstance(origem, str):
            self.caminho = origem
            self.lista = ListaEncadeada()
        elif isinstance(origem, ListaEncadeada):
            self.caminho = caminho
            self.lista = origem
        elif origem is None:
            self.caminho = caminho
            self.lista = ListaEncadeada()
        else:
            raise TypeError(
                "BaseConhecimento espera um caminho de arquivo ou uma ListaEncadeada"
            )

    @property
    def orientacoes(self):
        """Lista de objetos Orientacao carregados (visão da lista encadeada)."""
        return list(self.lista.percorrer())

    def carregar(self, caminho=None):
        """Lê o JSON e cria os objetos Orientacao na lista encadeada.

        Devolve a quantidade de orientações carregadas. Arquivo ausente ou
        corrompido não derruba o programa: apenas avisa e devolve 0.
        """
        caminho = caminho or self.caminho
        if not caminho:
            print("Aviso: nenhum caminho de base de conhecimento informado.")
            return 0

        self.caminho = caminho
        orientacoes = carregar_servicos(caminho)

        carregadas = 0
        for orientacao in orientacoes:
            if self.lista.inserir(orientacao):
                carregadas += 1
            else:
                print(f"Aviso: ID duplicado ignorado: {orientacao.id}")

        return carregadas

    def categorias(self):
        vistas = {}

        for servico in self.lista.percorrer():
            chave = normalizar(servico.categoria)
            if chave and chave not in vistas:
                vistas[chave] = servico.categoria

        return _ordenar_categorias(list(vistas.values()))

    def por_categoria(self, categoria):
        chave = normalizar(categoria)
        return [
            servico for servico in self.lista.percorrer()
            if normalizar(servico.categoria) == chave
        ]

    def pontuar(self, pergunta, servico):
        pergunta_normalizada = normalizar(pergunta)
        if not pergunta_normalizada:
            return 0

        pontos = 0

        for palavra_chave in servico.palavras_chave:
            chave = normalizar(palavra_chave)
            if chave and contem_palavra(pergunta, chave):
                pontos += 3

        palavras_da_pergunta = set(pergunta_normalizada.split())
        for palavra in palavras_da_pergunta:
            if len(palavra) >= 4 and contem_palavra(servico.titulo, palavra):
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        if not normalizar(pergunta):
            return []

        resultados = []
        for servico in self.lista.percorrer():
            pontos = self.pontuar(pergunta, servico)
            if pontos > 0:
                resultados.append((pontos, servico))

        return _ordenar_resultados(resultados)
