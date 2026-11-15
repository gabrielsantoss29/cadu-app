"""Gera os áudios do botão "Ouvir" com a voz do CadU (Kokoro, voz pm_alex, pt-BR).

Os áudios ficam em app/static/audio/<hash>.mp3, onde <hash> vem do texto lido.
O navegador calcula o mesmo hash e toca o arquivo; se não achar, usa a voz do navegador.
Rode de novo sempre que os textos mudarem (base de conhecimento ou telas).

Precisa de: pip install kokoro-onnx lameenc Flask
Modelos (baixar uma vez, de https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0):
  kokoro-v1.0.onnx e voices-v1.0.bin

Uso:  python ferramentas/gerar_audios.py CAMINHO_DOS_MODELOS
"""
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import lameenc
import numpy as np
from kokoro_onnx import Kokoro

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from app.app import app, base  # noqa: E402

VOZ = "pm_alex"
SAIDA = RAIZ / "app" / "static" / "audio"
PAGINAS = ["/", "/triagem", "/beneficios", "/energia", "/cadu", "/mais", "/mapa"]

# Como falar siglas e símbolos (só para o áudio; o texto na tela não muda)
FALAS = [
    ("CPF", "C P F"), ("BPC", "B P C"), ("INSS", "I N S S"), ("MEC", "M E C"), ("NIS", "nis"),
    ("CRAS", "crás"), ("CREAS", "créas"), ("kWh", "quilowatt-hora"), ("R$", "reais"),
    ("gov.br", "gov ponto B R"), ("MDS", "M D S"), ("SUS", "sus"), ("ODS", "O D S"),
]


def normalizar(texto: str) -> str:
    return " ".join(texto.split())


def chave(texto: str) -> str:
    """Mesmo cálculo do app.js: SHA-1 do texto normalizado, 16 primeiros caracteres hexadecimais."""
    return hashlib.sha1(normalizar(texto).encode("utf-8")).hexdigest()[:16]


class Alvos(HTMLParser):
    """Acha o texto dos elementos apontados por data-ouvir="#id"."""

    def __init__(self):
        super().__init__()
        self.ids_pedidos, self.textos, self._abertos = set(), {}, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "data-ouvir" in a:
            self.ids_pedidos.add(a["data-ouvir"].lstrip("#"))
        if tag in ("br", "img", "input", "meta", "link", "path", "hr"):
            return
        self._abertos = [(t, i, buf) for t, i, buf in self._abertos]
        self._abertos.append((tag, a.get("id"), []))

    def handle_endtag(self, tag):
        while self._abertos:
            t, i, buf = self._abertos.pop()
            if t == tag:
                if i:
                    self.textos[i] = "".join(buf)
                if self._abertos:
                    self._abertos[-1][2].append("".join(buf))
                return

    def handle_data(self, dado):
        if self._abertos:
            self._abertos[-1][2].append(dado)


def coletar_textos() -> set:
    textos = set()
    for o in base.orientacoes:                      # resposta do chat: título + resposta
        textos.add(normalizar(f"{o.titulo}. {o.resposta}"))
    cliente = app.test_client()
    for url in PAGINAS:                             # botões "Ouvir" das telas
        p = Alvos()
        p.feed(cliente.get(url).get_data(as_text=True))
        for i in p.ids_pedidos:
            if i in p.textos and normalizar(p.textos[i]):
                textos.add(normalizar(p.textos[i]))
    chat = (RAIZ / "app" / "static" / "chat.js").read_text(encoding="utf-8")
    for m in re.finditer(r'falaCadu\("([^"+]{12,})"\)', chat):   # frases fixas do CadU
        textos.add(normalizar(m.group(1)))
    return textos


def para_voz(texto: str) -> str:
    for de, para in FALAS:
        texto = re.sub(rf"(?<!\w){re.escape(de)}(?!\w)", para, texto)
    return texto


def main():
    modelos = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    kokoro = Kokoro(str(modelos / "kokoro-v1.0.onnx"), str(modelos / "voices-v1.0.bin"))
    SAIDA.mkdir(parents=True, exist_ok=True)
    textos = sorted(coletar_textos())
    esperados = set()
    for n, texto in enumerate(textos, 1):
        arq = SAIDA / f"{chave(texto)}.mp3"
        esperados.add(arq.name)
        if arq.exists():
            continue
        amostras, taxa = kokoro.create(para_voz(texto), voice=VOZ, speed=0.95, lang="pt-br")
        pcm = (np.clip(amostras, -1, 1) * 32767).astype(np.int16)
        enc = lameenc.Encoder()
        enc.set_bit_rate(48); enc.set_in_sample_rate(taxa); enc.set_channels(1); enc.set_quality(2)
        arq.write_bytes(enc.encode(pcm.tobytes()) + enc.flush())
        print(f"[{n}/{len(textos)}] {arq.name} {texto[:50]}")
    for velho in SAIDA.glob("*.mp3"):               # apaga áudios de textos que não existem mais
        if velho.name not in esperados:
            velho.unlink()
    print(f"{len(textos)} textos, {sum(f.stat().st_size for f in SAIDA.glob('*.mp3')) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
