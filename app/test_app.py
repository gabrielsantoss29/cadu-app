"""Testes do app. Rode: app/.venv/Scripts/python -m unittest app.test_app   (na raiz do repositório)"""
import unittest

from app.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.c = app.test_client()

    def test_paginas(self):
        for url in ["/", "/beneficios", "/energia", "/cadu", "/mais"]:
            self.assertEqual(self.c.get(url).status_code, 200, url)

    def test_chat_responde_com_fonte(self):
        r = self.c.post("/api/chat", json={"mensagem": "como funciona o bolsa familia"})
        d = r.get_json()
        self.assertEqual(d["nivel"], "ALTA")
        self.assertTrue(d["fonte_url"].startswith("https://"))

    def test_chat_recusa_cpf(self):
        d = self.c.post("/api/chat", json={"mensagem": "12345678909"}).get_json()
        self.assertEqual(d["nivel"], "RECUSADA")

    def test_chat_pedido_invalido(self):
        self.assertEqual(self.c.post("/api/chat", json={"x": 1}).status_code, 400)
        self.assertEqual(self.c.post("/api/chat", json={"mensagem": 5}).status_code, 400)

    def test_pedido_grande_demais(self):
        self.assertEqual(self.c.post("/api/chat", json={"mensagem": "a" * 10000}).status_code, 413)

    def test_nao_guarda_texto(self):
        from app.app import assistente
        self.c.post("/api/chat", json={"mensagem": "bolsa familia"})
        self.assertEqual(assistente.historico, [])

    def test_html_escapado_nas_paginas(self):
        # A API devolve texto puro; quem escapa é o JS (textContent) e o Jinja nas páginas.
        d = self.c.post("/api/chat", json={"mensagem": "<script>alert(1)</script>"}).get_json()
        self.assertNotIn("<script>", d["texto"])


if __name__ == "__main__":
    unittest.main()
