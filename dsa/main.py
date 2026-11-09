"""Demonstração em terminal. Rode com:  py -3.12 dsa/main.py"""

from crud import RepositorioOrientacoes
from lista_ligada import HistoricoPerguntas
from ordenacao import merge_sort


def titulo(texto):
    print("\n=== " + texto + " ===")


def main():
    repo = RepositorioOrientacoes()

    titulo("1. CRIAR")
    repo.criar(1, "Como fazer o Cadastro Único", "cadastro", ["cadunico", "inscricao", "cras"])
    repo.criar(2, "Prazo para atualizar o cadastro", "cadastro", ["atualizar", "prazo", "cadunico"])
    repo.criar(3, "Quem tem direito ao Bolsa Família", "beneficio", ["bolsa", "familia", "renda"])
    repo.criar(4, "Tarifa Social de Energia", "energia", ["energia", "luz", "tarifa", "desconto"])
    print(f"{len(repo)} orientações criadas")

    titulo("2. LISTAR")
    for o in repo.listar():
        print(" ", o)

    titulo("3. BUSCAR")
    print("por id 3:       ", repo.buscar_por_id(3))
    print("por id 99:      ", repo.buscar_por_id(99))
    print("categoria cadastro:", repo.buscar_por_categoria("Cadastro"))

    titulo("4. ATUALIZAR")
    repo.atualizar(2, titulo="Prazo para atualizar o CadÚnico (a cada 2 anos)")
    print(repo.buscar_por_id(2))

    titulo("5. REMOVER")
    print("removeu id 4?", repo.remover(4))
    print("removeu id 4 de novo?", repo.remover(4))
    print(f"restam {len(repo)}")

    titulo("6. RANQUEAMENTO (merge sort próprio)")
    pergunta = "qual o prazo para atualizar o cadúnico?"
    print("pergunta:", pergunta)
    for pontos, o in repo.ranquear(pergunta):
        print(f"  {pontos} pontos -> {o.titulo}")

    titulo("7. ORDENAÇÃO SOLTA")
    print(merge_sort([5, 2, 9, 1, 5, 6]))
    print(merge_sort([5, 2, 9, 1, 5, 6], decrescente=True))

    titulo("8. HISTÓRICO (lista ligada, guarda as 3 últimas)")
    historico = HistoricoPerguntas(capacidade=3)
    for p in ["pergunta 1", "pergunta 2", "pergunta 3", "pergunta 4"]:
        historico.registrar(p)
    print(historico.recentes())   # a 1 saiu


if __name__ == "__main__":
    main()
