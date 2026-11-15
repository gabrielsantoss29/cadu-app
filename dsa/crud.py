"""CRUD de serviços e orientações ao cidadão, guardados numa lista encadeada própria.

Cada registro (classe Servico) tem os campos mínimos do enunciado:
id, título, categoria, descrição, público-alvo e canal de atendimento,
mais palavras-chave (opcional), usadas no ranqueamento do assistente.

Este módulo não faz input/print: só regras e dados. Quem conversa com o
usuário é o menu.py. Erros de validação viram ValueError com mensagem clara.
"""

import unicodedata

from lista_ligada import ListaLigada
from ordenacao import merge_sort

CAMPOS_OBRIGATORIOS = ("titulo", "categoria", "descricao", "publico_alvo", "canal")

NOMES_CAMPOS = {
    "titulo": "título",
    "categoria": "categoria",
    "descricao": "descrição",
    "publico_alvo": "público-alvo",
    "canal": "canal de atendimento",
}


def normalizar(texto):
    """Minúsculas e sem acento, para 'Saúde' casar com 'saude'."""
    decomposto = unicodedata.normalize("NFD", str(texto).lower())
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def validar_id(valor):
    """Converte o id para inteiro positivo. Aceita int ou texto ('12')."""
    if isinstance(valor, bool):
        raise ValueError("o identificador deve ser um número inteiro positivo")
    try:
        numero = int(str(valor).strip())
    except ValueError:
        raise ValueError("o identificador deve ser um número inteiro positivo") from None
    if numero <= 0:
        raise ValueError("o identificador deve ser um número inteiro positivo")
    return numero


def validar_texto(nome_campo, valor):
    """Campo obrigatório: não pode ser vazio nem só espaços."""
    if valor is None or not str(valor).strip():
        raise ValueError(f"o campo {NOMES_CAMPOS[nome_campo]} é obrigatório")
    return str(valor).strip()


class Servico:
    """Um serviço ou orientação ao cidadão (o 'registro')."""

    def __init__(self, id, titulo, categoria, descricao, publico_alvo, canal, palavras_chave=None):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.publico_alvo = publico_alvo
        self.canal = canal
        self.palavras_chave = palavras_chave or ()

    def resumo(self):
        return f"[{self.id}] {self.titulo} ({self.categoria})"

    def detalhes(self):
        return (
            f"ID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Categoria: {self.categoria}\n"
            f"Descrição: {self.descricao}\n"
            f"Público-alvo: {self.publico_alvo}\n"
            f"Canal de atendimento: {self.canal}"
        )

    def __repr__(self):
        return f"Servico(id={self.id}, titulo={self.titulo!r})"


class RepositorioServicos:
    def __init__(self):
        self._lista = ListaLigada()     # estrutura principal de armazenamento

    def __len__(self):
        return len(self._lista)

    # ---------- Create ----------
    def cadastrar(self, id, titulo, categoria, descricao, publico_alvo, canal, palavras_chave=None):
        """Valida e insere no fim da lista. O(n): precisa conferir id duplicado."""
        id = validar_id(id)
        dados = {}
        valores = (titulo, categoria, descricao, publico_alvo, canal)
        for campo, valor in zip(CAMPOS_OBRIGATORIOS, valores):
            dados[campo] = validar_texto(campo, valor)
        if self.consultar(id) is not None:
            raise ValueError(f"já existe um registro com o identificador {id}")
        chaves = tuple(normalizar(p) for p in (palavras_chave or ()) if str(p).strip())
        novo = Servico(id, palavras_chave=chaves, **dados)
        self._lista.adicionar_fim(novo)     # O(1), graças à cauda
        return novo

    # ---------- Read ----------
    def listar(self):
        """Percorre todos os registros na ordem atual da lista. O(n)."""
        return iter(self._lista)

    def consultar(self, id):
        """Busca linear pelo id. Devolve o registro ou None. O(n)."""
        id = validar_id(id)
        return self._lista.buscar(lambda s: s.id == id)

    def pesquisar(self, campo, termo):
        """Pesquisa por 'titulo' ou 'categoria' (trecho do texto, sem acento).

        Devolve uma NOVA ListaLigada só com os registros encontrados. O(n).
        """
        if campo not in ("titulo", "categoria"):
            raise ValueError("pesquisa disponível apenas por título ou categoria")
        if termo is None or not str(termo).strip():
            raise ValueError("o termo de pesquisa é obrigatório")
        termo = normalizar(termo.strip())
        resultado = ListaLigada()
        for s in self._lista:                       # busca linear: olha todos
            if termo in normalizar(getattr(s, campo)):
                resultado.adicionar_fim(s)
        return resultado

    # ---------- Update ----------
    def atualizar(self, id, **novos):
        """Atualiza só os campos informados (valores None são ignorados).

        Devolve o registro atualizado, ou None se o id não existe. O(n).
        Valida tudo ANTES de mudar, para não deixar o registro pela metade.
        """
        s = self.consultar(id)
        if s is None:
            return None
        validados = {}
        for campo, valor in novos.items():
            if valor is None:
                continue
            if campo not in CAMPOS_OBRIGATORIOS:
                raise ValueError(f"campo desconhecido: {campo}")
            validados[campo] = validar_texto(campo, valor)
        for campo, valor in validados.items():
            setattr(s, campo, valor)
        return s

    # ---------- Delete ----------
    def excluir(self, id):
        """Remove pelo id religando o nó anterior ao seguinte. O(n).

        True se removeu, False se não existia.
        """
        id = validar_id(id)
        return self._lista.remover_se(lambda s: s.id == id) is not None

    # ---------- Ordenação ----------
    def ordenar(self, criterio):
        """Ordena a própria lista por 'id' ou 'titulo' (merge sort). O(n log n)."""
        if criterio == "id":
            merge_sort(self._lista, chave=lambda s: s.id)
        elif criterio == "titulo":
            merge_sort(self._lista, chave=lambda s: normalizar(s.titulo))
        else:
            raise ValueError("ordenação disponível apenas por id ou título")

    # ---------- Ranqueamento (para o assistente, extra) ----------
    def pontuar(self, servico, pergunta):
        """Cada palavra da pergunta vale 2 se está nas palavras-chave e 1 se
        está só no título (sem acento/maiúscula)."""
        titulo = normalizar(servico.titulo).split()
        pontos = 0
        for p in normalizar(pergunta).split():
            if p in servico.palavras_chave:
                pontos += 2
            elif p in titulo:
                pontos += 1
        return pontos

    def ranquear(self, pergunta, limite=3):
        """ListaLigada com até `limite` pares (pontos, servico), do maior para o menor.

        O(n·p) para pontuar (p = palavras da pergunta) + O(n log n) para ordenar.
        """
        pontuados = ListaLigada()
        for s in self._lista:
            pts = self.pontuar(s, pergunta)
            if pts > 0:
                pontuados.adicionar_fim((pts, s))
        merge_sort(pontuados, chave=lambda par: par[0], decrescente=True)
        melhores = ListaLigada()
        for par in pontuados:              # copia só os `limite` primeiros
            if len(melhores) == limite:
                break
            melhores.adicionar_fim(par)
        return melhores
