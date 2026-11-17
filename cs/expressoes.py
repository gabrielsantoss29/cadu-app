"""Regra de decisão do módulo de Computer Science (CadU).

Situação de atendimento: o assistente orienta a família sobre a ATUALIZAÇÃO DO CADASTRO ÚNICO
e diz se ela deve procurar o CRAS com prioridade.

Variáveis (1 = sim, 0 = não), na ordem da tabela-verdade (A é o bit mais significativo):
  A = já se passaram 24 meses ou mais desde a última atualização do cadastro
  B = mudou algo na família (endereço, renda ou quem mora na casa)
  C = a família recebe Bolsa Família
  D = a família recebeu aviso de convocação (revisão ou averiguação cadastral)

Saída S: 1 = procurar o CRAS com prioridade; 0 = sem urgência agora.

Regra (escolha do grupo, em cima das regras oficiais das fontes):
  S = 1 quando a família foi convocada (D), ou quando precisa atualizar (A ou B) e recebe
  Bolsa Família (C), porque o benefício pode ser bloqueado se o cadastro ficar desatualizado.

Forma canônica (produto de maxtermos): S = ΠM(0, 2, 4, 8, 12)
Expressão simplificada (álgebra e mapa de Karnaugh): S = D + A·C + B·C
"""

EXEMPLO = False

# ===== COMECE A EDITAR AQUI =====

NOMES = ["A", "B", "C", "D"]

PERGUNTAS = {
    "A": "Já faz 24 meses ou mais que o cadastro foi atualizado? (1 = sim, 0 = não)",
    "B": "Mudou algo na família: endereço, renda ou quem mora na casa? (1 = sim, 0 = não)",
    "C": "A família recebe Bolsa Família? (1 = sim, 0 = não)",
    "D": "Chegou aviso chamando a família para revisão ou averiguação do cadastro? (1 = sim, 0 = não)",
}


def original(a, b, c, d):
    """Forma canônica: produto de maxtermos, S = ΠM(0, 2, 4, 8, 12).

    M0  = A + B + C + D        (linha 0000)
    M2  = A + B + C' + D       (linha 0010)
    M4  = A + B' + C + D       (linha 0100)
    M8  = A' + B + C + D       (linha 1000)
    M12 = A' + B' + C + D      (linha 1100)
    """
    return ((a or b or c or d)
            and (a or b or (not c) or d)
            and (a or (not b) or c or d)
            and ((not a) or b or c or d)
            and ((not a) or (not b) or c or d))


def simplificada(a, b, c, d):
    """Expressão simplificada: S = D + A·C + B·C."""
    return d or (a and c) or (b and c)


ORIENTACAO = {
    1: ("Procure o CRAS ou o posto do Cadastro Único o quanto antes para atualizar o cadastro. "
        "Se chegou aviso, respeite a data-limite dele. Com o cadastro desatualizado, o benefício pode ser bloqueado."),
    0: ("Sem urgência agora. Mesmo assim, o cadastro precisa ser atualizado a cada 24 meses e sempre que algo "
        "mudar na família. Anote a data e procure o CRAS quando chegar a hora."),
}

FONTES = [
    "Ministério do Desenvolvimento e Assistência Social (MDS), Perguntas frequentes do Cadastro Único, "
    "https://www.gov.br/mds/pt-br/acoes-e-programas/cadastro-unico/perguntas-frequentes-cadastro-unico, "
    "consultado em 09/11/2026 e conferido em 16/11/2026.",
    "MDS, Tire suas dúvidas sobre o novo Cadastro Único (atualização a cada 24 meses ou quando algo mudar; "
    "Bolsa Família pode ser convocado a partir de 18 meses), "
    "https://www.gov.br/mds/pt-br/noticias-e-conteudos/Noticias/2025/tire-suas-duvidas-sobre-o-novo-cadastro-unico, "
    "consultado em 09/11/2026 e conferido em 16/11/2026.",
]

# ===== TERMINE DE EDITAR AQUI =====
