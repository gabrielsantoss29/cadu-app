"""Ordenação feita do zero: Merge Sort (ordenação por intercalação).

Por que Merge Sort?
- Fácil de explicar: "divide ao meio, ordena cada metade, junta as duas".
- Sempre O(n log n), mesmo no pior caso (o insertion sort chega a O(n²)).
- É estável: itens com a mesma pontuação mantêm a ordem original.
  Isso é bom no ranking, porque empates não ficam embaralhados.

Não usamos sorted() nem list.sort().
"""


def merge_sort(itens, chave=None, decrescente=False):
    """Devolve uma lista NOVA ordenada. A original não é alterada.

    chave: função que extrai o valor de comparação de cada item
           (ex.: lambda o: o.pontuacao). Se None, compara o próprio item.
    decrescente: True para do maior para o menor.
    """
    if chave is None:
        chave = lambda x: x
    copia = [x for x in itens]      # copia manual, para não mexer na original
    return _dividir(copia, chave, decrescente)


def _dividir(itens, chave, decrescente):
    # Caso base: 0 ou 1 item já está ordenado.
    if len(itens) <= 1:
        return itens
    meio = len(itens) // 2
    esquerda = _dividir(itens[:meio], chave, decrescente)
    direita = _dividir(itens[meio:], chave, decrescente)
    return _intercalar(esquerda, direita, chave, decrescente)


def _intercalar(esq, dir_, chave, decrescente):
    """Junta duas listas JÁ ordenadas em uma só, olhando só o início de cada."""
    resultado = []
    i = 0
    j = 0
    while i < len(esq) and j < len(dir_):
        a = chave(esq[i])
        b = chave(dir_[j])
        # Em empate, pegamos da esquerda primeiro: é isso que garante estabilidade.
        if decrescente:
            pegar_esquerda = a >= b
        else:
            pegar_esquerda = a <= b
        if pegar_esquerda:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir_[j])
            j += 1
    # Sobrou algo em um dos lados: já está ordenado, é só copiar.
    while i < len(esq):
        resultado.append(esq[i])
        i += 1
    while j < len(dir_):
        resultado.append(dir_[j])
        j += 1
    return resultado
