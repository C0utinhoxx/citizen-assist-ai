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

    def __init__(self, lista):
        self.lista = lista

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
