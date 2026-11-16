"""Ponto de integração simples para o assistente Cadu (SERS).

Uso:
    from integracao_cadu import responder_energia
    print(responder_energia('comparar'))

NÃO solicita nem armazena dados pessoais.
"""
from __future__ import annotations
from calculo_energia import carregar_energia, calcular_consumo_mensal, comparar_banho


def responder_energia(acao: str, parametros: dict | None = None) -> str:
    """Retorna texto acessível para: 'consumo', 'comparar' ou 'dicas'."""
    dados = carregar_energia()
    parametros = parametros or {}
    aviso = 'Estimativa educativa, não é uma medição nem garantia de economia.'
    if acao == 'consumo':
        aparelhos = parametros.get('aparelhos', dados['aparelhos'])
        resultado = calcular_consumo_mensal(aparelhos)
        itens = '\n'.join(f"- {item['nome']}: {item['consumo_kwh_mes']:.2f} kWh/mês"
                          for item in resultado['itens'])
        return (f'Consumo elétrico mensal estimado:\n{itens}\n'
                f"Total: {resultado['total_kwh_mes']:.2f} kWh/mês.\n"
                'Verifique potência e tempo de uso reais na etiqueta e nos seus hábitos.\n'
                f"{aviso}\nFonte: EPE (dados regionais) e tabela histórica Procel/USP; veja energia.json.")
    if acao == 'comparar':
        c = dados['comparacao_exemplo']
        argumentos = {
            'potencia_w': c['chuveiro_potencia_w'],
            'horas_base_dia': c['horas_banho_total_dia_base'],
            'horas_reduzidas_dia': c['horas_banho_total_dia_reduzido'],
            'dias_mes': c['dias_mes'],
            'fracao_substituida_solar': c['fracao_substituida_solar'],
        }
        argumentos.update(parametros)
        r = comparar_banho(**argumentos)
        base = r['cenario_base']['consumo_estimado_kwh_mes']
        curto = r['alternativa_1_banho_mais_curto']
        solar = r['alternativa_2_aquecimento_solar_termico']
        texto = (f'No período considerado, o chuveiro usa cerca de {base:.2f} kWh.\n'
                 f"Banhos mais curtos: {curto['consumo_estimado_kwh_mes']:.2f} kWh; "
                 f"economia estimada de {curto['economia_estimada_kwh_mes']:.2f} kWh.\n"
                 f"Solar térmico: {solar['consumo_estimado_kwh_mes']:.2f} kWh de apoio elétrico; "
                 f"economia hipotética de {solar['economia_estimada_kwh_mes']:.2f} kWh.\n")
        if 'economia_estimativa_r_mes' in curto:
            texto += (f"Economia estimada na eletricidade, com a tarifa informada: "
                      f"R$ {curto['economia_estimativa_r_mes']:.2f} (banho curto) e "
                      f"R$ {solar['economia_estimativa_r_mes']:.2f} (solar).\n")
        return (texto + 'Banhos curtos mudam a duração do serviço; o solar exige investimento, '
                'instalação, insolação e manutenção. A substituição solar é hipótese, não promessa.\n'
                f'{aviso}\nFontes: ProjetEEE/MME e estudo científico, identificados em energia.json.')
    if acao == 'dicas':
        return ('Dicas de energia:\n' + '\n'.join('- ' + o['mensagem_simples'] for o in dados['orientacoes'])
                + '\nConsulte os limites e as fontes disponíveis em energia.json.\n' + aviso)
    return 'Não entendi. Você quer calcular consumo, comparar alternativas ou ver dicas de energia?'


if __name__ == '__main__':
    for opcao in ('consumo', 'comparar', 'dicas'):
        print('\n===', opcao.upper(), '===')
        print(responder_energia(opcao))
