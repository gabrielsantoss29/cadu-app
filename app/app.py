"""App web do CadU (Flask).

Roda local:   app/.venv/Scripts/python app/app.py     (abre em http://127.0.0.1:5000)
Na Vercel:    a Vercel procura a variável `app` neste arquivo.

Regras do projeto que este arquivo respeita:
- NÃO escreve em disco (a Vercel não deixa): o assistente roda sem caminho de histórico.
- NÃO pede nem guarda dado pessoal; as respostas da triagem ficam só no aparelho (localStorage).
- O assistente é o MESMO código de assistente/ usado no terminal (sem duplicar).
"""
import json
import os
import re
import sys
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

RAIZ = Path(__file__).resolve().parent.parent
# Deixa a pasta assistente/ visível para importar as classes do terminal.
sys.path.insert(0, str(RAIZ / "assistente"))

from assistente import Assistente  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
import contadores  # noqa: E402
from base_conhecimento import BaseConhecimento  # noqa: E402

CAMINHO_BASE = os.environ.get("CADU_BASE", str(RAIZ / "assistente" / "data" / "base_conhecimento.json"))
CAMINHO_POSTOS = RAIZ / "dados" / "cras_sp.json"
CAMINHO_CONFIG_ENERGIA = RAIZ / "energia" / "config_app.json"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024   # pedidos de até 4 KB bastam para o chat

base = BaseConhecimento(CAMINHO_BASE)
if not base.carregar():
    raise RuntimeError(f"Base de conhecimento com problema: {base.erro}")
# Sem caminho_historico: o servidor não grava o que as pessoas digitam.
assistente = Assistente("CadU", base)
# Módulo de energia (SERS): aparelhos, hipóteses, fontes e os cálculos vêm de energia/
sys.path.insert(0, str(RAIZ / "energia"))
from calculo_energia import calcular_consumo_mensal, carregar_energia, comparar_banho  # noqa: E402
from integracao_cadu import responder_energia  # noqa: E402

energia_sers = carregar_energia()
energia = json.loads(CAMINHO_CONFIG_ENERGIA.read_text(encoding="utf-8"))
energia["aparelhos"] = [dict(a, icone=energia["icones"].get(a["id"], "🔌")) for a in energia_sers["aparelhos"]]
energia["comparacao"] = energia_sers["comparacao_exemplo"]
energia["orientacoes"] = energia_sers["orientacoes"]
energia["referencias"] = energia_sers["referencias"]
energia["data_verificacao"] = energia_sers["data_verificacao"]
postos = json.loads(CAMINHO_POSTOS.read_text(encoding="utf-8"))

# Abas do menu: (endereço, nome, ícone, chave da aba)
ABAS = [
    ("/", "Início", "casa", "inicio"),
    ("/beneficios", "Benefícios", "presente", "beneficios"),
    ("/energia", "Energia", "raio", "energia"),
    ("/cadu", "CadU", "conversa", "cadu"),
    ("/mais", "Mais", "mais", "mais"),
]
RASCUNHO = any(not o.conferido_por_humano for o in base.orientacoes)


@app.context_processor
def contexto_comum():
    # O Jinja escapa HTML sozinho em tudo que vai para as páginas (autoescape).
    return {"abas": ABAS, "base_rascunho": RASCUNHO}


