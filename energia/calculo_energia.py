"""Cadu/SERS: estimativas transparentes de energia e alternativas para banho.

Uso no projeto:
    from calculo_energia import calcular_consumo_mensal, comparar_banho

Nenhum dado pessoal e solicitado ou armazenado. Nao estima a fatura oficial.
"""
from __future__ import annotations

import json
from pathlib import Path


BASE = Path(__file__).resolve().parent / "energia.json"


def carregar_energia(caminho: str | Path = BASE) -> dict:
    """Carrega os aparelhos e as orientacoes do JSON."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def calcular_consumo_mensal(aparelhos: list[dict]) -> dict:
    """Consumo = potencia(W)/1000 * horas/dia * dias/mes * quantidade.

    Retorna valores mensais, nao valores medidos em uma residencia.
    """
    itens = []
    for aparelho in aparelhos:
        nome = str(aparelho.get("nome", "Aparelho"))
        potencia = float(aparelho["potencia_w"])
        horas = float(aparelho["horas_por_dia"])
        dias = float(aparelho.get("dias_por_mes", 30))
        quantidade = int(aparelho.get("quantidade", 1))
        if not (0 <= potencia and 0 <= horas <= 24 and 0 <= dias <= 31 and quantidade >= 1):
            raise ValueError(f"Valores invalidos para {nome}.")
        kwh = potencia / 1000 * horas * dias * quantidade
        itens.append({"nome": nome, "consumo_kwh_mes": round(kwh, 3)})
    return {"itens": itens, "total_kwh_mes": round(sum(i["consumo_kwh_mes"] for i in itens), 3)}


def comparar_banho(potencia_w: float, horas_base_dia: float,
                   horas_reduzidas_dia: float, dias_mes: int,
                   fracao_substituida_solar: float, tarifa_r_kwh: float | None = None,
                   investimento_solar_r: float | None = None) -> dict:
    """Duas alternativas PARA A MESMA NECESSIDADE: banho quente.

    A energia termica solar e ilustrada pela fracao hipotetica de eletricidade
    substituida. Nao e uma previsao de desempenho de coletor solar.
    """
    if potencia_w < 0 or not 0 <= horas_reduzidas_dia <= horas_base_dia <= 24:
        raise ValueError("Potencia ou tempos de banho invalidos.")
    if not 1 <= dias_mes <= 31 or not 0 <= fracao_substituida_solar <= 1:
        raise ValueError("Dias ou fracao solar invalidos.")
    if tarifa_r_kwh is not None and tarifa_r_kwh < 0:
        raise ValueError("Tarifa deve ser nao negativa.")
    if investimento_solar_r is not None and investimento_solar_r < 0:
        raise ValueError("Investimento deve ser nao negativo.")

    base = potencia_w / 1000 * horas_base_dia * dias_mes
    curto = potencia_w / 1000 * horas_reduzidas_dia * dias_mes
    solar = base * (1 - fracao_substituida_solar)

    def opcao(consumo: float) -> dict:
        economizado = base - consumo
        resultado = {
            "consumo_estimado_kwh_mes": round(consumo, 3),
            "economia_estimada_kwh_mes": round(economizado, 3),
            "reducao_percentual": round(100 * economizado / base, 2) if base else 0.0,
        }
        if tarifa_r_kwh is not None:
            resultado["economia_estimativa_r_mes"] = round(economizado * tarifa_r_kwh, 2)
        return resultado

    solar_resultado = opcao(solar)
    if investimento_solar_r is not None and tarifa_r_kwh is not None:
        economia_r = (base - solar) * tarifa_r_kwh
        solar_resultado["retorno_simples_meses_ilustrativo"] = (
            round(investimento_solar_r / economia_r, 1) if economia_r > 0 else None
        )
    return {
        "necessidade": "Agua quente para banho",
        "cenario_base": opcao(base),
        "alternativa_1_banho_mais_curto": opcao(curto),
        "alternativa_2_aquecimento_solar_termico": solar_resultado,
        "aviso": "Valores estimados; nao incluem impostos, bandeiras, disponibilidade de sol, manutencao ou perdas. Solar depende de viabilidade local e orcamento.",
    }


if __name__ == "__main__":
    dados = carregar_energia()
    print("=== CADU: CONSUMO ESTIMADO ===")
    consumo = calcular_consumo_mensal(dados["aparelhos"])
    for item in consumo["itens"]:
        print(f"{item['nome']}: {item['consumo_kwh_mes']:.2f} kWh/mes")
    print(f"TOTAL ilustrativo: {consumo['total_kwh_mes']:.2f} kWh/mes\n")

    c = dados["comparacao_exemplo"]
    resultados = comparar_banho(
        potencia_w=c["chuveiro_potencia_w"],
        horas_base_dia=c["horas_banho_total_dia_base"],
        horas_reduzidas_dia=c["horas_banho_total_dia_reduzido"],
        dias_mes=c["dias_mes"],
        fracao_substituida_solar=c["fracao_substituida_solar"],
    )
    print("=== MESMA NECESSIDADE: BANHO QUENTE ===")
    for nome, valor in resultados.items():
        if isinstance(valor, dict):
            print(f"{nome}: {valor}")
    print("AVISO:", resultados["aviso"])
