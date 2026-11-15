# DSA: Citizen Assist AI (CadU)

Entrega de Estruturas de Dados e Algoritmos da Global Solution 2026.2, em Python puro, sem bibliotecas externas.

## Objetivo

Sistema de terminal para gerenciar e consultar serviços e orientações ao cidadão (documentos, assistência social, educação, saúde etc.). Os registros ficam guardados numa **lista encadeada feita pela equipe**, e a busca e a ordenação também foram escritas no código, sem `sorted()`, `list.sort()` nem listas nativas para guardar os dados.

## Como executar

Precisa só do Python 3.12. Na raiz do repositório:

```bash
py -3.12 dsa/main.py
```

Testes automáticos (20 testes com `unittest`):

```bash
py -3.12 -m unittest discover -s dsa/testes -v
```

Gerar de novo as evidências (`EVIDENCIAS.md`):

```bash
py -3.12 dsa/testes/gerar_evidencias.py
```

## Instruções de uso

O menu mostra as opções de 0 a 8. Para testar rápido, escolha **8** (carrega 5 registros fictícios) e depois use as outras opções.

- 1, Cadastrar: pede ID, título, categoria, descrição, público-alvo, canal e palavras-chave (opcional).
- 2, Listar: mostra todos os registros na ordem atual da lista.
- 3, Consultar: mostra todos os campos de um ID.
- 4, Atualizar: mostra o valor atual de cada campo; Enter mantém o valor.
- 5, Excluir: remove pelo ID.
- 6, Pesquisar: por trecho do título ou da categoria, ignorando acento e maiúscula.
- 7, Ordenar: por ID ou por título (em ordem alfabética).
- 8, Carregar dados de exemplo.
- 0, Sair.

Entradas inválidas não derrubam o programa: opção inexistente, ID que não é número inteiro positivo, ID repetido, campo obrigatório vazio e registro não encontrado mostram uma mensagem clara e voltam ao menu.

## Campos do registro

Classe `Servico` em `crud.py`:

- `id`: identificador único, número inteiro positivo.
- `titulo`, `categoria`, `descricao`, `publico_alvo`, `canal`: textos obrigatórios (não podem ficar vazios).
- `palavras_chave`: opcional, usado só no ranqueamento para o assistente do CadU.

## Organização do código

- `lista_ligada.py`: classes `No` e `ListaLigada` (a estrutura principal) e `HistoricoPerguntas` (extra para o assistente).
- `ordenacao.py`: merge sort que ordena a própria lista encadeada.
- `crud.py`: `Servico`, validações e `RepositorioServicos` (cadastrar, listar, consultar, atualizar, excluir, pesquisar, ordenar e ranquear). Não faz `input`/`print`.
- `main.py`: o menu interativo. Só conversa com o usuário e chama o `crud.py`.
- `dados_exemplo.py`: registros fictícios.
- `testes/test_dsa.py`: testes automáticos.
- `testes/gerar_evidencias.py`: roda o menu com entradas prontas e grava `EVIDENCIAS.md`.

Separar regras (`crud.py`) de interface (`main.py`) permite testar as regras sem digitar nada e reaproveitar o repositório no assistente depois.

## A lista encadeada

Cada registro fica dentro de um nó (`No`), que guarda o valor e uma referência para o próximo nó. A lista guarda:

- `cabeca`: o primeiro nó;
- `cauda`: o último nó (permite inserir no fim sem percorrer);
- `_tamanho`: um contador (permite saber o tamanho sem percorrer).

Operações principais:

- **Inserção** (`adicionar_fim`): o último nó passa a apontar para o novo, e a cauda passa a ser o novo.
- **Percurso** (`__iter__`): começa na cabeça e segue `proximo` até chegar em `None`. É o que permite usar `for registro in lista`.
- **Atualização**: acha o nó pela busca e troca os campos do registro guardado nele.
- **Remoção** (`remover_se`): anda com dois ponteiros, `anterior` e `atual`. Ao achar o nó, faz `anterior.proximo = atual.proximo`, e o nó sai da corrente. Casos especiais: se era a cabeça, a cabeça passa a ser o segundo nó; se era a cauda, a cauda passa a ser o anterior. Em Python não é preciso liberar memória à mão: o nó sem nenhuma referência é recolhido sozinho pelo coletor de lixo.

