"""Assistente virtual do CadU (chatbot por regras, sem IA generativa).

O terminal (`python -m assistente`) e o app web (Flask) usam ESTE mesmo pacote.
"""
from .orientacao import Orientacao
from .base_conhecimento import BaseConhecimento, ErroBase
from .assistente import Assistente, Resposta, ALTA, MEDIA, SEM_RESPOSTA, FORA_ESCOPO, RECUSADA

__all__ = [
    "Orientacao", "BaseConhecimento", "ErroBase", "Assistente", "Resposta",
    "ALTA", "MEDIA", "SEM_RESPOSTA", "FORA_ESCOPO", "RECUSADA",
]
