"""Menu interativo do sistema. Rode na raiz do repositório:  py -3.12 dsa/main.py"""

import sys

import dados_exemplo
from crud import CAMPOS_OBRIGATORIOS, NOMES_CAMPOS, RepositorioServicos, validar_id

MENU = """
===== CadU - Serviços e Orientações =====
1 - Cadastrar registro
2 - Listar todos
3 - Consultar por ID
4 - Atualizar registro
5 - Excluir registro
6 - Pesquisar por título ou categoria
7 - Ordenar por ID ou título
8 - Carregar dados de exemplo
0 - Sair"""


def ler(mensagem):
    """input() que também mostra o valor digitado quando a entrada vem de um
    arquivo (útil para gerar as evidências). Fim da entrada vira '0' (sair)."""
    try:
        valor = input(mensagem)
    except EOFError:
        print()
        return "0"
    if not sys.stdin.isatty():
        print(valor)
    return valor


def mostrar_lista(registros):
    vazio = True
    for s in registros:
        print("  " + s.resumo())
        vazio = False
    if vazio:
        print("Nenhum registro encontrado.")


def cadastrar(repo):
    # Valida o ID logo de cara, para não pedir os outros campos à toa.
    id = validar_id(ler("ID (número inteiro): "))
    if repo.consultar(id) is not None:
        raise ValueError(f"já existe um registro com o identificador {id}")
    valores = {}
    for campo in CAMPOS_OBRIGATORIOS:
        valores[campo] = ler(NOMES_CAMPOS[campo].capitalize() + ": ")
    chaves = ler("Palavras-chave separadas por vírgula (opcional): ")
    novo = repo.cadastrar(id, palavras_chave=chaves.split(","), **valores)
    print("Registro cadastrado: " + novo.resumo())


def listar(repo):
    print(f"Total: {len(repo)} registro(s)")
    mostrar_lista(repo.listar())


def consultar(repo):
    s = repo.consultar(ler("ID: "))
    if s is None:
        print("Registro não encontrado.")
    else:
        print(s.detalhes())


def atualizar(repo):
    id = ler("ID do registro a atualizar: ")
    s = repo.consultar(id)
    if s is None:
        print("Registro não encontrado.")
        return
    print("Deixe em branco para manter o valor atual.")
    novos = {}
    for campo in CAMPOS_OBRIGATORIOS:
        valor = ler(f"{NOMES_CAMPOS[campo].capitalize()} [{getattr(s, campo)}]: ")
        if valor.strip():
            novos[campo] = valor
    repo.atualizar(id, **novos)
    print("Registro atualizado:\n" + s.detalhes())


def excluir(repo):
    if repo.excluir(ler("ID do registro a excluir: ")):
        print("Registro excluído.")
    else:
        print("Registro não encontrado.")


def pesquisar(repo):
    opcao = ler("Pesquisar por (1) título ou (2) categoria: ").strip()
    campos = {"1": "titulo", "2": "categoria"}
    if opcao not in campos:
        print("Opção inválida. Digite 1 ou 2.")
        return
    resultado = repo.pesquisar(campos[opcao], ler("Termo: "))
    print(f"{len(resultado)} resultado(s):")
    mostrar_lista(resultado)


def ordenar(repo):
    opcao = ler("Ordenar por (1) ID ou (2) título: ").strip()
    criterios = {"1": "id", "2": "titulo"}
    if opcao not in criterios:
        print("Opção inválida. Digite 1 ou 2.")
        return
    repo.ordenar(criterios[opcao])
    print("Lista ordenada:")
    mostrar_lista(repo.listar())


def carregar_exemplos(repo):
    novos = dados_exemplo.carregar(repo)
    print(f"{novos} registro(s) de exemplo carregado(s).")


ACOES = {
    "1": cadastrar,
    "2": listar,
    "3": consultar,
    "4": atualizar,
    "5": excluir,
    "6": pesquisar,
    "7": ordenar,
    "8": carregar_exemplos,
}


def main():
    # Garante acentos corretos no terminal do Windows e em arquivos redirecionados.
    for fluxo in (sys.stdout, sys.stdin):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")

    repo = RepositorioServicos()
    while True:
        print(MENU)
        opcao = ler("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        acao = ACOES.get(opcao)
        if acao is None:
            print("Opção inválida. Escolha um número de 0 a 8.")
            continue
        try:
            acao(repo)
        except ValueError as erro:      # validações do crud.py
            print(f"Erro: {erro}.")


if __name__ == "__main__":
    main()
