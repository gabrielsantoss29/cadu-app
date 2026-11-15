"""Contadores anônimos do CadU (Neon / Postgres).

Guarda SÓ números agregados: quantas triagens foram feitas, quantas vezes cada assunto foi
consultado e quantas pessoas disseram que a resposta ajudou. Nunca guarda texto digitado,
IP, nem qualquer identificador de pessoa.

Se não houver banco configurado (variável DATABASE_URL ou POSTGRES_URL), tudo vira no-op:
o app funciona igual, só não conta.
"""
import os

try:
    import psycopg
except ImportError:  # sem a biblioteca, não conta (o app segue normal)
    psycopg = None


def _url():
    return os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or ""


def ativo() -> bool:
    return bool(psycopg and _url())


def _conectar():
    return psycopg.connect(_url(), connect_timeout=5, autocommit=True)


def somar(chave: str) -> bool:
    """Soma 1 ao contador. Devolve False se não deu (sem banco ou erro): nunca derruba o app."""
    if not ativo():
        return False
    try:
        with _conectar() as con:
            con.execute("CREATE TABLE IF NOT EXISTS contadores (chave text PRIMARY KEY, total bigint NOT NULL DEFAULT 0)")
            con.execute("INSERT INTO contadores (chave, total) VALUES (%s, 1) "
                        "ON CONFLICT (chave) DO UPDATE SET total = contadores.total + 1", (chave,))
        return True
    except Exception:
        return False


def totais() -> dict:
    if not ativo():
        return {}
    try:
        with _conectar() as con:
            con.execute("CREATE TABLE IF NOT EXISTS contadores (chave text PRIMARY KEY, total bigint NOT NULL DEFAULT 0)")
            return {k: int(t) for k, t in con.execute("SELECT chave, total FROM contadores ORDER BY chave").fetchall()}
    except Exception:
        return {}
