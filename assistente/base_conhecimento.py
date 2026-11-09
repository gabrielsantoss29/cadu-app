"""Classe BaseConhecimento: carrega e guarda as orientações do JSON."""
import json
from pathlib import Path

from .orientacao import Orientacao


class ErroBase(Exception):
    """Problema ao ler a base (arquivo ausente, JSON quebrado, campo faltando)."""


class BaseConhecimento:
    def __init__(self, orientacoes: list[Orientacao], meta: dict | None = None):
        self.orientacoes = orientacoes
        self.meta = meta or {}          # versao, exemplo, etc.

    @classmethod
    def carregar(cls, caminho: str | Path) -> "BaseConhecimento":
        caminho = Path(caminho)
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise ErroBase(f"Arquivo não encontrado: {caminho}")
        except json.JSONDecodeError as e:
            raise ErroBase(f"JSON inválido em {caminho}: {e}")
        if not isinstance(dados.get("orientacoes"), list):
            raise ErroBase("O JSON precisa ter a lista 'orientacoes'.")
        try:
            itens = [Orientacao.de_dicionario(o) for o in dados["orientacoes"]]
        except ValueError as e:
            raise ErroBase(str(e))
        ids = [o.id for o in itens]
        if len(ids) != len(set(ids)):
            raise ErroBase("Há ids repetidos na base.")
        meta = {k: v for k, v in dados.items() if k != "orientacoes"}
        return cls(itens, meta)

    @property
    def eh_exemplo(self) -> bool:
        return bool(self.meta.get("exemplo"))

    def categorias(self) -> list[str]:
        return sorted({o.categoria for o in self.orientacoes})

    def buscar_por_id(self, id_: str) -> Orientacao | None:
        return next((o for o in self.orientacoes if o.id == id_), None)

    def melhor(self, mensagem: str) -> tuple[Orientacao | None, int]:
        """Devolve a orientação com mais pontos (empate: a primeira do arquivo)."""
        melhor, melhor_pontos = None, 0
        for o in self.orientacoes:
            p = o.pontuar(mensagem)
            if p > melhor_pontos:
                melhor, melhor_pontos = o, p
        return melhor, melhor_pontos

    def conferir_qualidade(self) -> list[str]:
        """Exigências da entrega (10+ orientações, 3+ categorias, 3+ palavras-chave).
        Devolve a lista de problemas; vazia = base pronta."""
        problemas = []
        if len(self.orientacoes) < 10:
            problemas.append(f"só {len(self.orientacoes)} orientações (mínimo 10)")
        if len(self.categorias()) < 3:
            problemas.append(f"só {len(self.categorias())} categorias (mínimo 3)")
        for o in self.orientacoes:
            if len(o.palavras_chave) < 3:
                problemas.append(f"'{o.id}' tem menos de 3 palavras-chave")
            if not o.fonte_url.startswith("https://"):
                problemas.append(f"'{o.id}' com fonte_url sem https")
        return problemas
