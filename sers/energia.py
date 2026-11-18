from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Premissas:
    consumo_mensal_kwh: float = 150.0
    tarifa_rs_kwh: float = 0.90
    dias_no_mes: int = 30
    meses_no_ano: int = 12

    lampadas: int = 5
    potencia_antiga_w: float = 60.0
    potencia_led_w: float = 9.0
    horas_led_dia: float = 2.0
    custo_led_rs: float = 15.0
    potencia_standby_w: float = 8.0
    custo_corta_standby_rs: float = 60.0

    produtividade_kwh_kwp_ano: float = 1200.0
    custo_kwp_rs: float = 5000.0
    fator_compensacao: float = 0.85
    vida_util_anos: int = 25

    fator_emissao_kg_kwh: float = 0.040

    def validar(self) -> None:
        campos_positivos = {
            "consumo_mensal_kwh": self.consumo_mensal_kwh,
            "tarifa_rs_kwh": self.tarifa_rs_kwh,
            "lampadas": self.lampadas,
            "potencia_antiga_w": self.potencia_antiga_w,
            "potencia_led_w": self.potencia_led_w,
            "horas_led_dia": self.horas_led_dia,
            "custo_led_rs": self.custo_led_rs,
            "potencia_standby_w": self.potencia_standby_w,
            "custo_corta_standby_rs": self.custo_corta_standby_rs,
            "produtividade_kwh_kwp_ano": self.produtividade_kwh_kwp_ano,
            "custo_kwp_rs": self.custo_kwp_rs,
        }
        for nome, valor in campos_positivos.items():
            if not isinstance(valor, (int, float)) or valor <= 0:
                raise ValueError(f"Premissa inválida: {nome} deve ser maior que zero.")

        if self.potencia_led_w >= self.potencia_antiga_w:
            raise ValueError("A lâmpada LED deve consumir menos que a lâmpada antiga.")
        if not 0 < self.fator_compensacao <= 1:
            raise ValueError("O fator de compensação deve ficar entre 0 e 1.")
        if self.dias_no_mes <= 0 or self.meses_no_ano <= 0:
            raise ValueError("Dias e meses devem ser maiores que zero.")


def _arredondar(valor: float, casas: int = 2) -> float:
    return round(valor + 1e-9, casas)


def _payback_meses(investimento: float, economia_mes: float) -> float:
    if economia_mes <= 0:
        return float("inf")
    return _arredondar(investimento / economia_mes, 1)


def _payback_anos(investimento: float, economia_ano: float) -> float:
    if economia_ano <= 0:
        return float("inf")
    return _arredondar(investimento / economia_ano, 1)


def economia_eficiencia(p: Premissas) -> Dict[str, float]:
    p.validar()

    economia_led_dia = (
        (p.potencia_antiga_w - p.potencia_led_w) * p.lampadas * p.horas_led_dia
    ) / 1000.0
    economia_led_mes = economia_led_dia * p.dias_no_mes

    economia_standby_dia = (p.potencia_standby_w * 24.0) / 1000.0
    economia_standby_mes = economia_standby_dia * p.dias_no_mes

    economia_kwh_mes = economia_led_mes + economia_standby_mes
    economia_kwh_ano = economia_kwh_mes * p.meses_no_ano

    economia_rs_mes = economia_kwh_mes * p.tarifa_rs_kwh
    economia_rs_ano = economia_rs_mes * p.meses_no_ano

    investimento = (
        p.lampadas * p.custo_led_rs + p.custo_corta_standby_rs
    )

    return {
        "economia_led_kwh_mes": _arredondar(economia_led_mes),
        "economia_standby_kwh_mes": _arredondar(economia_standby_mes),
        "economia_kwh_mes": _arredondar(economia_kwh_mes),
        "economia_kwh_ano": _arredondar(economia_kwh_ano),
        "economia_rs_mes": _arredondar(economia_rs_mes),
        "economia_rs_ano": _arredondar(economia_rs_ano),
        "investimento_rs": _arredondar(investimento),
        "payback_meses": _payback_meses(investimento, economia_rs_mes),
        "payback_anos": _payback_anos(investimento, economia_rs_ano),
        "co2_evitado_kg_ano": _arredondar(
            economia_kwh_ano * p.fator_emissao_kg_kwh
        ),
        "consumo_reduzido_kwh_mes": _arredondar(
            p.consumo_mensal_kwh - economia_kwh_mes
        ),
    }


