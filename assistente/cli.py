"""Assistente de terminal. Rode: python -m assistente"""
import argparse
import sys
from pathlib import Path

from .assistente import Assistente
from .base_conhecimento import BaseConhecimento, ErroBase

RAIZ = Path(__file__).resolve().parent.parent   # pasta do repositório


def achar_base(caminho: str | None) -> Path:
    """Usa o caminho dado; senão dados/base.json; senão o arquivo de exemplo."""
    if caminho:
        return Path(caminho)
    real = RAIZ / "dados" / "base.json"
    return real if real.exists() else RAIZ / "dados" / "base_exemplo.json"


AJUDA = (
    "Comandos: /historico  /indicadores  /exportar [arquivo.csv]  /ajuda  /sair\n"
    "Ou escreva sua pergunta."
)


def mostrar_resposta(r) -> None:
    print(f"\nCadU [{r.nivel}]: {r.texto}")
    if r.fonte_url:
        print(f"Fonte: {r.fonte_nome} - {r.fonte_url} (verificado em {r.data_verificacao})")
    print()


def mostrar_indicadores(a: Assistente) -> None:
    ind = a.indicadores()
    print(f"\nTotal de consultas: {ind['total']}")
    for nivel, n in ind["por_nivel"].items():
        print(f"  {nivel}: {n}")
    print(f"  Recusadas (dado pessoal): {ind['recusadas']}")
    print("Por categoria:")
    for cat, n in sorted(ind["por_categoria"].items()):
        print(f"  {cat}: {n}")
    print()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Assistente CadU (terminal)")
    ap.add_argument("--base", help="caminho do JSON da base (padrão: dados/base.json)")
    args = ap.parse_args(argv)
    # Console do Windows às vezes não usa UTF-8: força, para os acentos saírem certos.
    for fluxo in (sys.stdout, sys.stdin):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")
    try:
        base = BaseConhecimento.carregar(achar_base(args.base))
    except ErroBase as e:
        print(f"Erro: {e}")
        return 1

    a = Assistente(base)
    print("=== CadU - assistente de CadÚnico e benefícios ===")
    print("Não sou canal oficial e não preciso de dados pessoais (CPF, NIS...).")
    if base.eh_exemplo:
        print("ATENÇÃO: usando a base de EXEMPLO (só para teste).")
    print(AJUDA)

    while True:
        try:
            linha = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not linha:
            continue
        if linha.startswith("/"):
            cmd, *resto = linha.split(maxsplit=1)
            if cmd == "/sair":
                break
            elif cmd == "/ajuda":
                print(AJUDA)
            elif cmd == "/indicadores":
                mostrar_indicadores(a)
            elif cmd == "/historico":
                for c in a.historico:
                    print(f"{c.momento} [{c.nivel}] {c.mensagem}")
                if not a.historico:
                    print("(vazio)")
            elif cmd == "/exportar":
                destino = resto[0] if resto else "historico.csv"
                n = a.exportar_csv(destino)
                print(f"{n} consultas salvas em {destino}")
            else:
                print("Comando desconhecido. Digite /ajuda.")
            continue
        mostrar_resposta(a.responder(linha))

    print("Até logo!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
