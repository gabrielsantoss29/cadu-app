"""Ordenação feita do zero: Merge Sort direto na lista encadeada.

Ideia em 3 passos:
1. DIVIDIR: corta a lista ao meio (sem copiar nada, só desligando um ponteiro).
2. ORDENAR: ordena cada metade do mesmo jeito (recursão), até sobrar 0 ou 1 nó.
3. INTERCALAR: junta as duas metades já ordenadas, sempre pegando o menor
   dos dois primeiros nós e religando os ponteiros.

Por que Merge Sort?
- Em lista encadeada ele é o algoritmo mais natural: não precisa acessar
  posição por índice (que na lista custaria O(n)), só andar para frente.
- Sempre O(n log n), até no pior caso (insertion sort chega a O(n²)).
- Não cria nós novos: só troca os ponteiros `proximo`.
- É estável: em empate, mantém a ordem original.

Não usamos sorted(), list.sort() nem listas nativas.
"""

from lista_ligada import No


def merge_sort(lista, chave=None, decrescente=False):
    """Ordena a ListaLigada no próprio lugar (religando os nós).

    chave: função que extrai o valor de comparação (ex.: lambda s: s.id).
    decrescente: True para do maior para o menor.
    """
    if chave is None:
        chave = lambda x: x
    lista.cabeca = _ordenar(lista.cabeca, chave, decrescente)
    # Depois de religar, a cauda pode ter mudado: andamos até o último nó.
    atual = lista.cabeca
    while atual is not None and atual.proximo is not None:
        atual = atual.proximo
    lista.cauda = atual


def _ordenar(cabeca, chave, decrescente):
    # Caso base: 0 ou 1 nó já está ordenado.
    if cabeca is None or cabeca.proximo is None:
        return cabeca
    esquerda, direita = _dividir(cabeca)
    esquerda = _ordenar(esquerda, chave, decrescente)
    direita = _ordenar(direita, chave, decrescente)
    return _intercalar(esquerda, direita, chave, decrescente)


def _dividir(cabeca):
    """Acha o meio com dois ponteiros: o 'lento' anda 1 nó, o 'rápido' anda 2.

    Quando o rápido chega no fim, o lento está no meio. Aí cortamos a
    ligação e temos duas listas separadas.
    """
    lento = cabeca
    rapido = cabeca.proximo
    while rapido is not None and rapido.proximo is not None:
        lento = lento.proximo
        rapido = rapido.proximo.proximo
    meio = lento.proximo
    lento.proximo = None          # corta a lista em duas
    return cabeca, meio


def _intercalar(a, b, chave, decrescente):
    """Junta duas listas ordenadas. Usa um nó 'sentinela' só para facilitar
    o começo (assim não precisamos tratar a primeira ligação separada)."""
    sentinela = No(None)
    fim = sentinela
    while a is not None and b is not None:
        ka = chave(a.valor)
        kb = chave(b.valor)
        # Em empate, pega de `a` (a metade da esquerda): isso garante estabilidade.
        if decrescente:
            pegar_a = ka >= kb
        else:
            pegar_a = ka <= kb
        if pegar_a:
            fim.proximo = a
            a = a.proximo
        else:
            fim.proximo = b
            b = b.proximo
        fim = fim.proximo
    # O que sobrou de um dos lados já está ordenado: é só ligar no fim.
    fim.proximo = a if a is not None else b
    return sentinela.proximo
