"""Gera dsa/EVIDENCIAS.md rodando o menu de verdade com entradas pré-definidas.

Cada cenário abre o programa do zero, digita as entradas e guarda a saída
do terminal (o "resultado observado"). Rode na raiz do repositório:

    py -3.12 dsa/testes/gerar_evidencias.py
"""

import os
import subprocess
import sys

PASTA_DSA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, PASTA_DSA)

from main import MENU  # noqa: E402

# (título, explicação da entrada, linhas digitadas, resultado esperado)
CENARIOS = (
    ("Operações sobre lista vazia",
     "Sem carregar nada: listar (2), consultar o ID 1 (3), excluir o ID 1 (5) e ordenar por título (7).",
     ["2", "3", "1", "5", "1", "7", "2", "0"],
     "Total 0 e 'Nenhum registro encontrado.' em todas as operações, sem erro."),
    ("Opções de menu inválidas",
     "Digitar 9, depois 'abc', depois nada (Enter).",
     ["9", "abc", "", "0"],
     "Três vezes 'Opção inválida. Escolha um número de 0 a 8.' e o menu continua."),
    ("Cadastro com múltiplos registros",
     "Carregar os 5 exemplos (8), cadastrar o ID 6 com todos os campos e listar (2).",
     ["8", "1", "6", "Tarifa Social de Energia", "energia",
      "Desconto na conta de luz para famílias de baixa renda", "Famílias inscritas no CadÚnico",
      "Distribuidora de energia", "luz, energia, desconto", "2", "0"],
     "5 exemplos carregados, ID 6 cadastrado e listagem com 6 registros."),
    ("Cadastro com ID duplicado",
     "Carregar exemplos e tentar cadastrar o ID 1, que já existe.",
     ["8", "1", "1", "0"],
     "Erro: já existe um registro com o identificador 1."),
    ("Cadastro com ID inválido",
     "Tentar cadastrar com ID 'abc' e depois com ID -5.",
     ["1", "abc", "1", "-5", "0"],
     "Duas vezes: Erro: o identificador deve ser um número inteiro positivo."),
    ("Cadastro com campo obrigatório vazio",
     "Cadastrar o ID 10 deixando o título só com espaços.",
     ["1", "10", "   ", "saúde", "desc", "todos", "UBS", "", "2", "0"],
     "Erro: o campo título é obrigatório. A listagem continua vazia (Total: 0)."),
    ("Consulta por ID",
     "Carregar exemplos e consultar o ID 5, o ID 99 (não existe) e o ID 'x' (inválido).",
     ["8", "3", "5", "3", "99", "3", "x", "0"],
     "Detalhes completos do ID 5; 'Registro não encontrado.' para o 99; erro de identificador para 'x'."),
    ("Atualização",
     "Carregar exemplos, atualizar só o título do ID 5 (Enter mantém os outros campos) e tentar atualizar o ID 99.",
     ["8", "4", "5", "Campanha de vacinação", "", "", "", "", "4", "99", "0"],
     "ID 5 com título novo e demais campos iguais; 'Registro não encontrado.' para o 99."),
    ("Exclusão",
     "Carregar exemplos, excluir o ID 3 (primeiro da lista), tentar excluir de novo e listar.",
     ["8", "5", "3", "5", "3", "2", "0"],
     "'Registro excluído.', depois 'Registro não encontrado.', e a listagem com 4 registros sem o ID 3."),
    ("Pesquisa por categoria e por título",
     "Carregar exemplos; categoria 'ASSISTENCIA' (sem acento, maiúsculo); título 'cadúnico'; opção 3 (inválida); título vazio.",
     ["8", "6", "2", "ASSISTENCIA", "6", "1", "cadúnico", "6", "3", "6", "1", "", "0"],
     "IDs 3 e 4 na categoria; ID 4 no título; 'Opção inválida' para 3; erro de termo obrigatório para pesquisa vazia."),
    ("Ordenação por ID e por título",
     "Carregar exemplos (ficam na ordem 3, 1, 5, 2, 4), ordenar por ID, por título e tentar a opção 5.",
     ["8", "7", "1", "7", "2", "7", "5", "0"],
     "IDs 1 a 5 em ordem; títulos em ordem alfabética (ignorando acento); 'Opção inválida' para 5."),
)


def rodar(entradas):
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, os.path.join(PASTA_DSA, "main.py")],
        input="\n".join(entradas) + "\n",
        capture_output=True, text=True, encoding="utf-8", env=ambiente, check=True,
    )
    # Tira o menu repetido para a evidência ficar legível.
    saida = proc.stdout.replace(MENU.strip("\n"), "[menu]")
    return saida.strip()


def main():
    partes = [
        "# Evidências dos testes (DSA)\n",
        "Gerado por `py -3.12 dsa/testes/gerar_evidencias.py`, que roda o menu de verdade "
        "com as entradas abaixo. O texto do menu foi trocado por `[menu]` para facilitar a leitura. "
        "Cada valor digitado aparece logo depois da pergunta.\n",
    ]
    for numero, (titulo, explicacao, entradas, esperado) in enumerate(CENARIOS, start=1):
        partes.append(f"## {numero}. {titulo}\n")
        partes.append(f"**Entrada:** {explicacao}\n")
        partes.append("Linhas digitadas: `" + " | ".join(e if e else "(Enter)" for e in entradas) + "`\n")
        partes.append(f"**Resultado esperado:** {esperado}\n")
        partes.append("**Resultado observado:**\n")
        partes.append("```text\n" + rodar(entradas) + "\n```\n")
    destino = os.path.join(PASTA_DSA, "EVIDENCIAS.md")
    with open(destino, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(partes))
    print(f"{len(CENARIOS)} cenarios gravados em {os.path.abspath(destino)}")


if __name__ == "__main__":
    main()
