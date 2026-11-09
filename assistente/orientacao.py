"""Classe Orientacao: um item da base de conhecimento (um assunto explicado)."""
from dataclasses import dataclass, field

from .texto import palavras

# Campos que TODA orientação precisa ter no JSON.
CAMPOS_OBRIGATORIOS = (
    "id", "titulo", "categoria", "palavras_chave", "resposta",
    "fonte_nome", "fonte_url", "data_verificacao",
)


@dataclass
class Orientacao:
    id: str
    titulo: str
    categoria: str
    palavras_chave: list[str]
    resposta: str
    fonte_nome: str
    fonte_url: str
    data_verificacao: str              # formato AAAA-MM-DD
    passos: list[str] = field(default_factory=list)   # "o que fazer", opcional
    prazo: str = ""                    # texto livre, opcional

    @classmethod
    def de_dicionario(cls, d: dict) -> "Orientacao":
        """Cria a partir de um dict do JSON, conferindo os campos."""
        faltando = [c for c in CAMPOS_OBRIGATORIOS if not d.get(c)]
        if faltando:
            raise ValueError(f"orientação '{d.get('id', '?')}' sem: {', '.join(faltando)}")
        if not isinstance(d["palavras_chave"], list):
            raise ValueError(f"orientação '{d['id']}': palavras_chave deve ser lista")
        return cls(
            id=d["id"], titulo=d["titulo"], categoria=d["categoria"],
            palavras_chave=list(d["palavras_chave"]), resposta=d["resposta"],
            fonte_nome=d["fonte_nome"], fonte_url=d["fonte_url"],
            data_verificacao=d["data_verificacao"],
            passos=list(d.get("passos", [])), prazo=d.get("prazo", ""),
        )

    def palavras_do_titulo(self) -> list[str]:
        """Palavras do título com 4+ letras (valem +1 ponto cada)."""
        return [p for p in palavras(self.titulo) if len(p) >= 4]

    def pontuar(self, mensagem: str) -> int:
        """Regra de pontos: +3 por palavra-chave achada, +1 por palavra do título."""
        tokens = palavras(mensagem)
        conjunto = set(tokens)
        texto = " " + " ".join(tokens) + " "
        pontos = 0
        for kw in self.palavras_chave:
            kw_n = " ".join(palavras(kw))
            if not kw_n:
                continue
            if " " in kw_n:                      # frase: procura inteira
                achou = f" {kw_n} " in texto
            else:                                # palavra: aceita plural simples
                achou = kw_n in conjunto or kw_n + "s" in conjunto or kw_n + "es" in conjunto
            if achou:
                pontos += 3
        for p in set(self.palavras_do_titulo()):
            if p in conjunto:
                pontos += 1
        return pontos
