"""Aqui o Gabriel coloca a regra dele.

Como preencher (só entre os marcadores COMECE/TERMINE):
  1. NOMES: nomes das variáveis (3 ou 4), na mesma ordem da tabela-verdade.
  2. PERGUNTAS: a pergunta que o assistente faz para cada variável,
     dizendo o que significa 1 e o que significa 0.
  3. original: a regra original (por exemplo, a forma canônica).
  4. simplificada: a expressão simplificada.
     Use `and`, `or`, `not`. Cada argumento vale 0 ou 1.
  5. ORIENTACAO: o texto mostrado ao cidadão quando a saída é 1 e quando é 0.
  6. FONTES: fontes verificáveis das regras, com data de consulta.
  7. Mude EXEMPLO para False.

Tudo abaixo é só EXEMPLO (não é a regra do trabalho).
"""

EXEMPLO = True  # <-- mude para False quando colocar a sua regra

# ===== COMECE A EDITAR AQUI =====

NOMES = ["A", "B", "C"]  # EXEMPLO

PERGUNTAS = {  # EXEMPLO
    "A": "Exemplo A? (1 = sim, 0 = não)",
    "B": "Exemplo B? (1 = sim, 0 = não)",
    "C": "Exemplo C? (1 = sim, 0 = não)",
}


def original(a, b, c):
    # EXEMPLO: troque pela sua regra original/canônica
    return (a and b) or (a and not b)


def simplificada(a, b, c):
    # EXEMPLO: troque pela sua expressão simplificada
    return a


ORIENTACAO = {  # EXEMPLO
    1: "Exemplo de orientação quando a saída é 1.",
    0: "Exemplo de orientação quando a saída é 0.",
}

FONTES = [  # EXEMPLO
    "Exemplo: nome da fonte, endereço, consultado em DD/MM/AAAA.",
]

# ===== TERMINE DE EDITAR AQUI =====