## Busca

**Busca linear (sequencial).** Começa na cabeça e compara nó por nó até achar ou chegar no fim. É usada para consultar por ID e para pesquisar por título ou categoria (aqui vai até o fim, porque pode haver vários resultados, que vão para uma nova lista encadeada).

Por que linear e não binária? A busca binária precisa pular direto para o meio, e na lista encadeada chegar ao meio já custa O(n). Então, em lista encadeada, a busca linear é a escolha natural.

## Ordenação

**Merge sort direto na lista encadeada** (`ordenacao.py`):

1. Dividir: acha o meio com dois ponteiros (o lento anda 1 nó, o rápido anda 2; quando o rápido chega no fim, o lento está no meio) e corta a ligação.
2. Ordenar cada metade do mesmo jeito (recursão), até sobrar 0 ou 1 nó.
3. Intercalar: junta as duas metades ordenadas, sempre pegando o menor dos dois primeiros nós e religando os ponteiros.

Por que merge sort? Não precisa de acesso por índice (só anda para frente), não cria nós novos (só religa ponteiros), custa O(n log n) até no pior caso e é estável (em empate, mantém a ordem original). O insertion sort seria mais curto, mas custa O(n²) no pior caso.

A ordenação por título usa o texto sem acento e em minúsculas, para "Água" não ir para depois do "Z".

## Análise Big-O

Hipóteses: n é o número de registros na lista; a lista só tem ligação para frente; não há índice auxiliar (como um dicionário por ID), então achar um registro pede percorrer a lista. Textos (título, categoria) são curtos e tratados como custo constante.

- **Inserção no fim (estrutura): O(1).** Graças à referência para a cauda.
- **Cadastrar (operação completa): O(n).** Antes de inserir, a busca linear confere se o ID já existe. A inserção em si é O(1).
- **Listar (percurso): O(n).** Passa por todos os nós.
- **Consultar por ID: O(n) no pior caso.** Busca linear: o ID pode estar no fim ou não existir. Melhor caso O(1), se estiver na cabeça.
- **Pesquisar por título ou categoria: O(n).** Sempre passa por todos, porque pode haver vários resultados.
- **Atualizar: O(n).** O custo é achar o registro; trocar os campos é O(1).
- **Excluir: O(n).** O custo é achar o nó e o anterior; religar o ponteiro é O(1).
- **Ordenar (merge sort): O(n log n) em qualquer caso.** A lista é dividida ao meio log n vezes, e em cada nível a intercalação passa por n nós. Achar o meio também custa O(n) por nível, o que não muda o total. Memória extra: O(log n), só da pilha de recursão, porque nenhum nó é copiado. Ao fim, achar a nova cauda custa mais O(n).

Extras para o assistente do CadU:

- **Histórico de perguntas:** registrar é O(1) enquanto cabe; quando passa da capacidade, remover a mais antiga do fim é O(n) (é preciso achar o penúltimo nó).
- **Ranquear:** O(n·p) para pontuar (p é o número de palavras da pergunta) mais O(n log n) para ordenar pela pontuação.

## Testes e evidências

- `testes/test_dsa.py`: 20 testes automáticos da lista, do merge sort (inclusive 200 listas aleatórias comparadas com o `sorted()` do Python, usado só para conferir), do CRUD, das validações e das operações com a lista vazia.
- `EVIDENCIAS.md`: 11 cenários rodados no menu de verdade, cada um com entrada, resultado esperado e resultado observado (saída do terminal). Inclui cadastro com múltiplos registros, consulta, atualização, exclusão, pesquisa, ordenação, entradas inválidas e operações com a lista vazia.
