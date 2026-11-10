"""Base de conhecimento: categorias e busca por pontuação.

A base não guarda outra cópia dos registros: ela usa a mesma lista
encadeada do catálogo. Assim, toda consulta percorre os nós de verdade.
"""

from .texto import contem_palavra, normalizar

# Pontuação mínima para cada nível de confiança.
PONTOS_ALTA = 6
PONTOS_MEDIA = 3


def _ordenar_categorias(nomes):
    """Ordena nomes de categoria com Insertion Sort, ignorando acentos."""
    for indice in range(1, len(nomes)):
        atual = nomes[indice]
        posicao = indice - 1

        while posicao >= 0 and normalizar(nomes[posicao]) > normalizar(atual):
            nomes[posicao + 1] = nomes[posicao]
            posicao -= 1

        nomes[posicao + 1] = atual

    return nomes


def _vem_antes(item, outro):
    """Compara resultados: maior pontuação primeiro; empate pelo menor ID."""
    pontos, servico = item
    outros_pontos, outro_servico = outro

    if pontos != outros_pontos:
        return pontos > outros_pontos
    return servico.id < outro_servico.id


def _ordenar_resultados(resultados):
    """Ordena os resultados da busca com Insertion Sort."""
    for indice in range(1, len(resultados)):
        atual = resultados[indice]
        posicao = indice - 1

        while posicao >= 0 and _vem_antes(atual, resultados[posicao]):
            resultados[posicao + 1] = resultados[posicao]
            posicao -= 1

        resultados[posicao + 1] = atual

    return resultados


class BaseConhecimento:
    """Oferece categorias e busca por pontuação sobre a lista encadeada."""

    def __init__(self, lista):
        self.lista = lista

    def categorias(self):
        """Devolve as categorias sem repetir, em ordem alfabética."""
        vistas = {}

        for servico in self.lista.percorrer():
            chave = normalizar(servico.categoria)
            if chave and chave not in vistas:
                vistas[chave] = servico.categoria

        return _ordenar_categorias(list(vistas.values()))

    def por_categoria(self, categoria):
        """Devolve os serviços de uma categoria, na ordem da lista."""
        chave = normalizar(categoria)
        return [
            servico for servico in self.lista.percorrer()
            if normalizar(servico.categoria) == chave
        ]

    def pontuar(self, pergunta, servico):
        """Calcula quantos pontos um serviço faz para a pergunta.

        Regras mantidas da Lição 1:
        - +3 para cada palavra-chave que aparece inteira na pergunta;
        - +1 para cada palavra da pergunta (4 letras ou mais) que
          aparece inteira no título.
        """
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
        """Devolve tuplas (pontos, servico) da maior para a menor pontuação.

        A busca é linear: percorre todos os nós da lista encadeada.
        Registros com zero ponto não entram no resultado.
        """
        if not normalizar(pergunta):
            return []

        resultados = []
        for servico in self.lista.percorrer():
            pontos = self.pontuar(pergunta, servico)
            if pontos > 0:
                resultados.append((pontos, servico))

        return _ordenar_resultados(resultados)
