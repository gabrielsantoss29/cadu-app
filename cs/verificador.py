"""Verificador de expressões booleanas.

Testa todas as 2^n combinações das variáveis e confere se a expressão
original e a simplificada dão o mesmo resultado em todas elas.
"""
from itertools import product


def combinacoes(n):
    """Todas as combinações de n bits, em ordem crescente (00..0 até 11..1)."""
    if n not in (3, 4):
        raise ValueError("use 3 ou 4 variáveis")
    return list(product((0, 1), repeat=n))


def verificar(original, simplificada, nomes):
    """Compara as duas funções em todas as combinações.

    Retorna uma lista de tuplas (valores, res_original, res_simplificada).
    """
    resultado = []
    for valores in combinacoes(len(nomes)):
        a = int(bool(original(*valores)))
        b = int(bool(simplificada(*valores)))
        resultado.append((valores, a, b))
    return resultado


def listagem(linhas, nomes):
    """Monta o texto da listagem e do resumo final."""
    cab = " ".join(f"{n:>2}" for n in nomes) + " | original | simplificada | situação"
    saida = [cab, "-" * len(cab)]
    diferentes = 0
    for valores, a, b in linhas:
        igual = a == b
        if not igual:
            diferentes += 1
        vs = " ".join(f"{v:>2}" for v in valores)
        saida.append(f"{vs} | {a:^8} | {b:^12} | {'IGUAL' if igual else 'DIFERENTE'}")
    total = len(linhas)
    saida.append("")
    saida.append(f"Combinações testadas: {total}")
    saida.append(f"Iguais: {total - diferentes}")
    saida.append(f"Diferentes: {diferentes}")
    if diferentes == 0:
        saida.append("RESULTADO: as expressões são equivalentes.")
    else:
        saida.append("RESULTADO: as expressões NÃO são equivalentes.")
    return "\n".join(saida)


def equivalentes(original, simplificada, nomes):
    return all(a == b for _, a, b in verificar(original, simplificada, nomes))


if __name__ == "__main__":
    import sys
    import expressoes

    sys.stdout.reconfigure(encoding="utf-8")

    linhas = verificar(expressoes.original, expressoes.simplificada, expressoes.NOMES)
    if expressoes.EXEMPLO:
        print("*** ATENÇÃO: usando expressões de EXEMPLO, não as do trabalho ***\n")
    print(listagem(linhas, expressoes.NOMES))
