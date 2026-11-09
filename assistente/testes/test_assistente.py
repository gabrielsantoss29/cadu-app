"""Testes automáticos. Rode na raiz do repositório: py -3.12 -m unittest discover -s assistente/testes -t ."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

from assistente import (ALTA, FORA_ESCOPO, MEDIA, RECUSADA, SEM_RESPOSTA,
                        Assistente, BaseConhecimento, ErroBase, Orientacao)

RAIZ = Path(__file__).resolve().parents[2]
EXEMPLO = RAIZ / "dados" / "base_exemplo.json"


def nova_orientacao(**extra):
    d = dict(id="x", titulo="Bolsa Família", categoria="Benefícios",
             palavras_chave=["bolsa familia", "bolsa", "renda"], resposta="r",
             fonte_nome="f", fonte_url="https://exemplo.gov.br", data_verificacao="2026-11-09")
    d.update(extra)
    return Orientacao.de_dicionario(d)


class TestPontuacao(unittest.TestCase):
    def test_palavra_chave_vale_3(self):
        o = nova_orientacao(titulo="Algum assunto", palavras_chave=["renda", "a", "b"])
        self.assertEqual(o.pontuar("minha renda"), 3)

    def test_titulo_vale_1_so_com_4_letras(self):
        o = nova_orientacao(titulo="O que é Bolsa", palavras_chave=["zzz", "yyy", "xxx"])
        self.assertEqual(o.pontuar("o que e bolsa"), 1)   # só "bolsa" (4+ letras)

    def test_ignora_acento_e_maiuscula(self):
        o = nova_orientacao(titulo="x", palavras_chave=["família", "b", "c"])
        self.assertEqual(o.pontuar("FAMILIA"), 3)

    def test_aceita_plural(self):
        o = nova_orientacao(titulo="x", palavras_chave=["beneficio", "b", "c"])
        self.assertEqual(o.pontuar("quais beneficios"), 3)


class TestBase(unittest.TestCase):
    def test_carrega_exemplo(self):
        base = BaseConhecimento.carregar(EXEMPLO)
        self.assertTrue(base.eh_exemplo)
        self.assertGreaterEqual(len(base.orientacoes), 4)

    def test_arquivo_inexistente(self):
        with self.assertRaises(ErroBase):
            BaseConhecimento.carregar(RAIZ / "nao_existe.json")

    def test_campo_faltando(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "b.json"
            p.write_text(json.dumps({"orientacoes": [{"id": "a"}]}), encoding="utf-8")
            with self.assertRaises(ErroBase):
                BaseConhecimento.carregar(p)

    def test_exemplo_nao_passa_na_qualidade(self):
        # O exemplo é pequeno de propósito: precisa apontar problemas.
        self.assertTrue(BaseConhecimento.carregar(EXEMPLO).conferir_qualidade())


class TestAssistente(unittest.TestCase):
    def setUp(self):
        self.a = Assistente(BaseConhecimento.carregar(EXEMPLO))

    def test_alta(self):
        r = self.a.responder("Como funciona o Bolsa Família?")
        self.assertEqual(r.nivel, ALTA)
        self.assertTrue(r.fonte_url.startswith("https://"))
        self.assertTrue(r.data_verificacao)

    def test_media(self):
        r = self.a.responder("quero saber do bolsa")  # só palavra-chave simples: 3+1
        self.assertEqual(r.nivel, MEDIA)

    def test_sem_resposta_indica_121_e_cras(self):
        r = self.a.responder("como tiro passaporte")
        self.assertEqual(r.nivel, SEM_RESPOSTA)
        self.assertIn("121", r.texto)
        self.assertIn("CRAS", r.texto)
        self.assertEqual(r.fonte_url, "")      # nunca inventa fonte

    def test_fora_do_escopo(self):
        r = self.a.responder("me conta uma piada de futebol")
        self.assertEqual(r.nivel, FORA_ESCOPO)
        self.assertIn("só ajudo", r.texto)

    def test_recusa_cpf_e_nao_registra(self):
        r = self.a.responder("meu cpf é 123.456.789-09")
        self.assertEqual(r.nivel, RECUSADA)
        self.assertEqual(self.a.historico, [])
        self.assertEqual(self.a.indicadores()["total"], 0)
        self.assertEqual(self.a.indicadores()["recusadas"], 1)

    def test_recusa_email(self):
        self.assertEqual(self.a.responder("joao@email.com").nivel, RECUSADA)

    def test_7_digitos_passa(self):
        self.assertNotEqual(self.a.responder("bolsa 1234567").nivel, RECUSADA)

    def test_limite_de_tamanho(self):
        r = self.a.responder("a" * 301)
        self.assertEqual(r.nivel, RECUSADA)
        self.assertEqual(self.a.historico, [])

    def test_vazio(self):
        self.assertEqual(self.a.responder("   ").nivel, RECUSADA)

    def test_indicadores(self):
        self.a.responder("Como funciona o Bolsa Família?")
        self.a.responder("como tiro passaporte")
        self.a.responder("qualquer piada")
        ind = self.a.indicadores()
        self.assertEqual(ind["total"], 3)
        self.assertEqual(ind["por_nivel"][ALTA], 1)
        self.assertEqual(ind["por_nivel"][SEM_RESPOSTA], 1)
        self.assertEqual(ind["por_nivel"][FORA_ESCOPO], 1)
        self.assertEqual(ind["por_categoria"], {"Benefícios": 1})

    def test_sem_guardar_texto(self):
        a = Assistente(BaseConhecimento.carregar(EXEMPLO), guardar_texto=False)
        a.responder("Como funciona o Bolsa Família?")
        self.assertEqual(a.historico, [])
        self.assertEqual(a.indicadores()["total"], 1)

    def test_exportar_csv(self):
        self.a.responder("=2+2 bolsa familia")
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "h.csv"
            self.assertEqual(self.a.exportar_csv(p), 1)
            with open(p, encoding="utf-8-sig", newline="") as f:
                linhas = list(csv.reader(f, delimiter=";"))
        self.assertEqual(len(linhas), 2)                 # cabeçalho + 1
        self.assertTrue(linhas[1][1].startswith("'="))   # fórmula neutralizada


if __name__ == "__main__":
    unittest.main()
