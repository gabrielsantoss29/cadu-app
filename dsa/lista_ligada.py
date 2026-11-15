"""Lista ligada simples, feita do zero (sem usar `list` para guardar os dados).

Ideia: cada elemento fica dentro de um "nó". O nó guarda o valor e aponta
para o próximo nó. A lista só conhece o primeiro nó (a "cabeça").

    cabeça -> [A | ->] -> [B | ->] -> [C | None]

Para chegar no item C, é preciso passar por A e B. Por isso buscar é O(n).
"""


class No:
    """Um elemento da lista: guarda um valor e o próximo nó."""

    def __init__(self, valor, proximo=None):
        self.valor = valor
        self.proximo = proximo


class ListaLigada:
    """Lista ligada com cabeça e cauda (a cauda deixa inserir no fim em O(1))."""

    def __init__(self):
        self.cabeca = None   # primeiro nó
        self.cauda = None    # último nó
        self._tamanho = 0    # contador, para len() ser O(1)

    # ---------- inserção ----------

    def adicionar_inicio(self, valor):
        """Põe o valor na frente da lista. O(1): só troca a cabeça."""
        self.cabeca = No(valor, self.cabeca)
        if self.cauda is None:       # lista estava vazia
            self.cauda = self.cabeca
        self._tamanho += 1

    def adicionar_fim(self, valor):
        """Põe o valor no fim da lista. O(1): usamos a cauda, sem percorrer."""
        novo = No(valor)
        if self.cauda is None:       # lista vazia
            self.cabeca = novo
        else:
            self.cauda.proximo = novo
        self.cauda = novo
        self._tamanho += 1

    # ---------- remoção ----------

    def remover_inicio(self):
        """Tira e devolve o primeiro valor. O(1). Erro se a lista estiver vazia."""
        if self.cabeca is None:
            raise IndexError("lista vazia")
        valor = self.cabeca.valor
        self.cabeca = self.cabeca.proximo
        if self.cabeca is None:      # ficou vazia
            self.cauda = None
        self._tamanho -= 1
        return valor

    def remover_fim(self):
        """Tira e devolve o último valor. O(n): precisa achar o penúltimo nó."""
        if self.cabeca is None:
            raise IndexError("lista vazia")
        if self.cabeca is self.cauda:    # só um elemento
            return self.remover_inicio()
        atual = self.cabeca
        while atual.proximo is not self.cauda:
            atual = atual.proximo
        valor = self.cauda.valor
        atual.proximo = None
        self.cauda = atual
        self._tamanho -= 1
        return valor

    def remover_se(self, condicao):
        """Remove o primeiro item para o qual condicao(valor) é verdadeira.

        Devolve o valor removido, ou None se nada bateu. O(n).
        Usamos dois ponteiros: `anterior` e `atual`. Para "pular" o nó
        removido, o anterior passa a apontar para o seguinte.
        """
        anterior = None
        atual = self.cabeca
        while atual is not None:
            if condicao(atual.valor):
                if anterior is None:             # removendo a cabeça
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual is self.cauda:          # removendo a cauda
                    self.cauda = anterior
                self._tamanho -= 1
                return atual.valor
            anterior = atual
            atual = atual.proximo
        return None

    # ---------- consulta ----------

    def buscar(self, condicao):
        """Devolve o primeiro valor com condicao(valor) verdadeira, ou None. O(n)."""
        atual = self.cabeca
        while atual is not None:
            if condicao(atual.valor):
                return atual.valor
            atual = atual.proximo
        return None

    def substituir_se(self, condicao, novo_valor):
        """Troca o primeiro valor que bate com a condição. True se trocou. O(n)."""
        atual = self.cabeca
        while atual is not None:
            if condicao(atual.valor):
                atual.valor = novo_valor
                return True
            atual = atual.proximo
        return False

    def esta_vazia(self):
        return self._tamanho == 0

    def limpar(self):
        self.cabeca = None
        self.cauda = None
        self._tamanho = 0

    # ---------- Python "entende" a lista ----------

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        """Permite usar `for item in lista`. Percorre do começo ao fim."""
        atual = self.cabeca
        while atual is not None:
            yield atual.valor
            atual = atual.proximo

    def __repr__(self):
        return "ListaLigada([" + ", ".join(repr(v) for v in self) + "])"


class HistoricoPerguntas:
    """Guarda as últimas N perguntas do usuário (a mais recente primeiro).

    Usa a ListaLigada: a pergunta nova entra na frente (O(1)) e, se passar
    da capacidade, a mais antiga (a do fim) sai.
    """

    def __init__(self, capacidade=10):
        if capacidade < 1:
            raise ValueError("capacidade deve ser pelo menos 1")
        self.capacidade = capacidade
        self._lista = ListaLigada()

    def registrar(self, pergunta):
        """Registra uma pergunta nova. O(n) só quando precisa descartar a mais antiga."""
        self._lista.adicionar_inicio(pergunta)
        if len(self._lista) > self.capacidade:
            self._lista.remover_fim()

    def recentes(self):
        """Percorre as perguntas da mais recente para a mais antiga. O(n)."""
        return iter(self._lista)

    def limpar(self):
        self._lista.limpar()

    def __len__(self):
        return len(self._lista)
