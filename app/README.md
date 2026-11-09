# App web do CadU (esqueleto)

Flask + páginas HTML com Tailwind. **Visual provisório (placeholder)**: o modelo de design ainda será escolhido.

## Como rodar local

Na raiz do repositório:

```bash
py -3.12 -m venv app/.venv
app/.venv/Scripts/python -m pip install -r app/requirements.txt
app/.venv/Scripts/python app/app.py
```

Abra http://127.0.0.1:5000. Testes: `app/.venv/Scripts/python -m unittest app.test_app`.

## O que tem

- `app.py`: rotas das páginas (`/`, `/beneficios`, `/energia`, `/cadu`, `/mais`) e a API `POST /api/chat` (`{"mensagem": "..."}`), que usa o pacote `assistente/` (o mesmo do terminal).
- `templates/`: páginas Jinja (escapam HTML sozinhas). `base.html` tem o menu lateral (computador), a barra de baixo (celular) e o botão redondo do CadU.
- `static/app.js`: apagar dados, botão "Ouvir" (voz do navegador, provisória).
- `static/chat.js`: triagem de 4 passos e chat. Respostas só no `localStorage` do aparelho. Todo texto entra na tela com `textContent` (nunca `innerHTML`).

## Base de dados

Usa `dados/base.json`; se não existir, `dados/base_exemplo.json` (aparece um aviso amarelo). Dá para forçar outra com a variável `CADU_BASE`.

## Privacidade e Vercel

- Não escreve em disco. O assistente roda com `guardar_texto=False`: o servidor não guarda o que a pessoa digita.
- A triagem nunca pergunta renda e não pede nome/CPF; o assistente recusa mensagens com `@` ou 8+ dígitos.
- Para publicar na Vercel: o arquivo `app.py` expõe a variável `app`. Falta configurar o projeto na Vercel (a pasta `assistente/` e `dados/` ficam fora de `app/`, então o projeto deve ser publicado a partir da raiz ou com "incluir arquivos fora do diretório raiz" ligado).

## Falta fazer

- Aplicar o modelo de design escolhido (trocar o Tailwind por CDN pelo build).
- Pergunta "Quem mora com você", dentro do chat, só quando fizer sentido.
- Calculadora de energia, mapa de postos (Leaflet, só São Paulo), voz (Whisper/Kokoro).
- Contagens anônimas em banco Neon.
