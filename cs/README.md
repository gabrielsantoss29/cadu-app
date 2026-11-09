# Módulo de decisão lógica (Computer Science)

Dois programas em Python, sem bibliotecas externas:

- `assistente.py`: o usuário responde às perguntas (1 ou 0) e vê a orientação. Usa a expressão simplificada. Respostas inválidas são recusadas e a pergunta é repetida. Digite `sair` para encerrar. Mostra o aviso de que não é um canal oficial, as limitações e as fontes, e não pede dados pessoais.
- `verificador.py`: testa todas as combinações das variáveis (8 ou 16) e mostra, para cada uma, a regra original, a expressão simplificada e o resultado executado pelo assistente, com IGUAL ou DIFERENTE. No final mostra um resumo.

## Onde colocar a regra

Abra `expressoes.py` e edite só o trecho entre "COMECE A EDITAR" e "TERMINE DE EDITAR":

1. `NOMES`: as variáveis (3 ou 4), na ordem da tabela-verdade;
2. `PERGUNTAS`: o que o assistente pergunta para cada variável (o que é 1 e o que é 0);
3. `original` e `simplificada`: as expressões (use `and`, `or`, `not`);
4. `ORIENTACAO`: o texto para a saída 1 e para a saída 0;
5. `FONTES`: as fontes das regras, com data de consulta;
6. mude `EXEMPLO = True` para `EXEMPLO = False`.

O que está no arquivo hoje é só exemplo.

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
