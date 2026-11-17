# Módulo de decisão lógica (Computer Science)

Dois programas em Python, sem bibliotecas externas:

- `assistente.py`: o usuário responde às perguntas (1 ou 0) e vê a orientação. Usa a expressão simplificada. Respostas inválidas são recusadas e a pergunta é repetida. Digite `sair` para encerrar. Mostra o aviso de que não é um canal oficial, as limitações e as fontes, e não pede dados pessoais.
- `verificador.py`: testa todas as combinações das variáveis (8 ou 16) e mostra, para cada uma, a regra original, a expressão simplificada e o resultado executado pelo assistente, com IGUAL ou DIFERENTE. No final mostra um resumo.

## A regra

Situação: orientar a família sobre a atualização do Cadastro Único. Variáveis (1 = sim): A = 24 meses ou mais sem atualizar; B = mudou algo na família; C = recebe Bolsa Família; D = recebeu aviso de revisão ou averiguação. Saída S = 1 (procurar o CRAS com prioridade) ou 0 (sem urgência).

- Forma canônica: S = ΠM(0, 2, 4, 8, 12)
- Simplificada: S = D + A·C + B·C

A regra fica em `expressoes.py`, com as perguntas, os textos de orientação e as fontes.

## Como rodar

Dentro da pasta `cs/`:

```bash
py -3.12 assistente.py
```

```bash
py -3.12 verificador.py
```

O verificador termina com código 0 se tudo for igual e 1 se houver alguma diferença.

## Testes

```bash
py -3.12 -m unittest -v
```

Os testes conferem o verificador, o tratamento de entradas inválidas, o assistente e se a regra de `expressoes.py` é equivalente em todas as combinações.
