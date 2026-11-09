# Evidências dos testes (DSA)

Gerado por `py -3.12 dsa/testes/gerar_evidencias.py`, que roda o menu de verdade com as entradas abaixo. O texto do menu foi trocado por `[menu]` para facilitar a leitura. Cada valor digitado aparece logo depois da pergunta.

## 1. Operações sobre lista vazia

**Entrada:** Sem carregar nada: listar (2), consultar o ID 1 (3), excluir o ID 1 (5) e ordenar por título (7).

Linhas digitadas: `2 | 3 | 1 | 5 | 1 | 7 | 2 | 0`

**Resultado esperado:** Total 0 e 'Nenhum registro encontrado.' em todas as operações, sem erro.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 2
Total: 0 registro(s)
Nenhum registro encontrado.

[menu]
Escolha uma opção: 3
ID: 1
Registro não encontrado.

[menu]
Escolha uma opção: 5
ID do registro a excluir: 1
Registro não encontrado.

[menu]
Escolha uma opção: 7
Ordenar por (1) ID ou (2) título: 2
Lista ordenada:
Nenhum registro encontrado.

[menu]
Escolha uma opção: 0
Até logo!
```

## 2. Opções de menu inválidas

**Entrada:** Digitar 9, depois 'abc', depois nada (Enter).

Linhas digitadas: `9 | abc | (Enter) | 0`

**Resultado esperado:** Três vezes 'Opção inválida. Escolha um número de 0 a 8.' e o menu continua.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 9
Opção inválida. Escolha um número de 0 a 8.

[menu]
Escolha uma opção: abc
Opção inválida. Escolha um número de 0 a 8.

[menu]
Escolha uma opção: 
Opção inválida. Escolha um número de 0 a 8.

[menu]
Escolha uma opção: 0
Até logo!
```

## 3. Cadastro com múltiplos registros

**Entrada:** Carregar os 5 exemplos (8), cadastrar o ID 6 com todos os campos e listar (2).

Linhas digitadas: `8 | 1 | 6 | Tarifa Social de Energia | energia | Desconto na conta de luz para famílias de baixa renda | Famílias inscritas no CadÚnico | Distribuidora de energia | luz, energia, desconto | 2 | 0`

**Resultado esperado:** 5 exemplos carregados, ID 6 cadastrado e listagem com 6 registros.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 1
ID (número inteiro): 6
Título: Tarifa Social de Energia
Categoria: energia
Descrição: Desconto na conta de luz para famílias de baixa renda
Público-alvo: Famílias inscritas no CadÚnico
Canal de atendimento: Distribuidora de energia
Palavras-chave separadas por vírgula (opcional): luz, energia, desconto
Registro cadastrado: [6] Tarifa Social de Energia (energia)

[menu]
Escolha uma opção: 2
Total: 6 registro(s)
  [3] Inscrição no Cadastro Único (assistência social)
  [1] Emissão da Carteira de Identidade (documentos)
  [5] Vacinação de rotina (saúde)
  [2] Matrícula na rede pública (educação)
  [4] Atualização cadastral do CadÚnico (assistência social)
  [6] Tarifa Social de Energia (energia)

[menu]
Escolha uma opção: 0
Até logo!
```

## 4. Cadastro com ID duplicado

**Entrada:** Carregar exemplos e tentar cadastrar o ID 1, que já existe.

Linhas digitadas: `8 | 1 | 1 | 0`

**Resultado esperado:** Erro: já existe um registro com o identificador 1.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 1
ID (número inteiro): 1
Erro: já existe um registro com o identificador 1.

[menu]
Escolha uma opção: 0
Até logo!
```

## 5. Cadastro com ID inválido

**Entrada:** Tentar cadastrar com ID 'abc' e depois com ID -5.

Linhas digitadas: `1 | abc | 1 | -5 | 0`

**Resultado esperado:** Duas vezes: Erro: o identificador deve ser um número inteiro positivo.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 1
ID (número inteiro): abc
Erro: o identificador deve ser um número inteiro positivo.

[menu]
Escolha uma opção: 1
ID (número inteiro): -5
Erro: o identificador deve ser um número inteiro positivo.

[menu]
Escolha uma opção: 0
Até logo!
```

## 6. Cadastro com campo obrigatório vazio

**Entrada:** Cadastrar o ID 10 deixando o título só com espaços.

Linhas digitadas: `1 | 10 |     | saúde | desc | todos | UBS | (Enter) | 2 | 0`

**Resultado esperado:** Erro: o campo título é obrigatório. A listagem continua vazia (Total: 0).

**Resultado observado:**

```text
[menu]
Escolha uma opção: 1
ID (número inteiro): 10
Título:    
Categoria: saúde
Descrição: desc
Público-alvo: todos
Canal de atendimento: UBS
Palavras-chave separadas por vírgula (opcional): 
Erro: o campo título é obrigatório.

[menu]
Escolha uma opção: 2
Total: 0 registro(s)
Nenhum registro encontrado.

[menu]
Escolha uma opção: 0
Até logo!
```

## 7. Consulta por ID

**Entrada:** Carregar exemplos e consultar o ID 5, o ID 99 (não existe) e o ID 'x' (inválido).

Linhas digitadas: `8 | 3 | 5 | 3 | 99 | 3 | x | 0`

**Resultado esperado:** Detalhes completos do ID 5; 'Registro não encontrado.' para o 99; erro de identificador para 'x'.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 3
ID: 5
ID: 5
Título: Vacinação de rotina
Categoria: saúde
Descrição: Calendário de vacinas gratuitas para todas as idades.
Público-alvo: Crianças, adultos e idosos
Canal de atendimento: Unidade Básica de Saúde (UBS)

[menu]
Escolha uma opção: 3
ID: 99
Registro não encontrado.

[menu]
Escolha uma opção: 3
ID: x
Erro: o identificador deve ser um número inteiro positivo.

[menu]
Escolha uma opção: 0
Até logo!
```

