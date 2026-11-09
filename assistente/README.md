# Assistente CadU (terminal)

Chatbot **por regras** (sem IA generativa) que responde dúvidas sobre CadÚnico e benefícios usando só a base `dados/base.json`. Toda resposta traz fonte oficial e data de verificação. Se não sabe, diz que não sabe e indica o **121** e o **CRAS**; nunca inventa.

O app web (`app/`) importa este mesmo pacote: não existe código duplicado.

## Como rodar

Na raiz do repositório (precisa de Python 3.12; não tem dependências externas):

```bash
py -3.12 -m assistente
```

Comandos dentro do chat: `/historico`, `/indicadores`, `/exportar arquivo.csv`, `/ajuda`, `/sair`.

Escolher outra base: `py -3.12 -m assistente --base caminho/do/arquivo.json`.
Se `dados/base.json` não existir, usa `dados/base_exemplo.json` (e avisa que é exemplo).

## Testes

```bash
py -3.12 -m unittest discover -s assistente/testes -t .
```

## As 3 classes

- `Orientacao` (`orientacao.py`): um assunto da base. Sabe se pontuar para uma mensagem (`pontuar`).
- `BaseConhecimento` (`base_conhecimento.py`): lê o JSON, valida os campos e acha a orientação com mais pontos (`melhor`). `conferir_qualidade()` lista o que falta para a entrega (10+ orientações, 3+ categorias, 3+ palavras-chave cada).
- `Assistente` (`assistente.py`): recebe a mensagem, aplica as regras, guarda o histórico, calcula indicadores e exporta CSV.

## Regras de pontuação

Para cada orientação, depois de tirar acentos e maiúsculas:

- +3 por palavra-chave encontrada na mensagem (aceita plural simples: "benefício" casa com "benefícios");
- +1 por palavra do título com 4 ou mais letras que aparece na mensagem.

Vence a orientação com mais pontos (empate: a primeira do arquivo).

- 6 ou mais pontos: **ALTA** (responde direto);
- 3 a 5: **MEDIA** (responde avisando "acho que isso pode ajudar");
- menos de 3: **SEM_RESPOSTA** (indica 121 e CRAS). Se a mensagem tem palavra de fora do assunto (futebol, piada, receita...) o nível é **FORA_ESCOPO** ("só ajudo com CadÚnico e benefícios"). Saudações ("oi", "bom dia") também recebem a apresentação.

## Segurança da entrada

- Mensagem com `@` ou **8 ou mais dígitos** (CPF, NIS, telefone, e-mail) é **recusada e não é registrada** (só entra um contador anônimo `recusadas`).
- Limite de 300 caracteres por mensagem; acima disso é recusada e não registrada.
- No CSV, textos que começam com `= + - @` ganham um `'` na frente (evita fórmula maliciosa no Excel).
- `Assistente(base, guardar_texto=False)` não guarda o que a pessoa digitou, só as contagens (é assim que o app web usa).

## Esquema do JSON da base (para a pesquisa de `dados/`)

```json
{
  "versao": "2026-11-xx",
  "orientacoes": [
    {
      "id": "bolsa-familia",
      "titulo": "Bolsa Família",
      "categoria": "Benefícios",
      "palavras_chave": ["bolsa familia", "bolsa", "transferencia de renda"],
      "resposta": "Texto curto, em linguagem simples.",
      "passos": ["Primeiro passo.", "Segundo passo."],
      "prazo": "Texto livre, ou \"\" se não houver.",
      "fonte_nome": "Ministério do Desenvolvimento e Assistência Social",
      "fonte_url": "https://www.gov.br/...",
      "data_verificacao": "2026-11-09"
    }
  ]
}
```

Obrigatórios: `id` (único, sem espaço), `titulo`, `categoria`, `palavras_chave` (lista), `resposta`, `fonte_nome`, `fonte_url` (https, página oficial real), `data_verificacao` (AAAA-MM-DD, dia em que a página foi conferida). Opcionais: `passos`, `prazo`. Campos extras no topo (`versao`, etc.) são aceitos.

Dicas para quem escreve a base:

- Mínimo da entrega: **10 orientações, 3 categorias, 3 palavras-chave por orientação**. Confira com `BaseConhecimento.carregar("dados/base.json").conferir_qualidade()` (lista vazia = ok).
- Palavras-chave: pense em como a pessoa escreveria ("bolsa familia", "conta de luz", "cras"). Acento e maiúscula não importam. Use frases e palavras soltas.
- Cuidado com palavras do título com 4+ letras (valem +1): evite "como", "para", "que" em títulos.
- `dados/base_exemplo.json` é só um exemplo de formato (marcado `"exemplo": true`); o conteúdo dele não é orientação oficial.
