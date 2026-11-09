"""App web do CadU (Flask).

Roda local:   py -3.12 app/app.py        (abre em http://127.0.0.1:5000)
Na Vercel:    a Vercel procura a variável `app` neste arquivo.

Regras do projeto que este arquivo respeita:
- NÃO escreve em disco (a Vercel não deixa); o assistente roda com guardar_texto=False.
- NÃO pede nem guarda dado pessoal; as respostas da triagem ficam só no aparelho (localStorage).
- O assistente é o MESMO pacote `assistente/` usado no terminal (sem código duplicado).
"""
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# Deixa a raiz do repositório visível para importar `assistente`.
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from assistente import Assistente, BaseConhecimento  # noqa: E402


def achar_base() -> Path:
    """Variável CADU_BASE > dados/base.json > dados/base_exemplo.json."""
    if os.environ.get("CADU_BASE"):
        return Path(os.environ["CADU_BASE"])
    real = RAIZ / "dados" / "base.json"
    return real if real.exists() else RAIZ / "dados" / "base_exemplo.json"


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024   # pedidos de até 4 KB bastam para o chat

base = BaseConhecimento.carregar(achar_base())
# guardar_texto=False: o servidor não guarda o que as pessoas digitam.
assistente = Assistente(base, guardar_texto=False)

# Abas do menu: (endereço, nome, ícone, chave usada para marcar a aba ativa)
ABAS = [
    ("/", "Início", "🏠", "inicio"),
    ("/beneficios", "Benefícios", "🎁", "beneficios"),
    ("/energia", "Energia", "💡", "energia"),
    ("/cadu", "CadU", "💬", "cadu"),
    ("/mais", "Mais", "➕", "mais"),
]


@app.context_processor
def contexto_comum():
    # O Jinja já escapa HTML em tudo que vai para as páginas (autoescape).
    return {"abas": ABAS, "base_exemplo": base.eh_exemplo}


@app.after_request
def cabecalhos(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    if request.path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"
    return resp


# ---------- páginas ----------
@app.get("/")
def inicio():
    return render_template("inicio.html", aba="inicio")


@app.get("/beneficios")
def beneficios():
    return render_template("beneficios.html", aba="beneficios", orientacoes=base.orientacoes)


@app.get("/energia")
def energia():
    return render_template("energia.html", aba="energia")


@app.get("/cadu")
def cadu():
    return render_template("cadu.html", aba="cadu")


@app.get("/mais")
def mais():
    return render_template("mais.html", aba="mais")


# ---------- API ----------
@app.post("/api/chat")
def api_chat():
    """Recebe {"mensagem": "..."} e devolve a resposta do assistente em JSON."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not isinstance(dados.get("mensagem"), str):
        return jsonify(erro="Envie {\"mensagem\": \"texto\"}."), 400
    return jsonify(assistente.responder(dados["mensagem"]).para_dict())


@app.get("/api/saude")
def api_saude():
    return jsonify(ok=True, orientacoes=len(base.orientacoes), exemplo=base.eh_exemplo)


@app.errorhandler(413)
def grande_demais(_):
    return jsonify(erro="Mensagem grande demais."), 413


if __name__ == "__main__":
    app.run(debug=True)
