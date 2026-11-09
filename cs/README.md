# Verificador de expressões booleanas

Programa que testa todas as combinações das variáveis (3 ou 4) e confere se a
expressão simplificada dá o mesmo resultado da original.

## Onde colocar as expressões

Abra `expressoes.py` e, entre os marcadores "COMECE A EDITAR" e "TERMINE DE EDITAR":

1. troque `NOMES` pelas suas variáveis;
2. reescreva `original` e `simplificada` (use `and`, `or`, `not`);
3. mude `EXEMPLO = True` para `EXEMPLO = False`.

O que está no arquivo hoje é só exemplo.

## Como rodar

Dentro da pasta `cs/`:

```bash
py -3.12 verificador.py
```

Mostra uma linha por combinação (valores, resultado de cada expressão, IGUAL ou
DIFERENTE) e um resumo no final.

## Testes

```bash
py -3.12 -m unittest -v
```
