class Orientacao:
    """Uma orientação da base de conhecimento (um registro do JSON).

    Campos canônicos (os mesmos do enunciado): id, categoria, titulo,
    palavras_chave, resposta, documentos, onde, fonte, verificado_em.

    Por compatibilidade com o código antigo do catálogo, os nomes
    ``descricao`` e ``local`` continuam funcionando como apelidos de
    ``resposta`` e ``onde`` (leitura e escrita).
    """

    def __init__(self, id, titulo, categoria, descricao=None, documentos=None,
                 local=None, fonte="", palavras_chave=None, verificado_em="",
                 resposta=None, onde=None):
        self.id = int(id)
        self.titulo = str(titulo).strip()
        self.categoria = str(categoria).strip()
        self.resposta = str(
            resposta if resposta is not None else (descricao or "")
        ).strip()
        self.documentos = list(documentos or [])
        self.onde = str(onde if onde is not None else (local or "")).strip()
        self.fonte = str(fonte).strip()
        self.palavras_chave = list(palavras_chave or [])
        self.verificado_em = str(verificado_em).strip()

    # Apelidos usados pelo catálogo DSA (descricao/local).
    @property
    def descricao(self):
        return self.resposta

    @descricao.setter
    def descricao(self, valor):
        self.resposta = str(valor).strip()

    @property
    def local(self):
        return self.onde

    @local.setter
    def local(self, valor):
        self.onde = str(valor).strip()

    def para_dict(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "palavras_chave": self.palavras_chave,
            "resposta": self.resposta,
            "documentos": self.documentos,
            "onde": self.onde,
            "fonte": self.fonte,
            "verificado_em": self.verificado_em,
        }

    @classmethod
    def de_dict(cls, dados):
        if not isinstance(dados, dict):
            raise TypeError("o registro deve ser um objeto")

        resposta = dados.get("resposta", dados.get("descricao"))
        onde = dados.get("onde", dados.get("local", ""))

        if resposta is None:
            raise KeyError("resposta")

        documentos = dados.get("documentos")
        if documentos is None:
            requisitos = dados.get("requisitos", "")
            documentos = [
                parte.strip()
                for parte in str(requisitos).split(";")
                if parte.strip()
            ]

        palavras_chave = dados.get("palavras_chave", [])

        if not isinstance(documentos, list):
            raise TypeError("documentos deve ser uma lista")
        if not isinstance(palavras_chave, list):
            raise TypeError("palavras_chave deve ser uma lista")

        return cls(
            id=int(dados["id"]),
            titulo=str(dados["titulo"]).strip(),
            categoria=str(dados["categoria"]).strip(),
            resposta=str(resposta).strip(),
            documentos=[str(item).strip() for item in documentos if str(item).strip()],
            onde=str(onde).strip(),
            fonte=str(dados.get("fonte", "")).strip(),
            palavras_chave=[
                str(item).strip() for item in palavras_chave if str(item).strip()
            ],
            verificado_em=str(dados.get("verificado_em", "")).strip(),
        )

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(f"ID: {self.id}")
        print(f"Resposta: {self.resposta}")

        print("Documentos necessários:")
        if self.documentos:
            for documento in self.documentos:
                print(f" - {documento}")
        else:
            print(" - Nenhum documento informado.")

        print(f"Onde: {self.onde or 'não informado'}")

        if self.fonte:
            if self.verificado_em:
                print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
            else:
                print(f"Fonte: {self.fonte}")
        else:
            print("Fonte: não informada")

        if self.palavras_chave:
            print(f"Palavras-chave: {', '.join(self.palavras_chave)}")

        print("Aviso: este assistente NÃO é um canal oficial.")


# O catálogo DSA chama esse mesmo registro de Servico.
Servico = Orientacao
