# App web do CadU

Flask + páginas HTML com Tailwind. O app oficial do Cadastro Único consulta e informa; o CadU **acompanha**: linguagem simples, áudio, triagem, passo a passo quando dá problema, calculadora de energia. Consulta por CPF e comprovante ficam com o app oficial (o CadU leva a pessoa até lá).

## Como rodar local

Na raiz do repositório:

```bash
py -3.12 -m venv app/.venv
app/.venv/Scripts/python -m pip install -r app/requirements.txt
app/.venv/Scripts/python app/app.py
```

Abra http://127.0.0.1:5000. Testes: `app/.venv/Scripts/python -m unittest app.test_app`.

## Telas

- `/` Início: atalhos grandes (dúvida, benefícios, bloqueio, atualizar cadastro, conta de luz, atendimento).
- `/triagem`: uma pergunta por tela, 4 passos (abertura, "já está no CadÚnico?", "quais benefícios recebe?", chat). Nunca pergunta renda.
- `/beneficios`: cartões por categoria, etiquetas "Você recebe" (da triagem) e "Pode combinar" (da base, campo `pode_combinar`).
- `/cadu`: chat estilo WhatsApp com microfone grande e botão "Ouvir" em cada resposta.
- `/energia`: calculadora (aparelhos, horas por dia, kWh por mês, custo com preço do kWh editável, comparação com limite, dicas).
- `/mais`: atendimento oficial (121, CRAS, app oficial), apagar meus dados, sobre.

Layout: menu lateral no computador, barra inferior no celular, botão redondo do CadU (mascote) em todas as telas, menos chat e triagem. Letra mínima 16px e alvos de toque de 48px ou mais.

## Arquivos

- `app.py`: rotas e API. `POST /api/chat` (`{"mensagem": "..."}`) usa `Assistente.analisar()` de `assistente/` (o mesmo código do terminal). `GET /api/orientacao/<codigo>` abre um assunto direto (atalhos).
- `templates/`: páginas Jinja (escapam HTML sozinhas). `base.html` tem a paleta, o menu e o botão flutuante; `_icones.html` tem os ícones.
- `static/mascote.svg`: mascote **provisório**. Para trocar a persona, troque só este arquivo.
- `static/app.js` (comum), `triagem.js`, `chat.js`, `energia.js`.
- Dados da energia: `../energia/aparelhos_provisorio.json` (**provisório**, até chegar o `energia.json`). O limite de comparação é `limite_kwh` nesse arquivo.

Paleta: azul `#1B5FC1`, azul escuro `#12408A`, azul claro `#E6EEFB`, fundo `#F6F9FF`, texto `#14213D`, amarelo `#F5B72E`; verde só para sucesso.

## Privacidade e segurança

- O servidor não grava nada em disco nem guarda o que a pessoa digita (o assistente roda sem histórico).
- A triagem fica só no `localStorage` do aparelho, com "Apagar meus dados".
- O assistente recusa mensagens com `@` ou 8+ dígitos e com mais de 300 letras.
- Todo texto entra na tela com `textContent` (nunca `innerHTML`); links da fonte só se forem http/https.

## Vercel

`app.py` expõe a variável `app`. As pastas `assistente/` e `energia/` ficam fora de `app/`: publicar a partir da raiz do repositório (ainda não configurado).

## Falta fazer

- Voz própria (Whisper e Kokoro). Hoje "Ouvir" e o microfone usam a voz do navegador; o microfone não funciona em todo navegador (o chat avisa).
- Mapa de postos (Leaflet, São Paulo).
- Pergunta "Quem mora com você", dentro do chat, quando fizer sentido.
- Etiqueta "Pode combinar": depende do campo `pode_combinar` vir da pesquisa.
- Contagens anônimas em banco Neon. Deploy na Vercel.
