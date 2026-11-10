"""Dados de apoio usados pelos testes."""

from app.modelos import Servico


def criar_servico(id=1, titulo="Cartão SUS", categoria="Saúde",
                  descricao="Descrição do serviço", documentos=None,
                  local="UBS", fonte="https://www.gov.br",
                  palavras_chave=None, verificado_em="2026-11-05"):
    """Cria um Servico completo para os testes."""
    return Servico(
        id=id,
        titulo=titulo,
        categoria=categoria,
        descricao=descricao,
        documentos=documentos if documentos is not None else ["Documento com foto"],
        local=local,
        fonte=fonte,
        palavras_chave=(
            palavras_chave if palavras_chave is not None
            else ["cartao sus", "sus", "cartao do sus"]
        ),
        verificado_em=verificado_em,
    )
