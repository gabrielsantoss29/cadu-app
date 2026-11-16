"""Testes automáticos sem bibliotecas externas: python testes_sers.py"""
import unittest
from calculo_energia import carregar_energia, calcular_consumo_mensal, comparar_banho
from integracao_cadu import responder_energia


class TestesSERS(unittest.TestCase):
    def test_json_carrega(self):
        dados = carregar_energia()
        self.assertGreaterEqual(len(dados['aparelhos']), 2)
        self.assertEqual(len(dados['orientacoes']), 2)

    def test_chuveiro_base(self):
        r = calcular_consumo_mensal([{'nome': 'Chuveiro', 'potencia_w': 5500,
                                    'horas_por_dia': 1/3, 'dias_por_mes': 30}])
        self.assertAlmostEqual(r['total_kwh_mes'], 55, places=2)

    def test_cenarios(self):
        r = comparar_banho(5500, 1/3, 1/6, 30, 0.7)
        self.assertAlmostEqual(r['cenario_base']['consumo_estimado_kwh_mes'], 55)
        self.assertAlmostEqual(r['alternativa_1_banho_mais_curto']['consumo_estimado_kwh_mes'], 27.5)
        self.assertAlmostEqual(r['alternativa_2_aquecimento_solar_termico']['consumo_estimado_kwh_mes'], 16.5)

    def test_sem_tarifa_nao_exibe_reais(self):
        r = comparar_banho(5500, 1/3, 1/6, 30, 0.7)
        self.assertNotIn('economia_estimativa_r_mes', r['alternativa_1_banho_mais_curto'])
        self.assertNotIn('R$', responder_energia('comparar'))

    def test_tarifa_opcional(self):
        r = comparar_banho(5500, 1/3, 1/6, 30, 0.7, tarifa_r_kwh=0.9)
        self.assertAlmostEqual(r['alternativa_2_aquecimento_solar_termico']['economia_estimativa_r_mes'], 34.65)

    def test_dados_invalidos(self):
        with self.assertRaises(ValueError):
            comparar_banho(5500, 1/3, 1/6, 30, 1.5)
        with self.assertRaises(ValueError):
            calcular_consumo_mensal([{'potencia_w': -10, 'horas_por_dia': 1}])

    def test_respostas_acessiveis(self):
        for acao in ('consumo', 'comparar', 'dicas'):
            self.assertTrue(responder_energia(acao))
        self.assertIn('Não entendi', responder_energia('invalida'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
