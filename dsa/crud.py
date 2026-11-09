"""CRUD de orientações, guardadas numa lista ligada própria.

Uma "orientação" é um item da base do CadU: id, título, categoria e
palavras-chave. Este módulo é independente do assistente: depois basta
carregar os dados do JSON e chamar `ranquear(pergunta)`.
"""

import unicodedata

from lista_ligada import ListaLigada
from ordenacao import merge_sort


def normalizar(texto):
    """Minúsculas e sem acento, para 'Benefício' casar com 'beneficio'."""
    decomposto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


class Orientacao:
    def __init__(self, id, titulo, categoria, palavras_chave):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.palavras_chave = [normalizar(p) for p in palavras_chave]

    def __repr__(self):
        return f"Orientacao(id={self.id}, titulo={self.titulo!r}, categoria={self.categoria!r})"


class RepositorioOrientacoes:
    def __init__(self):
        self._lista = ListaLigada()

    # ---------- Create ----------
    def criar(self, id, titulo, categoria, palavras_chave):
        """Cria e guarda uma orientação. O(n): confere se o id já existe.

        Erro (ValueError) se o id for repetido ou o título vazio.
        """
        if not titulo or not titulo.strip():
            raise ValueError("título não pode ser vazio")
        if self.buscar_por_id(id) is not None:
            raise ValueError(f"já existe orientação com id {id}")
        nova = Orientacao(id, titulo, categoria, palavras_chave)
        self._lista.adicionar_fim(nova)   # O(1) graças à cauda
        return nova

    # ---------- Read ----------
    def listar(self):
        """Todas as orientações, na ordem de inserção. O(n)."""
        return [o for o in self._lista]

    def buscar_por_id(self, id):
        """Devolve a orientação com esse id, ou None. O(n)."""
        return self._lista.buscar(lambda o: o.id == id)

    def buscar_por_categoria(self, categoria):
        """Todas de uma categoria. O(n)."""
        alvo = normalizar(categoria)
        return [o for o in self._lista if normalizar(o.categoria) == alvo]

    # ---------- Update ----------
    def atualizar(self, id, titulo=None, categoria=None, palavras_chave=None):
        """Muda só os campos informados. Devolve a orientação, ou None se não existe. O(n)."""
        o = self.buscar_por_id(id)
        if o is None:
            return None
        if titulo is not None:
            if not titulo.strip():
                raise ValueError("título não pode ser vazio")
            o.titulo = titulo
        if categoria is not None:
            o.categoria = categoria
        if palavras_chave is not None:
            o.palavras_chave = [normalizar(p) for p in palavras_chave]
        return o

    # ---------- Delete ----------
    def remover(self, id):
        """Remove pelo id. True se removeu, False se não existia. O(n)."""
        return self._lista.remover_se(lambda o: o.id == id) is not None

    def __len__(self):
        return len(self._lista)

    # ---------- Ranqueamento ----------
    def pontuar(self, orientacao, pergunta):
        """Pontuação simples: cada palavra da pergunta vale 2 se estiver nas
        palavras-chave e 1 se estiver só no título. Sem acento/maiúscula."""
        palavras = normalizar(pergunta).split()
        titulo = normalizar(orientacao.titulo).split()
        pontos = 0
        for p in palavras:
            if p in orientacao.palavras_chave:
                pontos += 2
            elif p in titulo:
                pontos += 1
        return pontos

    def ranquear(self, pergunta, limite=3):
        """Devolve até `limite` pares (pontuacao, orientacao), do maior para o menor.

        Ignora quem tem 0 pontos. Custo: O(n·p) para pontuar + O(n log n) para ordenar.
        """
        pontuadas = []
        for o in self._lista:
            pts = self.pontuar(o, pergunta)
            if pts > 0:
                pontuadas.append((pts, o))
        ordenadas = merge_sort(pontuadas, chave=lambda par: par[0], decrescente=True)
        return ordenadas[:limite]
