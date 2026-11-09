import unittest

import verificador as v


class TestVerificador(unittest.TestCase):
    def test_numero_de_combinacoes(self):
        self.assertEqual(len(v.combinacoes(3)), 8)
        self.assertEqual(len(v.combinacoes(4)), 16)

    def test_variaveis_invalidas(self):
        with self.assertRaises(ValueError):
            v.combinacoes(2)

    def test_ordem(self):
        c = v.combinacoes(3)
        self.assertEqual(c[0], (0, 0, 0))
        self.assertEqual(c[1], (0, 0, 1))
        self.assertEqual(c[-1], (1, 1, 1))

    def test_equivalentes(self):
        f = lambda a, b, c: (a and b) or (a and not b)
        g = lambda a, b, c: a
        self.assertTrue(v.equivalentes(f, g, "ABC"))

    def test_diferentes(self):
        f = lambda a, b, c: a and b
        g = lambda a, b, c: a or b
        linhas = v.verificar(f, g, "ABC")
        self.assertEqual(sum(1 for _, x, y in linhas if x != y), 4)
        self.assertFalse(v.equivalentes(f, g, "ABC"))

    def test_quatro_variaveis(self):
        f = lambda a, b, c, d: a ^ d
        self.assertTrue(v.equivalentes(f, f, "ABCD"))
        self.assertEqual(len(v.verificar(f, f, "ABCD")), 16)

    def test_listagem(self):
        f = lambda a, b, c: a
        g = lambda a, b, c: b
        texto = v.listagem(v.verificar(f, g, "ABC"), "ABC")
        self.assertIn("IGUAL", texto)
        self.assertIn("DIFERENTE", texto)
        self.assertIn("NÃO são equivalentes", texto)
        ok = v.listagem(v.verificar(f, f, "ABC"), "ABC")
        self.assertNotIn("DIFERENTE |", ok)
        self.assertIn("são equivalentes", ok)

    def test_arquivo_expressoes_roda(self):
        import expressoes
        self.assertIn(len(expressoes.NOMES), (3, 4))
        self.assertTrue(v.equivalentes(expressoes.original, expressoes.simplificada, expressoes.NOMES))


if __name__ == "__main__":
    unittest.main()
