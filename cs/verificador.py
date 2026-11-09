"""Verificador de equivalência.

Testa todas as 2^n combinações das variáveis e confere se a regra
original, a expressão simplificada e o resultado executado pelo programa
(`assistente.decidir`) dão o mesmo valor em todas elas.
"""
from itertools import product


def combinacoes(n):
    """Todas as combinações de n bits, em ordem crescente (00..0 até 11..1)."""
    if n not in (3, 4):
        raise ValueError("use 3 ou 4 variáveis")
    return list(product((0, 1), repeat=n))


def verificar(nomes, *funcoes):
    """Avalia cada função em todas as combinações.

    Retorna uma lista de tuplas (valores, [resultado de cada função]).
    """
    if len(funcoes) < 2:
        raise ValueError("passe pelo menos duas funções")
    return [(v, [int(bool(f(*v))) for f in funcoes]) for v in combinacoes(len(nomes))]


def equivalentes(nomes, *funcoes):
    return all(len(set(r)) == 1 for _, r in verificar(nomes, *funcoes))


def listagem(linhas, nomes, titulos):
    """Monta o texto da listagem e do resumo final."""
    cab = (" ".join(f"{n:>2}" for n in nomes) + " | "
           + " | ".join(titulos) + " | situação")
    saida = [cab, "-" * len(cab)]
    diferentes = []
    for i, (valores, res) in enumerate(linhas):
        igual = len(set(res)) == 1
        if not igual:
            diferentes.append(i)
        vs = " ".join(f"{v:>2}" for v in valores)
        cols = " | ".join(f"{r:^{len(t)}}" for r, t in zip(res, titulos))
        saida.append(f"{vs} | {cols} | {'IGUAL' if igual else 'DIFERENTE'}")
    total = len(linhas)
    saida += ["",
              f"Combinações testadas: {total}",
              f"Iguais: {total - len(diferentes)}",
              f"Diferentes: {len(diferentes)}"]
    if diferentes:
        saida.append("Linhas diferentes: " + ", ".join(str(i) for i in diferentes))
        saida.append("RESULTADO: as representações NÃO são equivalentes.")
    else:
        saida.append("RESULTADO: as representações são equivalentes.")
    return "\n".join(saida)


def main():
    import assistente
    import expressoes

    funcoes = (expressoes.original, expressoes.simplificada, assistente.decidir)
    titulos = ["original", "simplificada", "executado"]
    if expressoes.EXEMPLO:
        print("*** ATENÇÃO: usando regra de EXEMPLO, não a do trabalho ***\n")
    print(listagem(verificar(expressoes.NOMES, *funcoes), expressoes.NOMES, titulos))
    return 0 if equivalentes(expressoes.NOMES, *funcoes) else 1


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