def economia_solar(p: Premissas, consumo_mensal_kwh: float | None = None) -> Dict[str, float]:
    p.validar()
    consumo = (
        p.consumo_mensal_kwh if consumo_mensal_kwh is None else consumo_mensal_kwh
    )
    if consumo <= 0:
        raise ValueError("O consumo deve ser maior que zero.")

    consumo_anual = consumo * p.meses_no_ano
    potencia_kwp = math.ceil(
        (consumo_anual / p.produtividade_kwh_kwp_ano) * 10.0
    ) / 10.0
    geracao_kwh_ano = potencia_kwp * p.produtividade_kwh_kwp_ano
    energia_compensada = min(geracao_kwh_ano, consumo_anual)

    economia_rs_ano = (
        energia_compensada * p.tarifa_rs_kwh * p.fator_compensacao
    )
    investimento = potencia_kwp * p.custo_kwp_rs

    return {
        "consumo_anual_kwh": _arredondar(consumo_anual),
        "potencia_kwp": _arredondar(potencia_kwp, 1),
        "geracao_kwh_ano": _arredondar(geracao_kwh_ano),
        "energia_compensada_kwh_ano": _arredondar(energia_compensada),
        "economia_rs_ano": _arredondar(economia_rs_ano),
        "economia_rs_mes": _arredondar(economia_rs_ano / p.meses_no_ano),
        "investimento_rs": _arredondar(investimento),
        "payback_anos": _payback_anos(investimento, economia_rs_ano),
        "payback_meses": _payback_meses(investimento, economia_rs_ano / p.meses_no_ano),
        "co2_evitado_kg_ano": _arredondar(
            energia_compensada * p.fator_emissao_kg_kwh
        ),
        "economia_liquida_25_anos_rs": _arredondar(
            economia_rs_ano * p.vida_util_anos - investimento
        ),
        "area_aproximada_m2": _arredondar(potencia_kwp * 4.0, 1),
    }


def analisar(p: Premissas | None = None) -> Dict[str, object]:
    p = p or Premissas()
    p.validar()

    eficiencia = economia_eficiencia(p)
    solar = economia_solar(p)

    consumo_com_eficiencia = eficiencia["consumo_reduzido_kwh_mes"]
    solar_com_eficiencia = economia_solar(p, consumo_com_eficiencia)

    investimento_combinado = (
        eficiencia["investimento_rs"] + solar_com_eficiencia["investimento_rs"]
    )
    economia_combinada_ano = (
        eficiencia["economia_rs_ano"] + solar_com_eficiencia["economia_rs_ano"]
    )
    co2_combinado = (
        eficiencia["co2_evitado_kg_ano"]
        + solar_com_eficiencia["co2_evitado_kg_ano"]
    )

    combinado = {
        "investimento_rs": _arredondar(investimento_combinado),
        "economia_rs_ano": _arredondar(economia_combinada_ano),
        "economia_rs_mes": _arredondar(economia_combinada_ano / p.meses_no_ano),
        "payback_anos": _payback_anos(investimento_combinado, economia_combinada_ano),
        "co2_evitado_kg_ano": _arredondar(co2_combinado),
        "solar": solar_com_eficiencia,
    }

    return {
        "premissas": asdict(p),
        "eficiencia": eficiencia,
        "solar": solar,
        "combinado": combinado,
        "recomendacao": _recomendacao(eficiencia, solar),
    }


def _recomendacao(eficiencia: Dict[str, float], solar: Dict[str, float]) -> List[str]:
    return [
        "Comece pela eficiência: custo baixo, payback rápido e funciona também "
        "para quem aluga.",
        "Avalie o solar se a casa for própria, o telhado tiver sombra livre e "
        "houver condições de investir ou financiar.",
        "Antes de investir, verifique se a família tem direito à Tarifa Social "
        "de Energia Elétrica (ANEEL).",
        "Trate os valores como estimativas: tarifa, impostos, bandeiras, "
        "consumo e orçamento local mudam o resultado.",
    ]