## 8. Atualização

**Entrada:** Carregar exemplos, atualizar só o título do ID 5 (Enter mantém os outros campos) e tentar atualizar o ID 99.

Linhas digitadas: `8 | 4 | 5 | Campanha de vacinação | (Enter) | (Enter) | (Enter) | (Enter) | 4 | 99 | 0`

**Resultado esperado:** ID 5 com título novo e demais campos iguais; 'Registro não encontrado.' para o 99.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 4
ID do registro a atualizar: 5
Deixe em branco para manter o valor atual.
Título [Vacinação de rotina]: Campanha de vacinação
Categoria [saúde]: 
Descrição [Calendário de vacinas gratuitas para todas as idades.]: 
Público-alvo [Crianças, adultos e idosos]: 
Canal de atendimento [Unidade Básica de Saúde (UBS)]: 
Registro atualizado:
ID: 5
Título: Campanha de vacinação
Categoria: saúde
Descrição: Calendário de vacinas gratuitas para todas as idades.
Público-alvo: Crianças, adultos e idosos
Canal de atendimento: Unidade Básica de Saúde (UBS)

[menu]
Escolha uma opção: 4
ID do registro a atualizar: 99
Registro não encontrado.

[menu]
Escolha uma opção: 0
Até logo!
```

## 9. Exclusão

**Entrada:** Carregar exemplos, excluir o ID 3 (primeiro da lista), tentar excluir de novo e listar.

Linhas digitadas: `8 | 5 | 3 | 5 | 3 | 2 | 0`

**Resultado esperado:** 'Registro excluído.', depois 'Registro não encontrado.', e a listagem com 4 registros sem o ID 3.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 5
ID do registro a excluir: 3
Registro excluído.

[menu]
Escolha uma opção: 5
ID do registro a excluir: 3
Registro não encontrado.

[menu]
Escolha uma opção: 2
Total: 4 registro(s)
  [1] Emissão da Carteira de Identidade (documentos)
  [5] Vacinação de rotina (saúde)
  [2] Matrícula na rede pública (educação)
  [4] Atualização cadastral do CadÚnico (assistência social)

[menu]
Escolha uma opção: 0
Até logo!
```

## 10. Pesquisa por categoria e por título

**Entrada:** Carregar exemplos; categoria 'ASSISTENCIA' (sem acento, maiúsculo); título 'cadúnico'; opção 3 (inválida); título vazio.

Linhas digitadas: `8 | 6 | 2 | ASSISTENCIA | 6 | 1 | cadúnico | 6 | 3 | 6 | 1 | (Enter) | 0`

**Resultado esperado:** IDs 3 e 4 na categoria; ID 4 no título; 'Opção inválida' para 3; erro de termo obrigatório para pesquisa vazia.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 6
Pesquisar por (1) título ou (2) categoria: 2
Termo: ASSISTENCIA
2 resultado(s):
  [3] Inscrição no Cadastro Único (assistência social)
  [4] Atualização cadastral do CadÚnico (assistência social)

[menu]
Escolha uma opção: 6
Pesquisar por (1) título ou (2) categoria: 1
Termo: cadúnico
1 resultado(s):
  [4] Atualização cadastral do CadÚnico (assistência social)

[menu]
Escolha uma opção: 6
Pesquisar por (1) título ou (2) categoria: 3
Opção inválida. Digite 1 ou 2.

[menu]
Escolha uma opção: 6
Pesquisar por (1) título ou (2) categoria: 1
Termo: 
Erro: o termo de pesquisa é obrigatório.

[menu]
Escolha uma opção: 0
Até logo!
```

## 11. Ordenação por ID e por título

**Entrada:** Carregar exemplos (ficam na ordem 3, 1, 5, 2, 4), ordenar por ID, por título e tentar a opção 5.

Linhas digitadas: `8 | 7 | 1 | 7 | 2 | 7 | 5 | 0`

**Resultado esperado:** IDs 1 a 5 em ordem; títulos em ordem alfabética (ignorando acento); 'Opção inválida' para 5.

**Resultado observado:**

```text
[menu]
Escolha uma opção: 8
5 registro(s) de exemplo carregado(s).

[menu]
Escolha uma opção: 7
Ordenar por (1) ID ou (2) título: 1
Lista ordenada:
  [1] Emissão da Carteira de Identidade (documentos)
  [2] Matrícula na rede pública (educação)
  [3] Inscrição no Cadastro Único (assistência social)
  [4] Atualização cadastral do CadÚnico (assistência social)
  [5] Vacinação de rotina (saúde)

[menu]
Escolha uma opção: 7
Ordenar por (1) ID ou (2) título: 2
Lista ordenada:
  [4] Atualização cadastral do CadÚnico (assistência social)
  [1] Emissão da Carteira de Identidade (documentos)
  [3] Inscrição no Cadastro Único (assistência social)
  [2] Matrícula na rede pública (educação)
  [5] Vacinação de rotina (saúde)

[menu]
Escolha uma opção: 7
Ordenar por (1) ID ou (2) título: 5
Opção inválida. Digite 1 ou 2.

[menu]
Escolha uma opção: 0
Até logo!
```