@app.after_request
def cabecalhos(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["X-Frame-Options"] = "DENY"
    if request.path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"
    return resp


# ---------- páginas ----------
@app.get("/")
def inicio():
    return render_template("inicio.html", aba="inicio")


@app.get("/triagem")
def triagem():
    return render_template("triagem.html", aba="triagem")


@app.get("/beneficios")
def beneficios():
    grupos = [(c, base.por_categoria(c)) for c in base.categorias()]
    titulos = {o.codigo: o.titulo for o in base.orientacoes}
    return render_template("beneficios.html", aba="beneficios", grupos=grupos, titulos=titulos)


@app.get("/energia")
def pagina_energia():
    return render_template("energia.html", aba="energia", energia=energia)


@app.get("/cadu")
def cadu():
    return render_template("cadu.html", aba="cadu")


@app.get("/mapa")
def mapa():
    return render_template("mapa.html", aba="mais", postos=postos["itens"],
                           fonte=postos["fonte"], baixado_em=postos["baixado_em"])


@app.get("/mais")
def mais():
    return render_template("mais.html", aba="mais")


# ---------- API ----------
def resposta_json(r: dict) -> dict:
    """Converte o resultado de Assistente.analisar() em algo que vira JSON."""
    saida = {"tipo": r["tipo"], "mensagem": r.get("mensagem", "")}
    if r["tipo"] == "encontrada":
        saida.update(confianca=r["confianca"], pontos=r["pontos"],
                     orientacao=r["orientacao"].para_dict(),
                     alternativas=[{"codigo": o.codigo, "titulo": o.titulo} for o in r["alternativas"]])
    elif r["tipo"] == "nao_encontrei":
        saida["categorias"] = r["categorias"]
    elif r["tipo"] == "dado_pessoal":
        saida["mensagem"] += (" Se você quer consultar seu cadastro pelo CPF, use o aplicativo "
                              "oficial do Cadastro Único, o 121 ou o CRAS.")
    return saida


@app.post("/api/chat")
def api_chat():
    """Recebe {"mensagem": "..."} e devolve a resposta do assistente em JSON."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not isinstance(dados.get("mensagem"), str):
        return jsonify(erro="Envie {\"mensagem\": \"texto\"}."), 400
    return jsonify(resposta_json(assistente.analisar(dados["mensagem"])))


@app.get("/api/orientacao/<codigo>")
def api_orientacao(codigo):
    """Busca uma orientação pelo código (usado pelos atalhos do chat)."""
    if not re.fullmatch(r"[a-z0-9-]{1,60}", codigo):
        abort(404)
    for o in base.orientacoes:
        if o.codigo == codigo:
            return jsonify(tipo="encontrada", confianca="ALTA", pontos=None,
                           orientacao=o.para_dict(), alternativas=[])
    return jsonify(erro="Orientação não encontrada."), 404


EVENTOS_FIXOS = {"triagem_concluida", "ajudou_sim", "ajudou_nao"}


@app.post("/api/contar")
def api_contar():
    """Conta um evento anônimo. Só aceita nomes de uma lista fixa; nunca guarda texto livre."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return "", 400
    evento, valor = dados.get("evento"), dados.get("valor")
    if evento in EVENTOS_FIXOS:
        chave = evento
    elif evento == "assunto" and valor in base.categorias():
        chave = "assunto:" + valor
    elif evento == "beneficio" and any(o.codigo == valor for o in base.orientacoes):
        chave = "beneficio:" + valor
    else:
        return "", 400
    contadores.somar(chave)
    return "", 204


@app.get("/api/contadores")
def api_contadores():
    """Totais anônimos (só números). Vazio quando não há banco ligado."""
    return jsonify(ativo=contadores.ativo(), totais=contadores.totais())


def _numero(dados, campo, minimo, maximo, padrao=None):
    """Lê um número do JSON do pedido. Devolve None se estiver fora da faixa."""
    v = dados.get(campo, padrao)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not (minimo <= v <= maximo):
        return None
    return float(v)


@app.post("/api/energia/comparar")
def api_energia_comparar():
    """Compara banho mais curto e aquecimento solar (módulo SERS). Não guarda nada."""
    d = request.get_json(silent=True)
    if not isinstance(d, dict):
        return jsonify(erro="Envie os números do chuveiro."), 400
    c = energia["comparacao"]
    potencia = _numero(d, "potencia_w", 0, 20000, c["chuveiro_potencia_w"])
    minutos = _numero(d, "minutos_dia", 1, 1440, round(c["horas_banho_total_dia_base"] * 60))
    minutos_novo = _numero(d, "minutos_dia_reduzido", 0, 1440, round(c["horas_banho_total_dia_reduzido"] * 60))
    dias = _numero(d, "dias_mes", 1, 31, c["dias_mes"])
    solar = _numero(d, "fracao_solar", 0, 1, c["fracao_substituida_solar"])
    tarifa = _numero(d, "tarifa_kwh", 0, 10) if d.get("tarifa_kwh") is not None else None
    if None in (potencia, minutos, minutos_novo, dias, solar) or (d.get("tarifa_kwh") is not None and tarifa is None):
        return jsonify(erro="Confira os números: algum está fora do possível."), 400
    try:
        r = comparar_banho(potencia, minutos / 60, minutos_novo / 60, int(dias), solar, tarifa_r_kwh=tarifa)
    except ValueError as e:
        return jsonify(erro=str(e)), 400
    return jsonify(r)


@app.get("/api/saude")
def api_saude():
    return jsonify(ok=True, orientacoes=len(base.orientacoes), rascunho=RASCUNHO)


@app.errorhandler(413)
def grande_demais(_):
    return jsonify(erro="Mensagem grande demais."), 413


@app.errorhandler(404)
def nao_achou(_):
    if request.path.startswith("/api/"):
        return jsonify(erro="Não encontrado."), 404
    return render_template("404.html", aba=""), 404


if __name__ == "__main__":
    app.run(debug=True)