FONTES = [
    {
        "tema": "Consumo residencial médio",
        "fonte": "EPE — Anuário Estatístico de Energia Elétrica 2025",
        "url": "https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-160/topico-168/anuario-factsheet.pdf",
        "uso": "Média residencial nacional de 183,8 kWh/mês; adotamos 150 kWh/mês como estimativa conservadora para o público.",
        "data": "2026-11-18",
    },
    {
        "tema": "Tarifa residencial",
        "fonte": "ANEEL / Enel São Paulo — Tarifa B1 (RTA 2025)",
        "url": "https://www.gov.br/mme/pt-br/assuntos/secretarias/secretaria-nacional-energia-eletrica/informativo-tarifario-do-setor-eletrico/informativo-tarifario-do-setor-eletrico-ano-2025.pdf",
        "uso": "Tarifa B1 da Enel SP de R$ 725,18/MWh em jul/2025; com ICMS de 18%, cerca de R$ 0,86/kWh. Adotamos R$ 0,90/kWh.",
        "data": "2026-11-18",
    },
    {
        "tema": "Geração solar",
        "fonte": "EPE/CRESESB e literatura técnica — irradiação de São Paulo",
        "url": "https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/atlas-de-energia-solar-brasileira",
        "uso": "Irradiação média de 4,46 kWh/m²/dia e desempenho de 74% resultam em cerca de 1.200 kWh/kWp/ano.",
        "data": "2026-11-18",
    },
    {
        "tema": "Custo do sistema solar",
        "fonte": "CustoSolar — preços residenciais 2026 (faixa de mercado)",
        "url": "https://custosolar.com/blog/quanto-custa-energia-solar-2026-precos-reais/",
        "uso": "Faixa de R$ 4.800 a R$ 5.500/kWp; adotamos R$ 5.000/kWp como estimativa conservadora.",
        "data": "2026-11-18",
    },
    {
        "tema": "Fator de emissão",
        "fonte": "MCTI — fatores de emissão do SIN, ano-base 2024",
        "url": "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao",
        "uso": "Fator médio de cerca de 40 kg CO2/MWh; adotamos 0,040 kg CO2/kWh.",
        "data": "2026-11-18",
    },
    {
        "tema": "Tarifa Social",
        "fonte": "ANEEL — Tarifa Social de Energia Elétrica",
        "url": "https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social",
        "uso": "Regra de 2026: desconto de 100% no consumo até 80 kWh/mês para quem atende aos critérios.",
        "data": "2026-11-18",
    },
]


def _linha(tabela: List[List[str]]) -> str:
    larguras = [max(len(str(linha[i])) for linha in tabela) for i in range(len(tabela[0]))]
    saida = []
    for indice, linha in enumerate(tabela):
        saida.append(" | ".join(str(c).ljust(larguras[i]) for i, c in enumerate(linha)))
        if indice == 0:
            saida.append("-+-".join("-" * largura for largura in larguras))
    return "\n".join(saida)


