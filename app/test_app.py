"""Testes do app. Rode na raiz do repositório:  app/.venv/Scripts/python -m unittest app.test_app"""
import unittest

from app.app import app, assistente


class TestApp(unittest.TestCase):
    def setUp(self):
        self.c = app.test_client()

    def test_paginas(self):
        for url in ["/", "/triagem", "/beneficios", "/energia", "/cadu", "/mais"]:
            r = self.c.get(url)
            self.assertEqual(r.status_code, 200, url)
            self.assertIn("não é canal oficial", r.get_data(as_text=True).lower(), url)

    def test_pagina_inexistente(self):
        self.assertEqual(self.c.get("/nao-existe").status_code, 404)

    def test_chat_encontra_com_fonte(self):
        d = self.c.post("/api/chat", json={"mensagem": "como funciona o gás do povo"}).get_json()
        self.assertEqual(d["tipo"], "encontrada")
        self.assertTrue(d["orientacao"]["fonte"].startswith("http"))
        self.assertTrue(d["orientacao"]["verificado_em"])

    def test_chat_recusa_dado_pessoal(self):
        for t in ["12345678909", "meu email a@b.com"]:
            d = self.c.post("/api/chat", json={"mensagem": t}).get_json()
            self.assertEqual(d["tipo"], "dado_pessoal")
            self.assertIn("aplicativo oficial", d["mensagem"])

    def test_chat_nao_encontrei(self):
        d = self.c.post("/api/chat", json={"mensagem": "como tiro passaporte"}).get_json()
        self.assertEqual(d["tipo"], "nao_encontrei")
        self.assertTrue(d["categorias"])

    def test_chat_pedido_invalido(self):
        self.assertEqual(self.c.post("/api/chat", json={"x": 1}).status_code, 400)
        self.assertEqual(self.c.post("/api/chat", json={"mensagem": 5}).status_code, 400)
        self.assertEqual(self.c.post("/api/chat", data="nada").status_code, 400)

    def test_pedido_grande_demais(self):
        self.assertEqual(self.c.post("/api/chat", json={"mensagem": "a" * 10000}).status_code, 413)

    def test_mensagem_longa(self):
        d = self.c.post("/api/chat", json={"mensagem": "a" * 500}).get_json()
        self.assertEqual(d["tipo"], "longa")

    def test_orientacao_por_codigo(self):
        d = self.c.get("/api/orientacao/gas-do-povo").get_json()
        self.assertEqual(d["orientacao"]["codigo"], "gas-do-povo")
        self.assertEqual(self.c.get("/api/orientacao/nao-existe").status_code, 404)
        self.assertEqual(self.c.get("/api/orientacao/<script>").status_code, 404)

    def test_atalhos_do_chat_existem_na_base(self):
        # Códigos usados em chat.js, inicio.html e energia.html precisam existir
        for codigo in ["bolsa-familia-bloqueio-cancelamento", "cadunico-atualizar", "bolsa-familia-calendario",
                       "golpes-cuidados", "cadunico-como-fazer", "cadunico-estou-no-cadastro",
                       "cadunico-app-oficial", "tarifa-social-energia"]:
            self.assertEqual(self.c.get(f"/api/orientacao/{codigo}").status_code, 200, codigo)

    def test_servidor_nao_guarda_historico(self):
        self.c.post("/api/chat", json={"mensagem": "gas do povo"})
        self.assertEqual(assistente.historico, [])
        self.assertIsNone(assistente.caminho_historico)

    def test_html_escapado_na_pagina(self):
        # Jinja escapa: nenhum texto da base vira tag
        html = self.c.get("/beneficios").get_data(as_text=True)
        self.assertNotIn("<script>alert", html)


if __name__ == "__main__":
    unittest.main()
