import unicodedata


def normalizar(texto):
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
    if not palavra_normalizada:
        return False

    texto_normalizado = normalizar(texto)
    return f" {palavra_normalizada} " in f" {texto_normalizado} "
