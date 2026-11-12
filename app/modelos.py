class Servico:

    def __init__(self, id, titulo, categoria, descricao, documentos=None,
                 local="", fonte="", palavras_chave=None, verificado_em=""):
        self.id = int(id)
        self.titulo = str(titulo).strip()
        self.categoria = str(categoria).strip()
        self.descricao = str(descricao).strip()
        self.documentos = list(documentos or [])
        self.local = str(local).strip()
        self.fonte = str(fonte).strip()
        self.palavras_chave = list(palavras_chave or [])
        self.verificado_em = str(verificado_em).strip()

    def para_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "documentos": self.documentos,
            "local": self.local,
            "fonte": self.fonte,
            "palavras_chave": self.palavras_chave,
            "verificado_em": self.verificado_em,
        }

    @classmethod
    def de_dict(cls, dados):
        if not isinstance(dados, dict):
            raise TypeError("o registro deve ser um objeto")

        descricao = dados.get("descricao", dados.get("resposta"))
        local = dados.get("local", dados.get("onde", ""))

        if descricao is None:
            raise KeyError("descricao")

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
            descricao=str(descricao).strip(),
            documentos=[str(item).strip() for item in documentos if str(item).strip()],
            local=str(local).strip(),
            fonte=str(dados.get("fonte", "")).strip(),
            palavras_chave=[
                str(item).strip() for item in palavras_chave if str(item).strip()
            ],
            verificado_em=str(dados.get("verificado_em", "")).strip(),
        )

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(f"ID: {self.id}")
        print(f"Descrição: {self.descricao}")

        print("Documentos/requisitos:")
        if self.documentos:
            for documento in self.documentos:
                print(f" - {documento}")
        else:
            print(" - Nenhum documento informado.")

        print(f"Local: {self.local or 'não informado'}")

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
