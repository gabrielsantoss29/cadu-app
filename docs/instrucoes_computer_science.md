# Instruções: Computer Science (GS 2026.2), para quem vai fazer a parte lógica

Contexto: o grupo faz o CadU, um app gratuito em linguagem simples para famílias do CadÚnico (explica benefícios, prazos e o que fazer quando algo bloqueia). Não é canal oficial e não pede dados pessoais. Na Global Solution, cada matéria entrega uma parte do mesmo projeto. A de Computer Science é o **módulo de decisão lógica**: uma regra com 3 ou 4 variáveis (0 ou 1) que decide qual orientação o assistente mostra.

## O que já está pronto (não precisa fazer)

- O programa em Python que roda a regra: `cs/assistente.py` (pergunta as variáveis, recusa entrada inválida, mostra a orientação, avisa que não é canal oficial) e `cs/verificador.py` (testa todas as combinações e compara a regra original com a simplificada).
- Os testes automáticos.
- Tudo está no repositório `cadu-app`, pasta `cs/`. O arquivo `cs/expressoes.py` tem só um EXEMPLO no lugar da regra de verdade.

## REGRA IMPORTANTE (nota)

O enunciado **proíbe usar inteligência artificial** para fazer a tabela-verdade, o mapa de Karnaugh e o circuito lógico. Se usar, **perde 4 pontos da nota total**. IA só pode ajudar no texto do relatório final. Então: faça essas partes à mão (papel, planilha ou o simulador) e entenda cada passo, porque o professor pode perguntar.

## O que precisa ser feito (na ordem do enunciado)

1. Escolher uma situação de atendimento do CadU e 3 ou 4 variáveis booleanas com significado claro para 0 e 1. Exemplo de ideia (troque pela de vocês): A = família já está no CadÚnico; B = cadastro atualizado nos últimos 2 anos; C = recebe algum benefício. Saída = qual orientação mostrar (por exemplo, "atualizar o cadastro no CRAS" ou "está em dia").
2. Construir a **tabela-verdade completa** (todas as combinações, com a saída de cada uma).
3. Escrever a expressão da saída em **forma canônica** (soma de mintermos ou produto de maxtermos).
4. **Simplificar por álgebra booleana**, dizendo qual propriedade usou em cada passo. Mostrar uma transformação com De Morgan, só se for necessário.
5. Simplificar de novo com **mapa de Karnaugh**, indicando os agrupamentos, e comparar com o resultado da álgebra (têm que dar equivalentes).
6. Desenhar o **circuito lógico original e o simplificado** no simulador (logic.ly/demo ou logiccircuit.org) e comparar a quantidade de portas.
7. Colocar a regra no programa: abrir `cs/expressoes.py`, editar só entre "COMECE A EDITAR" e "TERMINE DE EDITAR" (nomes das variáveis, perguntas, expressão original e simplificada, texto da orientação, fontes com data de consulta) e mudar `EXEMPLO = True` para `False`.
8. Rodar `py -3.12 verificador.py` dentro de `cs/` e conferir que todas as combinações dão IGUAL.

As orientações precisam ter **fonte verificável e data de consulta** (por exemplo, gov.br/mds). Não inventar regra.

## Entregáveis

- **Relatório técnico em PDF** com: descrição do problema, variáveis, regras e referências, tabela-verdade, expressões, etapas de simplificação, mapa de Karnaugh, circuitos e resultados dos testes.
- **Prints da simulação** (o circuito no simulador e o programa rodando).
- Instruções de execução (já estão em `cs/README.md`).
- Entrega no portal da FIAP até **19/11, 23h59** (o grupo combina quem envia). Meta interna: terça, 17/11.

Dúvida de formato (o que o professor aceita como arquivo único ou zip): confirmar com o professor.
