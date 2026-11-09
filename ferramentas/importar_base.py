"""Converte o rascunho da pesquisa (dados/rascunho/beneficios.json) para o formato
do enunciado do PCP (assistente/data/base_conhecimento.json).

Rode na raiz do repositório:  py -3.12 ferramentas/importar_base.py

- Fichas com status "nao_verificado" ficam de fora (é proibido inventar).
- "conferido_por_humano" é copiado como está: só o Gabriel muda para true.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "dados" / "rascunho" / "beneficios.json"
DESTINO = RAIZ / "assistente" / "data" / "base_conhecimento.json"

# Nome da categoria que aparece para a pessoa
CATEGORIAS = {
    "cadastro-unico": "Cadastro Único",
    "cotidiano": "Ajuda e cuidados",
    "bolsa-familia": "Bolsa Família",
    "educacao": "Educação",
    "energia": "Energia",
    "bpc": "BPC",
    "gas": "Gás",
    "outros-beneficios": "Outros benefícios",
}

SEM_CONTEUDO = ("não se aplica", "nao se aplica", "")


def limpar(texto):
    texto = (texto or "").strip()
    return "" if texto.lower() in SEM_CONTEUDO else texto


def converter(entradas):
    titulos = {e["id"]: e["titulo"] for e in entradas}
    base = []
    for e in entradas:
        if e.get("status_verificacao") == "nao_verificado":
            continue
        docs = limpar(e.get("documentos"))
        # "Ver a ficha 'x'" vira o título da outra orientação
        for codigo, titulo in titulos.items():
            docs = docs.replace(f"a ficha '{codigo}'", f"a orientação \"{titulo}\"")
        base.append({
            "id": len(base) + 1,
            "codigo": e["id"],
            "categoria": CATEGORIAS.get(e["categoria"], e["categoria"]),
            "titulo": e["titulo"],
            "palavras_chave": e["palavras_chave"],
            "resposta": e["resumo_simples"],
            "documentos": [docs] if docs else [],
            "onde": e.get("onde_ir", ""),
            "fonte": e["fonte_url"],
            "verificado_em": e["verificado_em"],
            "fonte_nome": e.get("fonte_nome", ""),
            "quem_pode": limpar(e.get("quem_pode")),
            "como_pedir": limpar(e.get("como_pedir")),
            "renovacao": limpar(e.get("renovacao")),
            "se_acabar_ou_bloquear": limpar(e.get("se_acabar_ou_bloquear")),
            "status_verificacao": e.get("status_verificacao", ""),
            "conferido_por_humano": bool(e.get("conferido_por_humano", False)),
        })
        if e.get("pode_combinar"):          # lista de códigos, se a pesquisa trouxer
            base[-1]["pode_combinar"] = e["pode_combinar"]
    return base


def main():
    dados = json.loads(ORIGEM.read_text(encoding="utf-8"))
    base = converter(dados["entradas"])
    DESTINO.parent.mkdir(exist_ok=True)
    DESTINO.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    puladas = len(dados["entradas"]) - len(base)
    print(f"{len(base)} orientações gravadas em {DESTINO.relative_to(RAIZ)} ({puladas} não verificadas ficaram de fora).")


if __name__ == "__main__":
    main()
