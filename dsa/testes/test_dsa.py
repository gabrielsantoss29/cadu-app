"""Testes automáticos da entrega de DSA. Rode na raiz do repositório:

    py -3.12 -m unittest discover -s dsa/testes -v
"""

import os
import random
import sys
import unittest

# Deixa os testes enxergarem os módulos da pasta dsa/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import dados_exemplo
from crud import RepositorioServicos
from lista_ligada import HistoricoPerguntas, ListaLigada
from ordenacao import merge_sort


def lista_de(*valores):
    l = ListaLigada()
    for v in valores:
        l.adicionar_fim(v)
    return l


def ids(registros):
    return [s.id for s in registros]


class TestListaLigada(unittest.TestCase):
    def test_vazia(self):
        l = ListaLigada()
        self.assertTrue(l.esta_vazia())
        self.assertEqual(len(l), 0)
        self.assertEqual(list(l), [])
        self.assertIsNone(l.buscar(lambda v: True))
        self.assertIsNone(l.remover_se(lambda v: True))
        with self.assertRaises(IndexError):
            l.remover_inicio()
        with self.assertRaises(IndexError):
            l.remover_fim()

    def test_adicionar_inicio_e_fim(self):
        l = lista_de(2, 3)
        l.adicionar_inicio(1)
        self.assertEqual(list(l), [1, 2, 3])
        self.assertEqual(len(l), 3)

    def test_remover_inicio_e_fim(self):
        l = lista_de(1, 2, 3)
        self.assertEqual(l.remover_inicio(), 1)
        self.assertEqual(l.remover_fim(), 3)
        self.assertEqual(l.remover_fim(), 2)
        self.assertTrue(l.esta_vazia())
        l.adicionar_fim(7)           # cauda consistente após esvaziar
        self.assertEqual(list(l), [7])

    def test_remover_se_meio_cabeca_cauda(self):
        l = lista_de(1, 2, 3, 4)
        self.assertEqual(l.remover_se(lambda v: v == 2), 2)   # meio
        self.assertEqual(l.remover_se(lambda v: v == 1), 1)   # cabeça
        self.assertEqual(l.remover_se(lambda v: v == 4), 4)   # cauda
        self.assertIsNone(l.remover_se(lambda v: v == 99))
        self.assertEqual(list(l), [3])
        l.adicionar_fim(5)           # a cauda foi ajustada corretamente
        self.assertEqual(list(l), [3, 5])

    def test_buscar_e_substituir(self):
        l = lista_de(10, 20, 30)
        self.assertEqual(l.buscar(lambda v: v > 15), 20)
        self.assertTrue(l.substituir_se(lambda v: v == 20, 25))
        self.assertFalse(l.substituir_se(lambda v: v == 99, 0))
        self.assertEqual(list(l), [10, 25, 30])


class TestMergeSort(unittest.TestCase):
    def test_casos_basicos(self):
        for entrada, esperado in [((), []), ((1,), [1]), ((3, 1, 2), [1, 2, 3]),
                                  ((2, 2, 1, 1), [1, 1, 2, 2])]:
            l = lista_de(*entrada)
            merge_sort(l)
            self.assertEqual(list(l), esperado)
        l = lista_de(3, 1, 2)
        merge_sort(l, decrescente=True)
        self.assertEqual(list(l), [3, 2, 1])

    def test_cauda_e_tamanho_apos_ordenar(self):
        l = lista_de(3, 1, 2)
        merge_sort(l)
        l.adicionar_fim(0)           # se a cauda estivesse errada, o 0 se perderia
        self.assertEqual(list(l), [1, 2, 3, 0])
        self.assertEqual(len(l), 4)

    def test_estavel(self):
        l = lista_de((1, "a"), (0, "x"), (1, "b"), (0, "y"))
        merge_sort(l, chave=lambda p: p[0])
        self.assertEqual(list(l), [(0, "x"), (0, "y"), (1, "a"), (1, "b")])

    def test_aleatorio_confere_com_sorted(self):
        # sorted() aparece SÓ aqui, para conferir a resposta do nosso algoritmo.
        random.seed(42)
        for _ in range(200):
            dados = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
            l = lista_de(*dados)
            merge_sort(l)
            self.assertEqual(list(l), sorted(dados))


class TestHistorico(unittest.TestCase):
    def test_guarda_so_as_ultimas(self):
        h = HistoricoPerguntas(capacidade=3)
        for p in "abcde":
            h.registrar(p)
        self.assertEqual(list(h.recentes()), ["e", "d", "c"])

    def test_capacidade_invalida(self):
        with self.assertRaises(ValueError):
            HistoricoPerguntas(0)


