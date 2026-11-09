"""Registros fictícios para testar o sistema (opção 8 do menu)."""

EXEMPLOS = (
    (3, "Inscrição no Cadastro Único", "assistência social",
     "Como se inscrever no CadÚnico para acessar programas sociais.",
     "Famílias com renda de até meio salário mínimo por pessoa",
     "CRAS do município", ("cadunico", "inscricao", "cras")),
    (1, "Emissão da Carteira de Identidade", "documentos",
     "Primeira via e segunda via do RG com o número do CPF.",
     "Qualquer cidadão", "Poupatempo ou posto de identificação", ("rg", "identidade", "documento")),
    (5, "Vacinação de rotina", "saúde",
     "Calendário de vacinas gratuitas para todas as idades.",
     "Crianças, adultos e idosos", "Unidade Básica de Saúde (UBS)", ("vacina", "ubs", "saude")),
    (2, "Matrícula na rede pública", "educação",
     "Como pedir vaga em escola estadual ou municipal.",
     "Estudantes de 4 a 17 anos", "Secretaria de Educação ou site da matrícula",
     ("matricula", "escola", "vaga")),
    (4, "Atualização cadastral do CadÚnico", "assistência social",
     "O cadastro deve ser atualizado a cada 2 anos ou quando a família mudar.",
     "Famílias já inscritas no CadÚnico", "CRAS do município", ("atualizar", "prazo", "cadunico")),
)


def carregar(repo):
    """Cadastra os exemplos que ainda não existem. Devolve quantos entraram."""
    novos = 0
    for registro in EXEMPLOS:
        if repo.consultar(registro[0]) is None:
            repo.cadastrar(*registro)
            novos += 1
    return novos
