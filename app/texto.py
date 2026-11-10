"""Normalização de texto usada pela busca, pela ordenação e pela pontuação."""

import unicodedata


def normalizar(texto):
    """Devolve o texto em minúsculas, sem acentos e sem pontuação.

    O resultado também tem os espaços ajustados, o que permite comparar
    palavras inteiras (por exemplo, "saude" não encontra "saudavel").
    """
    if texto is None:
        return ""

    decomposto = unicodedata.normalize("NFD", str(texto).lower())
    sem_acento = "".join(
        letra for letra in decomposto
        if unicodedata.category(letra) != "Mn"
    )
    limpo = "".join(
        letra if letra.isalnum() else " " for letra in sem_acento
    )
    return " ".join(limpo.split())


def contem_palavra(texto, palavra_normalizada):
    """Verifica se uma palavra ou expressão aparece inteira no texto."""
    if not palavra_normalizada:
        return False

    texto_normalizado = normalizar(texto)
    return f" {palavra_normalizada} " in f" {texto_normalizado} "
