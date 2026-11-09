"""Classe Assistente: recebe a mensagem, aplica as regras e responde."""
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from .base_conhecimento import BaseConhecimento
from .orientacao import Orientacao
from .texto import palavras

# Níveis de confiança da resposta.
ALTA, MEDIA, SEM_RESPOSTA = "ALTA", "MEDIA", "SEM_RESPOSTA"
FORA_ESCOPO, RECUSADA = "FORA_ESCOPO", "RECUSADA"

LIMITE_ALTA = 6       # 6 pontos ou mais = ALTA
LIMITE_MEDIA = 3      # de 3 a 5 = MÉDIA; abaixo disso = sem resposta
TAMANHO_MAXIMO = 300  # caracteres por mensagem

TEXTO_SEM_RESPOSTA = (
    "Não sei responder isso com segurança, e prefiro não inventar. "
    "Ligue para o 121 (Central de Atendimento do Governo) ou procure o CRAS "
    "da sua cidade. Lá eles ajudam de graça."
)
TEXTO_FORA_ESCOPO = (
    "Eu só ajudo com CadÚnico e benefícios sociais (como Bolsa Família, "
    "Tarifa Social de energia, BPC e outros). Pode me perguntar sobre isso!"
)
TEXTO_RECUSA_DADO = (
    "Por segurança, não escreva números longos (CPF, NIS, telefone, cartão) "
    "nem e-mail. Eu não preciso desses dados e não guardo nada disso. "
    "Pode refazer a pergunta sem eles."
)
TEXTO_SAUDACAO = (
    "Oi, eu sou o CadU! Posso explicar benefícios do CadÚnico, prazos e o que "
    "fazer. Sobre o que você quer saber?"
)

# Palavras que indicam assunto de fora (lista curta e simples).
PALAVRAS_FORA = {
    "futebol", "piada", "receita", "bolo", "filme", "musica", "novela", "jogo",
    "namorado", "namorada", "horoscopo", "bitcoin", "eleicao", "presidente",
    "time", "celebridade", "clima", "carro", "celular", "programar",
}
SAUDACOES = {"oi", "ola", "bom dia", "boa tarde", "boa noite", "e ai"}


@dataclass
class Resposta:
    nivel: str
    texto: str
    pontuacao: int = 0
    orientacao_id: str = ""
    categoria: str = ""
    fonte_nome: str = ""
    fonte_url: str = ""
    data_verificacao: str = ""

    def para_dict(self) -> dict:
        return asdict(self)


@dataclass
class Consulta:
    """Uma linha do histórico."""
    momento: str
    mensagem: str
    nivel: str
    pontuacao: int
    orientacao_id: str
    categoria: str


class Assistente:
    def __init__(self, base: BaseConhecimento, guardar_texto: bool = True):
        """guardar_texto=False: não guarda a mensagem digitada, só conta
        (usado no app web, que não deve reter o que as pessoas escrevem)."""
        self.base = base
        self.guardar_texto = guardar_texto
        self.historico: list[Consulta] = []
        self.recusadas = 0
        self._niveis = {ALTA: 0, MEDIA: 0, SEM_RESPOSTA: 0, FORA_ESCOPO: 0}
        self._categorias: dict[str, int] = {}

    # ---------- segurança da entrada ----------
    @staticmethod
    def entrada_insegura(mensagem: str) -> bool:
        """True se tiver '@' ou 8+ dígitos (parece e-mail, CPF, telefone...)."""
        digitos = sum(c.isdigit() for c in mensagem)
        return "@" in mensagem or digitos >= 8

    # ---------- resposta ----------
    def responder(self, mensagem: str) -> Resposta:
        mensagem = (mensagem or "").strip()
        if not mensagem:
            return Resposta(RECUSADA, "Escreva sua pergunta, por favor.")
        if len(mensagem) > TAMANHO_MAXIMO:
            return Resposta(RECUSADA, f"Mensagem muito longa. Use até {TAMANHO_MAXIMO} letras.")
        if self.entrada_insegura(mensagem):
            self.recusadas += 1          # só conta; o texto NÃO é guardado
            return Resposta(RECUSADA, TEXTO_RECUSA_DADO)

        orientacao, pontos = self.base.melhor(mensagem)
        if pontos >= LIMITE_ALTA:
            resp = self._com_orientacao(ALTA, orientacao, pontos)
        elif pontos >= LIMITE_MEDIA:
            resp = self._com_orientacao(MEDIA, orientacao, pontos)
        elif self._eh_saudacao(mensagem):
            resp = Resposta(FORA_ESCOPO, TEXTO_SAUDACAO, pontos)
        elif self._eh_fora_escopo(mensagem):
            resp = Resposta(FORA_ESCOPO, TEXTO_FORA_ESCOPO, pontos)
        else:
            resp = Resposta(SEM_RESPOSTA, TEXTO_SEM_RESPOSTA, pontos)
        self._registrar(mensagem, resp)
        return resp

    @staticmethod
    def _eh_saudacao(mensagem: str) -> bool:
        return " ".join(palavras(mensagem)) in SAUDACOES

    @staticmethod
    def _eh_fora_escopo(mensagem: str) -> bool:
        return bool(set(palavras(mensagem)) & PALAVRAS_FORA)

    @staticmethod
    def _com_orientacao(nivel: str, o: Orientacao, pontos: int) -> Resposta:
        partes = []
        if nivel == MEDIA:
            partes.append("Acho que isso pode ajudar (confira se é o que você queria):")
        partes.append(o.resposta)
        if o.passos:
            partes.append("O que fazer:\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(o.passos, 1)))
        if o.prazo:
            partes.append(f"Prazo: {o.prazo}")
        return Resposta(nivel, "\n\n".join(partes), pontos, o.id, o.categoria,
                        o.fonte_nome, o.fonte_url, o.data_verificacao)

    # ---------- histórico e indicadores ----------
    def _registrar(self, mensagem: str, resp: Resposta) -> None:
        self._niveis[resp.nivel] += 1
        if resp.categoria:
            self._categorias[resp.categoria] = self._categorias.get(resp.categoria, 0) + 1
        if self.guardar_texto:
            self.historico.append(Consulta(
                datetime.now().isoformat(timespec="seconds"), mensagem, resp.nivel,
                resp.pontuacao, resp.orientacao_id, resp.categoria))

    def indicadores(self) -> dict:
        return {
            "total": sum(self._niveis.values()),
            "por_nivel": dict(self._niveis),
            "por_categoria": dict(self._categorias),
            "recusadas": self.recusadas,
        }

    def exportar_csv(self, caminho: str | Path) -> int:
        """Salva o histórico em CSV (UTF-8 com BOM, abre bem no Excel).
        Devolve o número de linhas gravadas."""
        def seguro(v):
            # Evita "injeção de fórmula" no Excel: célula que começa com = + - @
            v = str(v)
            return "'" + v if v[:1] in ("=", "+", "-", "@") else v

        with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["momento", "mensagem", "nivel", "pontuacao", "orientacao_id", "categoria"])
            for c in self.historico:
                w.writerow([c.momento, seguro(c.mensagem), c.nivel, c.pontuacao,
                            c.orientacao_id, c.categoria])
        return len(self.historico)
