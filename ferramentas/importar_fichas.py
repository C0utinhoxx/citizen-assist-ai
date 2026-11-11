"""Converte as fichas oficiais (formato do professor) para o formato do agente.

As fichas oficiais usam campos em negrito, por exemplo:

    **Custo:** a segunda via custa R$ 38,00.
    **Prazo:** fica pronta em 10 dias úteis.

O agente espera seções Markdown com ``## Título | palavras-chave``. Este script
agrupa os campos em seções coerentes, preserva o texto literal e adiciona os
metadados de fonte, data e palavras-chave.

Uso:
    python3 ferramentas/importar_fichas.py ~/Downloads/referencia

O script não inventa conteúdo: apenas reorganiza os campos existentes.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DESTINO = Path(__file__).resolve().parent.parent / "agente" / "fichas"

CAMPOS = re.compile(r"^\*\*(?P<nome>.+?):\*\*\s*(?P<inicio>.*)$")

ASSUNTOS = {
    "FC-01": "Carteira de Identidade (RG): primeira e segunda via",
    "FC-02": "CPF: inscrição e atendimento",
    "FC-03": "Título de eleitor",
    "FC-04": "Carteira de Trabalho",
    "FC-05": "Certidões de nascimento, casamento e óbito",
    "FC-06": "CNH: renovação",
    "FC-07": "Atendimento, agendamento, terceiros, pagamento e acessibilidade",
}

# A FC-07 oficial não traz uma linha "Palavras-chave". Estes termos são
# apenas índice de busca; não acrescentam fatos ao conteúdo da ficha.
PALAVRAS_PADRAO = {
    "FC-07": (
        "atendimento, agendamento, horario, sabado, domingo, feriado, "
        "terceiros, procuracao, pagamento, prioridade, libras, privacidade, "
        "documentos, canal oficial"
    ),
}

# (título da seção, palavras-chave, campos oficiais que entram nela)
SECOES: Dict[str, List[Tuple[str, str, List[str]]]] = {
    "FC-01": [
        (
            "Custo e prazo",
            "quanto custa, valor, preco, taxa, gratuita, primeira via, "
            "segunda via, prazo, quanto tempo, dias uteis",
            ["Custo", "Prazo"],
        ),
        (
            "Quem pode pedir",
            "quem pode, menor de 12, responsavel legal, filho, crianca",
            ["Quem pode pedir"],
        ),
        (
            "Agendamento",
            "agendamento, agendar, marcar, horario, marcar horario, "
            "precisa agendar, portal, obrigatorio",
            ["Agendamento"],
        ),
        (
            "Documentos necessários para a segunda via",
            "documentos, levar, certidao, comprovante, boletim, extravio, "
            "roubo, furto, perda",
            ["Documentos necessários para a segunda via"],
        ),
        (
            "Passo a passo",
            "passo a passo, como, agendar, pagar, guia, comparecer, retirar",
            ["Passo a passo"],
        ),
        ("Onde", "onde, local, posto de identificacao", ["Onde"]),
    ],
    "FC-02": [
        (
            "Inscrição e atendimento",
            "cpf, inscricao, inscrever, como faco, portal, gratuito, gratis, "
            "taxa, pago, custa, quanto custa, prazo, 2 dias uteis, "
            "formulario, agendamento, sem agendamento, nao exige agendamento, "
            "documentos, passo a passo, onde, privacidade",
            [
                "Custo",
                "Prazo",
                "Agendamento",
                "Documentos necessários",
                "Passo a passo (pelo portal)",
                "Onde",
                "Atenção",
            ],
        ),
    ],
    "FC-03": [
        (
            "Obrigatoriedade e custo",
            "obrigatorio, facultativo, 16, 17, 70, gratuito, gratis, pago, "
            "paga, custa, quanto custa, preco, valor, primeira via, "
            "segunda via, transferencia",
            ["Quem deve ter", "Custo"],
        ),
        ("Prazo", "150 dias, eleicao, cadastro, prazo", ["Prazo"]),
        (
            "Agendamento",
            "agendamento, portal, balcao, central eleitoral",
            ["Agendamento"],
        ),
        (
            "Documentos necessários",
            "documentos, comprovante de residencia",
            ["Documentos necessários"],
        ),
        (
            "Passo a passo",
            "passo a passo, pedido, titulo digital, 5 dias uteis",
            ["Passo a passo"],
        ),
    ],
    "FC-04": [
        (
            "Custo, prazo e agendamento",
            "quanto custa, gratuita, prazo, demora, quanto demora, tempo, "
            "imediato, na hora, digital, agendamento",
            ["Custo", "Prazo", "Agendamento"],
        ),
        (
            "Documentos necessários",
            "documentos, cpf, documento com foto, menor de 18",
            ["Documentos necessários"],
        ),
        (
            "Passo a passo",
            "passo a passo, portal, aplicativo, dados, identidade",
            ["Passo a passo"],
        ),
    ],
    "FC-05": [
        (
            "Custo e prazo",
            "quanto custa, balcao, portal, pdf, 49, 55, 3 dias, 5 dias, "
            "isencao, baixa renda",
            ["Custo e prazo (cada certidão)", "Isenção"],
        ),
        (
            "Agendamento e quem pode pedir",
            "agendamento, nao necessario, terceiros, terceiro, procuracao, "
            "outra pessoa, pedir, representante, quem retira",
            ["Agendamento", "Quem pode pedir"],
        ),
        (
            "Documentos necessários",
            "documentos, documento com foto, dados do registro",
            ["Documentos necessários"],
        ),
        (
            "Passo a passo",
            "passo a passo, canal, dados, guia, retirar, pdf",
            ["Passo a passo"],
        ),
    ],
    "FC-06": [
        (
            "Custo e prazo",
            "quanto custa, taxa, 180, exame medico, prazo, 7 dias uteis",
            ["Custo", "Prazo"],
        ),
        (
            "Quando renovar",
            "quando renovar, antecedencia, 30 dias, vencida, 5 anos, "
            "dirigir, curso, prova",
            ["Quando renovar"],
        ),
        (
            "Validade da CNH renovada",
            "validade, quanto tempo, quanto tempo vale, vale, tempo, faixa, "
            "idade, 10 anos, 5 anos, 3 anos, 50 a 69, 70 anos",
            ["Validade da CNH renovada"],
        ),
        ("Agendamento", "agendamento, obrigatorio, portal", ["Agendamento"]),
        (
            "Documentos necessários",
            "documentos, cnh, comprovante, laudo",
            ["Documentos necessários"],
        ),
        (
            "Passo a passo",
            "passo a passo, exame, agendar, pagar, retirar",
            ["Passo a passo"],
        ),
    ],
    "FC-07": [
        (
            "Horário de atendimento presencial",
            "horario, sabado, sabados, domingo, domingos, feriado, feriados, "
            "8h, 17h, atendem, atende, funcionamento, abre, abrem, "
            "segunda a sexta",
            ["Horário de atendimento presencial"],
        ),
        (
            "Agendamento",
            "agendamento, rg, cnh, cpf, certidoes, titulo",
            ["Agendamento"],
        ),
        (
            "Documentos",
            "documentos, original, fotocopia, copia autenticada",
            ["Documentos"],
        ),
        (
            "Atendimento por terceiros",
            "terceiros, terceiro, outra pessoa, pedir, representante, "
            "procuracao, quem retira, certidao, certidoes, documento, "
            "menor de 12, responsavel",
            ["Atendimento por terceiros"],
        ),
        (
            "Pagamento",
            "pagamento, guia, banco, pix, 2 dias uteis",
            ["Pagamento"],
        ),
        (
            "Atendimento prioritário e Libras",
            "prioritario, 60 anos, gestante, deficiencia, libras, 48 horas",
            ["Atendimento prioritário"],
        ),
        (
            "Perda, roubo ou furto de documento",
            "perda, roubo, furto, boletim de ocorrencia",
            ["Perda, roubo ou furto de documento"],
        ),
        (
            "Privacidade",
            "privacidade, senha, documento, endereco, telefone, chat, mensagem",
            ["Privacidade"],
        ),
    ],
}


def _ler_campos(caminho: Path) -> Tuple[str, Dict[str, List[str]], List[str]]:
    linhas = caminho.read_text(encoding="utf-8-sig").splitlines()
    titulo = linhas[0].lstrip("# ").strip()
    campos: Dict[str, List[str]] = {}
    ordem: List[str] = []
    atual: Optional[str] = None

    for linha in linhas[1:]:
        achado = CAMPOS.match(linha.strip())
        if achado:
            atual = achado.group("nome").strip()
            ordem.append(atual)
            campos[atual] = [achado.group("inicio").rstrip()]
        elif atual is not None:
            campos[atual].append(linha.rstrip())

    for nome in campos:
        while campos[nome] and not campos[nome][-1].strip():
            campos[nome].pop()

    return titulo, campos, ordem


def _formatar_campo(nome: str, linhas: List[str]) -> str:
    if not linhas:
        return f"**{nome}:**"
    primeira = linhas[0].strip()
    resto = linhas[1:]
    if primeira:
        texto = f"**{nome}:** {primeira}"
    else:
        texto = f"**{nome}:**"
    if resto:
        texto += "\n" + "\n".join(resto)
    return texto


def _data_da_fonte(fonte: str) -> str:
    achado = re.search(r"(\d{2})/(\d{2})/(\d{4})", fonte)
    if not achado:
        return "2026-10-01"
    dia, mes, ano = achado.groups()
    return f"{ano}-{mes}-{dia}"


def _converter(caminho: Path) -> Tuple[str, str]:
    ficha_id = caminho.stem.split("_")[0]
    if ficha_id not in SECOES:
        raise ValueError(f"Ficha sem mapeamento: {caminho.name}")

    titulo, campos, ordem = _ler_campos(caminho)
    palavras = " ".join(campos.pop("Palavras-chave", [])).strip()
    if not palavras:
        palavras = PALAVRAS_PADRAO.get(ficha_id, "")
    fonte = " ".join(campos.pop("Fonte", [])).strip()
    if not fonte:
        fonte = f"Central do Cidadão de Aurora, ficha {ficha_id}, versão de 01/10/2026."
    data = _data_da_fonte(fonte)

    usados = {"Palavras-chave", "Fonte"}
    linhas = [
        f"# {titulo}",
        "",
        f"- **Ficha:** {ficha_id}",
        f"- **Assunto:** {ASSUNTOS.get(ficha_id, titulo)}",
        f"- **Fonte:** {fonte}",
        f"- **Data de verificação:** {data} (versão oficial da ficha)",
        f"- **Palavras-chave:** {palavras}",
        "",
    ]

    for titulo_secao, chaves, nomes in SECOES[ficha_id]:
        blocos = []
        for nome in nomes:
            if nome not in campos:
                raise ValueError(
                    f"{caminho.name}: campo não encontrado: {nome!r}"
                )
            usados.add(nome)
            blocos.append(_formatar_campo(nome, campos[nome]))
        linhas.append(f"## {titulo_secao} | {chaves}")
        linhas.append("\n\n".join(blocos))
        linhas.append("")

    restantes = [nome for nome in ordem if nome not in usados]
    if restantes:
        linhas.append("## Outras informações | informações adicionais")
        for nome in restantes:
            linhas.append(_formatar_campo(nome, campos[nome]))
        linhas.append("")

    return ficha_id, "\n".join(linhas).rstrip() + "\n"


def main(origem: Path) -> int:
    if not origem.is_dir():
        print(f"Pasta não encontrada: {origem}")
        return 1

    arquivos = sorted(origem.glob("FC-*.md"))
    if len(arquivos) != 7:
        print(f"Esperadas 7 fichas, encontradas {len(arquivos)} em {origem}")
        return 1

    DESTINO.mkdir(parents=True, exist_ok=True)
    for caminho in arquivos:
        ficha_id, conteudo = _converter(caminho)
        destino = DESTINO / caminho.name
        destino.write_text(conteudo, encoding="utf-8")
        print(f"{ficha_id}: {destino.name}")

    leia_me = origem / "00_LEIA-ME.md"
    if leia_me.exists():
        shutil.copyfile(leia_me, DESTINO / "00_LEIA-ME.md")
        print("00_LEIA-ME.md copiado")

    print(f"Fichas convertidas em {DESTINO}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 ferramentas/importar_fichas.py PASTA_DAS_FICHAS")
        raise SystemExit(2)
    raise SystemExit(main(Path(sys.argv[1]).expanduser()))
