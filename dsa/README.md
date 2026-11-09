# DSA: Estruturas de Dados e Algoritmos

Parte do CadU feita só com Python puro (sem bibliotecas externas). Ela é independente do assistente e pode ser ligada a ele depois:

- a **lista ligada** guarda o histórico das últimas perguntas e a base de orientações;
- a **ordenação própria** ranqueia as orientações pela pontuação de cada pergunta.

## Como executar

Na raiz do repositório:

```bash
py -3.12 dsa/main.py
```

```bash
py -3.12 -m unittest discover -s dsa/testes -v
```

## Arquivos

- `lista_ligada.py`: classes `No`, `ListaLigada` e `HistoricoPerguntas`. Não usa `list` para guardar os dados.
- `ordenacao.py`: `merge_sort`, escrito do zero (sem `sorted()` nem `list.sort()`).
- `crud.py`: `Orientacao` e `RepositorioOrientacoes` (criar, listar, buscar, atualizar, remover e ranquear), guardando tudo na lista ligada.
- `main.py`: demonstração no terminal.
- `testes/test_dsa.py`: 17 testes automáticos (`unittest`).

## Como funciona

**Lista ligada.** Cada valor fica num nó, e cada nó aponta para o próximo. A lista guarda a cabeça (primeiro nó) e a cauda (último nó). Ter a cauda deixa inserir no fim sem percorrer a lista.

**Merge sort.** Divide a lista ao meio até sobrar 0 ou 1 item (que já está ordenado), depois junta as metades olhando sempre o menor (ou maior) item de cada lado. Escolhi porque é fácil de explicar, tem custo garantido de n log n e é estável: em caso de empate de pontos, a ordem original é mantida.

**Ranqueamento.** Cada palavra da pergunta vale 2 pontos se está nas palavras-chave da orientação e 1 ponto se está só no título (ignorando acento e maiúscula). Orientações com 0 ponto saem, e o resto é ordenado do maior para o menor.

**Histórico.** A pergunta nova entra na frente da lista. Passou da capacidade, a mais antiga (do fim) é descartada.

## Big-O de cada operação

Aqui, n é o número de itens na lista e p é o número de palavras da pergunta.

Lista ligada:

- adicionar no início: O(1), só troca a cabeça.
- adicionar no fim: O(1), usa a cauda.
- remover do início: O(1).
- remover do fim: O(n), porque é preciso percorrer até achar o penúltimo nó (a lista só aponta para frente).
- buscar, substituir ou remover por condição: O(n) no pior caso, pois pode ser preciso passar por todos os nós.
- tamanho (`len`): O(1), há um contador.

CRUD de orientações:

- criar: O(n), porque confere se o id já existe (a inserção em si é O(1)).
- listar: O(n).
- buscar por id ou por categoria: O(n).
- atualizar: O(n), o custo é achar o item.
- remover: O(n), o custo é achar o item.
- ranquear: O(n·p) para pontuar mais O(n log n) para ordenar. Como p é pequeno (palavras de uma frase), o que domina é o n log n.

Histórico:

- registrar: O(1) enquanto cabe; O(n) quando precisa descartar a mais antiga, pois remover do fim é O(n). Como a capacidade é pequena (10), na prática é barato.
- listar recentes: O(n).

Merge sort:

- tempo: O(n log n) em qualquer caso (melhor, médio e pior). A lista é dividida log n vezes e cada nível custa n para juntar.
- memória extra: O(n), pois cria listas auxiliares.
- comparação: o insertion sort é mais simples, mas custa O(n²) no pior caso.

## Observações

- O `merge_sort` recebe e devolve uma `list` do Python como espaço de trabalho temporário. O armazenamento dos dados (orientações e histórico) é todo na lista ligada própria.
- Os testes usam `sorted()` apenas para conferir se o resultado do merge sort está certo.