def formatar_relatorio(resultado: Dict[str, object] | None = None) -> str:
    dados = resultado or analisar()
    p = dados["premissas"]
    eficiencia = dados["eficiencia"]
    solar = dados["solar"]
    combinado = dados["combinado"]

    tabela = [
        ["Indicador", "Eficiência (LED + standby)", "Solar fotovoltaica"],
        ["Investimento estimado", f"R$ {eficiencia['investimento_rs']:.2f}", f"R$ {solar['investimento_rs']:.2f}"],
        ["Economia por mês", f"R$ {eficiencia['economia_rs_mes']:.2f}", f"R$ {solar['economia_rs_mes']:.2f}"],
        ["Economia por ano", f"R$ {eficiencia['economia_rs_ano']:.2f}", f"R$ {solar['economia_rs_ano']:.2f}"],
        ["Payback", f"{eficiencia['payback_anos']:.1f} ano(s)", f"{solar['payback_anos']:.1f} ano(s)"],
        ["CO2 evitado por ano", f"{eficiencia['co2_evitado_kg_ano']:.1f} kg", f"{solar['co2_evitado_kg_ano']:.1f} kg"],
    ]

    linhas = [
        "ENERGIA E SUSTENTABILIDADE (SERS) — ESTIMATIVAS",
        "",
        f"Consumo considerado: {p['consumo_mensal_kwh']:.1f} kWh/mês "
        f"({p['consumo_mensal_kwh'] * p['meses_no_ano']:.0f} kWh/ano).",
        f"Tarifa considerada: R$ {p['tarifa_rs_kwh']:.2f}/kWh.",
        f"Fator de emissão: {p['fator_emissao_kg_kwh']:.3f} kg CO2/kWh.",
        "",
        "ALTERNATIVA A — EFICIÊNCIA ENERGÉTICA",
        f"- Troca de {p['lampadas']} lâmpadas de {p['potencia_antiga_w']:.0f} W por LED de "
        f"{p['potencia_led_w']:.0f} W, {p['horas_led_dia']:.0f} h/dia: "
        f"{eficiencia['economia_led_kwh_mes']:.1f} kWh/mês.",
        f"- Corte de {p['potencia_standby_w']:.0f} W de standby: "
        f"{eficiencia['economia_standby_kwh_mes']:.1f} kWh/mês.",
        f"- Total: {eficiencia['economia_kwh_mes']:.1f} kWh/mês e "
        f"{eficiencia['economia_kwh_ano']:.1f} kWh/ano.",
        f"- Economia: R$ {eficiencia['economia_rs_mes']:.2f}/mês e "
        f"R$ {eficiencia['economia_rs_ano']:.2f}/ano.",
        f"- Investimento: R$ {eficiencia['investimento_rs']:.2f}; payback de "
        f"{eficiencia['payback_meses']:.1f} meses.",
        "",
        "ALTERNATIVA B — GERAÇÃO SOLAR FOTOVOLTAICA",
        f"- Potência necessária: {solar['potencia_kwp']:.1f} kWp.",
        f"- Geração estimada: {solar['geracao_kwh_ano']:.0f} kWh/ano.",
        f"- Investimento: R$ {solar['investimento_rs']:.2f}.",
        f"- Economia: R$ {solar['economia_rs_ano']:.2f}/ano, com fator de "
        f"compensação de {p['fator_compensacao']:.0%}.",
        f"- Payback: {solar['payback_anos']:.1f} anos; economia líquida em "
        f"{p['vida_util_anos']} anos: R$ {solar['economia_liquida_25_anos_rs']:.2f}.",
        f"- Área aproximada: {solar['area_aproximada_m2']:.1f} m².",
        "",
        "CENÁRIO COMBINADO (EFICIÊNCIA + SOLAR)",
        f"- Investimento: R$ {combinado['investimento_rs']:.2f}.",
        f"- Economia: R$ {combinado['economia_rs_ano']:.2f}/ano; payback de "
        f"{combinado['payback_anos']:.1f} anos.",
        f"- CO2 evitado: {combinado['co2_evitado_kg_ano']:.1f} kg/ano.",
        "",
        "COMPARAÇÃO",
        _linha(tabela),
        "",
        "RECOMENDAÇÃO",
    ]
    linhas.extend(f"- {item}" for item in dados["recomendacao"])
    linhas.extend([
        "",
        "FONTES E CONDIÇÕES",
    ])
    for fonte in FONTES:
        linhas.append(
            f"- {fonte['tema']}: {fonte['fonte']} — {fonte['url']} "
            f"(consultado em {fonte['data']})."
        )
    linhas.extend([
        "",
        "AVISO: os valores são estimativas educacionais, não garantia de economia. "
        "Tarifa, impostos, bandeiras, consumo, sombreamento, estrutura do telhado "
        "e orçamento local alteram o resultado. Confirme com a distribuidora e "
        "com um profissional habilitado. Este assistente não é um canal oficial.",
    ])
    return "\n".join(linhas)


if __name__ == "__main__":
    print(formatar_relatorio())
