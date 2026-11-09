"""Funções pequenas de texto, usadas pelas três classes."""
import re
import unicodedata


def normalizar(texto: str) -> str:
    """Deixa em minúsculas e sem acento: 'Benefício' -> 'beneficio'."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.lower()


def palavras(texto: str) -> list[str]:
    """Separa em palavras (já normalizadas), ignorando pontuação."""
    return re.findall(r"[a-z0-9]+", normalizar(texto))
