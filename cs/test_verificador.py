import unittest

import assistente
import expressoes
import verificador as v


class TestVerificador(unittest.TestCase):
    def test_numero_de_combinacoes(self):
        self.assertEqual(len(v.combinacoes(3)), 8)
        self.assertEqual(len(v.combinacoes(4)), 16)
        self.assertEqual(len(set(v.combinacoes(4))), 16)

    def test_variaveis_invalidas(self):
        with self.assertRaises(ValueError):
            v.combinacoes(2)
        with self.assertRaises(ValueError):
            v.combinacoes(5)

    def test_ordem(self):
        c = v.combinacoes(3)
        self.assertEqual(c[0], (0, 0, 0))
        self.assertEqual(c[1], (0, 0, 1))
        self.assertEqual(c[-1], (1, 1, 1))

    def test_equivalentes(self):
        f = lambda a, b, c: (a and b) or (a and not b)
        g = lambda a, b, c: a
        self.assertTrue(v.equivalentes("ABC", f, g, g))

    def test_diferentes(self):
        f = lambda a, b, c: a and b
        g = lambda a, b, c: a or b
        linhas = v.verificar("ABC", f, g)
        self.assertEqual(sum(1 for _, r in linhas if r[0] != r[1]), 4)
        self.assertFalse(v.equivalentes("ABC", f, g))

    def test_quatro_variaveis(self):
        f = lambda a, b, c, d: a ^ d
        self.assertTrue(v.equivalentes("ABCD", f, f))
        self.assertEqual(len(v.verificar("ABCD", f, f)), 16)

    def test_listagem(self):
        f = lambda a, b, c: a
        g = lambda a, b, c: b
        titulos = ["original", "simplificada"]
        texto = v.listagem(v.verificar("ABC", f, g), "ABC", titulos)
        self.assertIn("IGUAL", texto)
        self.assertIn("DIFERENTE", texto)
        self.assertIn("NÃO são equivalentes", texto)
        ok = v.listagem(v.verificar("ABC", f, f), "ABC", titulos)
        self.assertNotIn("DIFERENTE", ok)
        self.assertIn("Combinações testadas: 8", ok)


class TestAssistente(unittest.TestCase):
    def test_interpretar(self):
        self.assertEqual(assistente.interpretar("1"), 1)
        self.assertEqual(assistente.interpretar(" Sim "), 1)
        self.assertEqual(assistente.interpretar("0"), 0)
        self.assertEqual(assistente.interpretar("não"), 0)
        for ruim in ("", "2", "x", "10", "-1"):
            self.assertIsNone(assistente.interpretar(ruim))

    def test_ler_bit_repete_ate_valido(self):
        respostas = iter(["abc", "7", "", "1"])
        msgs = []
        valor = assistente.ler_bit("?", lambda _: next(respostas), msgs.append)
        self.assertEqual(valor, 1)
        self.assertEqual(len(msgs), 3)

    def test_decidir_valida_entrada(self):
        n = len(expressoes.NOMES)
        with self.assertRaises(ValueError):
            assistente.decidir(*([1] * (n - 1)))
        with self.assertRaises(ValueError):
            assistente.decidir(*([2] * n))

    def test_rodar_uma_consulta(self):
        n = len(expressoes.NOMES)
        respostas = iter(["x"] + ["1"] * n + ["0"])
        saida = []
        assistente.rodar(lambda _: next(respostas), saida.append)
        texto = "\n".join(saida)
        self.assertIn("não é um canal oficial", texto.lower())
        self.assertIn("Resposta inválida", texto)
        self.assertIn(expressoes.ORIENTACAO[assistente.decidir(*([1] * n))], texto)

    def test_rodar_sair(self):
        saida = []
        assistente.rodar(lambda _: "sair", saida.append)
        self.assertEqual(saida[-1], "Até mais!")


class TestRegraDoTrabalho(unittest.TestCase):
    """Confere o que está em expressoes.py (a regra do Gabriel)."""

    def test_formato(self):
        self.assertIn(len(expressoes.NOMES), (3, 4))
        self.assertEqual(set(expressoes.PERGUNTAS), set(expressoes.NOMES))
        self.assertEqual(set(expressoes.ORIENTACAO), {0, 1})
        self.assertTrue(expressoes.FONTES)

    def test_todas_as_combinacoes_equivalentes(self):
        self.assertTrue(v.equivalentes(expressoes.NOMES, expressoes.original,
                                       expressoes.simplificada, assistente.decidir))


if __name__ == "__main__":
    unittest.main()
