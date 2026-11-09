"""Aqui o Gabriel coloca as expressões dele.

Como preencher:
  1. Troque NOMES pelos nomes das suas variáveis (3 ou 4), na ordem usada
     na tabela-verdade.
  2. Reescreva as funções `original` e `simplificada` com as suas expressões.
     Use: `and`, `or`, `not`. Cada argumento vale 0 ou 1.
  3. Mude EXEMPLO para False.

Tudo abaixo é só EXEMPLO (não é a regra do trabalho).
"""

EXEMPLO = True  # <-- mude para False quando colocar as suas expressões

# ===== COMECE A EDITAR AQUI =====

NOMES = ["A", "B", "C"]  # EXEMPLO: troque pelas suas variáveis


def original(a, b, c):
    # EXEMPLO: troque pela sua expressão original/canônica
    return (a and b) or (a and not b)


def simplificada(a, b, c):
    # EXEMPLO: troque pela sua expressão simplificada
    return a

# ===== TERMINE DE EDITAR AQUI =====
