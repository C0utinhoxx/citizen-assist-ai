import time
from datetime import datetime
from pathlib import Path

from .base_conhecimento import PONTOS_ALTA, PONTOS_MEDIA
from .persistencia import (
    carregar_historico,
    exportar_csv,
    salvar_historico,
)

PASTA_DADOS = Path(__file__).resolve().parents[1] / "data"


class Assistente:

    def __init__(self, nome, base, caminho_historico=None, caminho_csv=None):
        self.nome = nome
        self.base = base
        self.caminho_historico = str(
            caminho_historico or PASTA_DADOS / "historico.json"
        )
        self.caminho_csv = str(caminho_csv or PASTA_DADOS / "atendimentos.csv")
        self.historico = carregar_historico(self.caminho_historico)
        self.nota_facilidade = None

    def contem_dado_pessoal(self, texto):
        quantidade_digitos = sum(1 for caractere in texto if caractere.isdigit())
        return quantidade_digitos >= 8 or "@" in texto

    def _ler_opcao(self, maximo):
        entrada = input("Opção: ").strip()

        if not entrada.isdigit():
            print("Entrada inválida. Digite um número.")
            return None

        numero = int(entrada)
        if numero < 0 or numero > maximo:
            print(f"Entrada inválida. Digite um número de 0 a {maximo}.")
            return None

        return numero

    def _ler_sim_nao(self, mensagem, aceitar_zero=False):
        while True:
            resposta = input(mensagem).strip().lower()

            if resposta == "s":
                return True
            if resposta == "n":
                return False
            if aceitar_zero and resposta == "0":
                return None

            if aceitar_zero:
                print("Responda com s (sim), n (não) ou 0 para sair.")
            else:
                print("Responda com s (sim) ou n (não).")

    def _ler_nota(self):
        while True:
            entrada = input("Que nota de 1 a 5 você dá para a facilidade de uso? ").strip()
            if entrada.isdigit() and 1 <= int(entrada) <= 5:
                return int(entrada)
            print("Entrada inválida. Digite um número de 1 a 5.")

    def perguntar(self):
        print("\n--- Fazer uma pergunta ---")

        pergunta_original = None
        inicio = None
        tentativas = 0

        while True:
            pergunta = input("Digite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("Por favor, escreva sua dúvida.")
                continue

            if self.contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            if pergunta_original is None:
                pergunta_original = pergunta
                inicio = time.time()

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if resultados and resultados[0][0] >= PONTOS_MEDIA:
                pontos, melhor = resultados[0]
                confianca = "ALTA" if pontos >= PONTOS_ALTA else "MÉDIA"

                print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)\n")
                melhor.exibir()

                alternativas = [orientacao for _, orientacao in resultados[1:3]]
                if alternativas:
                    print("\nOutras orientações parecidas:")
                    for orientacao in alternativas:
                        print(f" - {orientacao.titulo} [{orientacao.categoria}]")

                ajudou = self._ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                tempo = round(time.time() - inicio, 1)
                self.registrar("pergunta", pergunta_original, melhor.id,
                               True, ajudou, tentativas, tempo)
                return

            print("\nNão encontrei uma orientação para essa dúvida.")
            print("Tente usar outras palavras ou escolha uma categoria:")
            for categoria in self.base.categorias():
                print(f" - {categoria}")

            continuar = self._ler_sim_nao(
                "Deseja tentar outra pergunta? (s/n, 0 para sair): ",
                aceitar_zero=True,
            )
            if not continuar:
                tempo = round(time.time() - inicio, 1)
                self.registrar("pergunta", pergunta_original, None,
                               False, False, tentativas, tempo)
                return

    def navegar(self):
        while True:
            categorias = self.base.categorias()

            if not categorias:
                print("A base de conhecimento está vazia. Não há categorias para mostrar.")
                return

            print("\n--- Categorias ---")
            for indice, categoria in enumerate(categorias, start=1):
                print(f"{indice} - {categoria}")
            print("0 - Voltar")

            opcao = self._ler_opcao(len(categorias))
            if opcao is None:
                continue
            if opcao == 0:
                return

            self._navegar_categoria(categorias[opcao - 1])

    def _navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)

        while True:
            print(f"\n--- {categoria} ---")
            for indice, orientacao in enumerate(orientacoes, start=1):
                print(f"{indice} - {orientacao.titulo}")
            print("0 - Voltar")

            opcao = self._ler_opcao(len(orientacoes))
            if opcao is None:
                continue
            if opcao == 0:
                return

            orientacao = orientacoes[opcao - 1]
            inicio = time.time()

            print()
            orientacao.exibir()

            ajudou = self._ler_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("categoria", orientacao.titulo, orientacao.id,
                           True, ajudou, 1, tempo)
            return

    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": tempo,
        }

        self.historico.append(registro)
        salvar_historico(self.caminho_historico, self.historico)
        return registro

    def calcular_indicadores(self):
        total = len(self.historico)

        encontrados = sum(1 for r in self.historico if r.get("encontrou"))
        ajudaram = sum(1 for r in self.historico if r.get("ajudou"))

        tentativas_medias = 0.0
        if total:
            tentativas_medias = (
                sum(int(r.get("tentativas", 1)) for r in self.historico) / total
            )

        tempos = [
            float(r.get("tempo", 0))
            for r in self.historico
            if r.get("encontrou")
        ]
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0.0

        notas = [
            r["nota_facilidade"]
            for r in self.historico
            if "nota_facilidade" in r
        ]
        if notas:
            facilidade = f"{sum(notas) / len(notas):.1f} (1 a 5)"
        elif self.nota_facilidade is not None:
            facilidade = f"{self.nota_facilidade} (1 a 5)"
        else:
            facilidade = "não avaliada"

        sem_solucao = []
        for registro in self.historico:
            if not registro.get("ajudou"):
                pergunta = registro.get("pergunta", "")
                if pergunta and pergunta not in sem_solucao:
                    sem_solucao.append(pergunta)

        return {
            "total": total,
            "encontrados": encontrados,
            "ajudaram": ajudaram,
            "percentual_encontrados": 100 * encontrados / total if total else 0.0,
            "percentual_ajudaram": 100 * ajudaram / total if total else 0.0,
            "tempo_medio": tempo_medio,
            "tentativas_medias": tentativas_medias,
            "facilidade": facilidade,
            "sem_solucao": sem_solucao,
        }

    def indicadores(self):
        dados = self.calcular_indicadores()
        print("\n--- Indicadores de atendimento ---")

        if dados["total"] == 0:
            print("Nenhum atendimento registrado ainda.")
            print(f"Facilidade de uso: {dados['facilidade']}")
            return

        print(f"Atendimentos: {dados['total']}")
        print(f"Resposta encontrada: {dados['percentual_encontrados']:.1f}%")
        print(f"Ajudou a resolver a dúvida: {dados['percentual_ajudaram']:.1f}%")
        print(f"Tempo médio para encontrar: {dados['tempo_medio']:.1f} s")
        print(f"Tentativas por atendimento: {dados['tentativas_medias']:.1f}")
        print(f"Facilidade de uso: {dados['facilidade']}")

        print("Dúvidas sem solução:")
        if dados["sem_solucao"]:
            for pergunta in dados["sem_solucao"][:5]:
                print(f" - {pergunta}")
        else:
            print(" - Nenhuma")

    def exportar_csv(self):
        return exportar_csv(self.caminho_csv, self.historico)

    def finalizar(self):
        print("\n--- Encerrando o atendimento ---")
        self.nota_facilidade = self._ler_nota()

        if self.historico:
            self.historico[-1]["nota_facilidade"] = self.nota_facilidade
            salvar_historico(self.caminho_historico, self.historico)

        self.exportar_csv()
        self.indicadores()
        print(f"\nObrigado por usar o {self.nome}!")
