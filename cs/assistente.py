"""Programa do assistente: o usuário informa as entradas e vê a orientação.

A decisão usa a expressão SIMPLIFICADA de `expressoes.py`.
"""
import expressoes

AVISO = (
    "AVISO: este é um protótipo acadêmico. Não é um canal oficial e não "
    "confirma a concessão de serviços ou direitos.\n"
    "Limitações: a orientação depende só das respostas dadas e das regras "
    "das fontes listadas; confira sempre no canal oficial.\n"
    "Nenhum dado pessoal é pedido nem guardado: responda apenas 1 ou 0."
)

SAIR = ("sair", "q")


class Saiu(Exception):
    """O usuário digitou 'sair'."""


def interpretar(texto):
    """Converte a resposta em 0 ou 1. Retorna None se for inválida."""
    t = texto.strip().lower()
    if t in ("1", "sim", "s"):
        return 1
    if t in ("0", "nao", "não", "n"):
        return 0
    return None


def ler_bit(pergunta, entrada=input, saida=print):
    """Pergunta até receber uma resposta válida."""
    while True:
        texto = entrada(pergunta + " ")
        if texto.strip().lower() in SAIR:
            raise Saiu
        valor = interpretar(texto)
        if valor is not None:
            return valor
        saida("Resposta inválida. Digite 1 (sim) ou 0 (não), ou 'sair'.")


def decidir(*valores):
    """Resultado executado pelo programa (usa a expressão simplificada)."""
    if len(valores) != len(expressoes.NOMES):
        raise ValueError(f"esperado {len(expressoes.NOMES)} valores")
    if any(v not in (0, 1) for v in valores):
        raise ValueError("os valores devem ser 0 ou 1")
    return int(bool(expressoes.simplificada(*valores)))


def orientacao(*valores):
    return expressoes.ORIENTACAO[decidir(*valores)]


def rodar(entrada=input, saida=print):
    saida(AVISO)
    if expressoes.EXEMPLO:
        saida("*** ATENÇÃO: usando regra de EXEMPLO, não a do trabalho ***")
    saida("Fontes: " + "; ".join(expressoes.FONTES))
    try:
        while True:
            saida("")
            valores = [ler_bit(expressoes.PERGUNTAS[n], entrada, saida)
                       for n in expressoes.NOMES]
            entradas = ", ".join(f"{n}={v}" for n, v in zip(expressoes.NOMES, valores))
            saida(f"Entradas: {entradas} -> saída {decidir(*valores)}")
            saida("Orientação: " + orientacao(*valores))
            if ler_bit("Fazer outra consulta? (1 = sim, 0 = não)", entrada, saida) == 0:
                break
    except (Saiu, EOFError, KeyboardInterrupt):
        pass
    saida("Até mais!")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    rodar()
