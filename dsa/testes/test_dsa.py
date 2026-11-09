"""Testes da entrega de DSA. Rode na raiz do repositório:

    py -3.12 -m unittest discover -s dsa/testes -v
"""

import os
import random
import sys
import unittest

# Deixa os testes enxergarem os módulos da pasta dsa/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from crud import RepositorioOrientacoes
from lista_ligada import HistoricoPerguntas, ListaLigada
from ordenacao import merge_sort


class TestListaLigada(unittest.TestCase):
    def test_vazia(self):
        l = ListaLigada()
        self.assertTrue(l.esta_vazia())
        self.assertEqual(len(l), 0)
        with self.assertRaises(IndexError):
            l.remover_inicio()
        with self.assertRaises(IndexError):
            l.remover_fim()

    def test_adicionar_inicio_e_fim(self):
        l = ListaLigada()
        l.adicionar_fim(2)
        l.adicionar_fim(3)
        l.adicionar_inicio(1)
        self.assertEqual(list(l), [1, 2, 3])
        self.assertEqual(len(l), 3)

    def test_remover_inicio_e_fim(self):
        l = ListaLigada()
        for x in [1, 2, 3]:
            l.adicionar_fim(x)
        self.assertEqual(l.remover_inicio(), 1)
        self.assertEqual(l.remover_fim(), 3)
        self.assertEqual(list(l), [2])
        self.assertEqual(l.remover_fim(), 2)
        self.assertTrue(l.esta_vazia())
        l.adicionar_fim(7)           # cauda deve estar consistente após esvaziar
        self.assertEqual(list(l), [7])

    def test_remover_se_meio_cabeca_cauda(self):
        l = ListaLigada()
        for x in [1, 2, 3, 4]:
            l.adicionar_fim(x)
        self.assertEqual(l.remover_se(lambda v: v == 2), 2)   # meio
        self.assertEqual(l.remover_se(lambda v: v == 1), 1)   # cabeça
        self.assertEqual(l.remover_se(lambda v: v == 4), 4)   # cauda
        self.assertIsNone(l.remover_se(lambda v: v == 99))
        self.assertEqual(list(l), [3])
        l.adicionar_fim(5)           # a cauda foi atualizada corretamente
        self.assertEqual(list(l), [3, 5])

    def test_buscar_e_substituir(self):
        l = ListaLigada()
        for x in [10, 20, 30]:
            l.adicionar_fim(x)
        self.assertEqual(l.buscar(lambda v: v > 15), 20)
        self.assertIsNone(l.buscar(lambda v: v > 100))
        self.assertTrue(l.substituir_se(lambda v: v == 20, 25))
        self.assertFalse(l.substituir_se(lambda v: v == 99, 0))
        self.assertEqual(list(l), [10, 25, 30])


class TestHistorico(unittest.TestCase):
    def test_guarda_so_as_ultimas(self):
        h = HistoricoPerguntas(capacidade=3)
        for p in ["a", "b", "c", "d", "e"]:
            h.registrar(p)
        self.assertEqual(h.recentes(), ["e", "d", "c"])
        self.assertEqual(len(h), 3)

    def test_capacidade_invalida(self):
        with self.assertRaises(ValueError):
            HistoricoPerguntas(0)


class TestOrdenacao(unittest.TestCase):
    def test_casos_basicos(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([1]), [1])
        self.assertEqual(merge_sort([3, 1, 2]), [1, 2, 3])
        self.assertEqual(merge_sort([3, 1, 2], decrescente=True), [3, 2, 1])
        self.assertEqual(merge_sort([2, 2, 1, 1]), [1, 1, 2, 2])

    def test_nao_altera_original(self):
        original = [3, 1, 2]
        merge_sort(original)
        self.assertEqual(original, [3, 1, 2])

    def test_estavel(self):
        # Mesma chave (1) deve manter a ordem original: "a" antes de "b".
        itens = [(1, "a"), (0, "x"), (1, "b"), (0, "y")]
        r = merge_sort(itens, chave=lambda p: p[0])
        self.assertEqual(r, [(0, "x"), (0, "y"), (1, "a"), (1, "b")])
        r = merge_sort(itens, chave=lambda p: p[0], decrescente=True)
        self.assertEqual(r, [(1, "a"), (1, "b"), (0, "x"), (0, "y")])

    def test_aleatorio_confere_com_sorted(self):
        # Aqui (e só nos testes) usamos sorted() para conferir a resposta.
        random.seed(42)
        for _ in range(200):
            dados = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
            self.assertEqual(merge_sort(dados), sorted(dados))
            self.assertEqual(merge_sort(dados, decrescente=True), sorted(dados, reverse=True))


class TestCrud(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioOrientacoes()
        self.repo.criar(1, "Como fazer o Cadastro Único", "cadastro", ["cadunico", "inscrição"])
        self.repo.criar(2, "Prazo para atualizar o cadastro", "cadastro", ["atualizar", "prazo", "cadunico"])
        self.repo.criar(3, "Tarifa Social de Energia", "energia", ["luz", "desconto"])

    def test_criar_e_listar(self):
        self.assertEqual([o.id for o in self.repo.listar()], [1, 2, 3])

    def test_criar_id_repetido_ou_titulo_vazio(self):
        with self.assertRaises(ValueError):
            self.repo.criar(1, "outra", "x", [])
        with self.assertRaises(ValueError):
            self.repo.criar(9, "   ", "x", [])

    def test_buscar(self):
        self.assertEqual(self.repo.buscar_por_id(3).titulo, "Tarifa Social de Energia")
        self.assertIsNone(self.repo.buscar_por_id(99))
        self.assertEqual(len(self.repo.buscar_por_categoria("CADASTRO")), 2)

    def test_atualizar(self):
        self.repo.atualizar(3, titulo="Novo título", palavras_chave=["Luz"])
        o = self.repo.buscar_por_id(3)
        self.assertEqual(o.titulo, "Novo título")
        self.assertEqual(o.palavras_chave, ["luz"])
        self.assertEqual(o.categoria, "energia")          # não mexeu no que não foi pedido
        self.assertIsNone(self.repo.atualizar(99, titulo="x"))

    def test_remover(self):
        self.assertTrue(self.repo.remover(2))
        self.assertFalse(self.repo.remover(2))
        self.assertEqual([o.id for o in self.repo.listar()], [1, 3])
        self.assertEqual(len(self.repo), 2)

    def test_ranquear(self):
        r = self.repo.ranquear("Qual o PRAZO para atualizar o CadÚnico?")
        self.assertEqual(r[0][1].id, 2)                   # ignora acento e maiúscula
        pontos = [p for p, _ in r]
        self.assertEqual(pontos, sorted(pontos, reverse=True))
        self.assertEqual(self.repo.ranquear("assunto sem relação"), [])
        self.assertEqual(len(self.repo.ranquear("cadastro", limite=1)), 1)


if __name__ == "__main__":
    unittest.main()