class TestRepositorioVazio(unittest.TestCase):
    """Operações sobre lista vazia (exigido pelo enunciado)."""

    def test_operacoes_em_lista_vazia(self):
        repo = RepositorioServicos()
        self.assertEqual(len(repo), 0)
        self.assertEqual(ids(repo.listar()), [])
        self.assertIsNone(repo.consultar(1))
        self.assertIsNone(repo.atualizar(1, titulo="x"))
        self.assertFalse(repo.excluir(1))
        self.assertEqual(len(repo.pesquisar("titulo", "rg")), 0)
        repo.ordenar("titulo")                       # não pode quebrar
        self.assertEqual(ids(repo.listar()), [])


class TestRepositorio(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioServicos()
        dados_exemplo.carregar(self.repo)            # ids na ordem 3, 1, 5, 2, 4

    def test_cadastrar_e_listar(self):
        self.assertEqual(ids(self.repo.listar()), [3, 1, 5, 2, 4])
        self.repo.cadastrar("6", "Tarifa Social", "energia", "Desconto na conta de luz",
                            "Famílias do CadÚnico", "Distribuidora de energia")
        self.assertEqual(ids(self.repo.listar()), [3, 1, 5, 2, 4, 6])

    def test_cadastro_invalido(self):
        validos = ("Título", "cat", "desc", "público", "canal")
        with self.assertRaisesRegex(ValueError, "já existe"):
            self.repo.cadastrar(1, *validos)
        for id_ruim in ("abc", "", "0", "-3", "2.5", None):
            with self.assertRaisesRegex(ValueError, "inteiro positivo"):
                self.repo.cadastrar(id_ruim, *validos)
        with self.assertRaisesRegex(ValueError, "título é obrigatório"):
            self.repo.cadastrar(9, "   ", "cat", "desc", "público", "canal")
        with self.assertRaisesRegex(ValueError, "canal de atendimento é obrigatório"):
            self.repo.cadastrar(9, "T", "cat", "desc", "público", "")
        self.assertEqual(len(self.repo), 5)          # nada inválido entrou

    def test_consultar(self):
        self.assertEqual(self.repo.consultar(5).categoria, "saúde")
        self.assertEqual(self.repo.consultar("5").id, 5)
        self.assertIsNone(self.repo.consultar(99))
        with self.assertRaises(ValueError):
            self.repo.consultar("xyz")

    def test_atualizar(self):
        self.repo.atualizar(5, titulo="Campanha de vacinação", canal=None)
        s = self.repo.consultar(5)
        self.assertEqual(s.titulo, "Campanha de vacinação")
        self.assertEqual(s.canal, "Unidade Básica de Saúde (UBS)")   # mantido
        with self.assertRaisesRegex(ValueError, "obrigatório"):
            self.repo.atualizar(5, titulo="ok", descricao="  ")
        self.assertEqual(self.repo.consultar(5).titulo, "Campanha de vacinação")  # nada mudou

    def test_excluir_cabeca_meio_cauda(self):
        self.assertTrue(self.repo.excluir(3))     # cabeça
        self.assertTrue(self.repo.excluir(5))     # meio
        self.assertTrue(self.repo.excluir(4))     # cauda
        self.assertFalse(self.repo.excluir(4))
        self.assertEqual(ids(self.repo.listar()), [1, 2])
        self.repo.cadastrar(7, "T", "c", "d", "p", "x")   # cauda continua certa
        self.assertEqual(ids(self.repo.listar()), [1, 2, 7])

    def test_pesquisar(self):
        self.assertEqual(ids(self.repo.pesquisar("categoria", "ASSISTENCIA")), [3, 4])
        self.assertEqual(ids(self.repo.pesquisar("titulo", "cadunico")), [4])
        self.assertEqual(ids(self.repo.pesquisar("titulo", "inexistente")), [])
        with self.assertRaises(ValueError):
            self.repo.pesquisar("titulo", " ")
        with self.assertRaises(ValueError):
            self.repo.pesquisar("canal", "cras")

    def test_ordenar(self):
        self.repo.ordenar("id")
        self.assertEqual(ids(self.repo.listar()), [1, 2, 3, 4, 5])
        self.repo.ordenar("titulo")
        titulos = [s.titulo for s in self.repo.listar()]
        self.assertEqual(titulos[0], "Atualização cadastral do CadÚnico")
        self.assertEqual(titulos[-1], "Vacinação de rotina")
        with self.assertRaises(ValueError):
            self.repo.ordenar("categoria")

    def test_ranquear(self):
        r = list(self.repo.ranquear("Qual o PRAZO para atualizar o CadÚnico?"))
        self.assertEqual(r[0][1].id, 4)
        pontos = [p for p, _ in r]
        self.assertEqual(pontos, sorted(pontos, reverse=True))
        self.assertEqual(len(self.repo.ranquear("cadunico", limite=1)), 1)
        self.assertEqual(len(self.repo.ranquear("nada a ver")), 0)


if __name__ == "__main__":
    unittest.main()
