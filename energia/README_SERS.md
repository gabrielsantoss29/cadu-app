# Cadu — Módulo Energia | SERS — Global Solution 2026.2

**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (1CC)  
**Público:** famílias que buscam entender o consumo residencial e orientações sociais em linguagem acessível.

## Objetivo
Ajudar o usuário a estimar consumo elétrico, comparar duas alternativas para aquecimento de água no banho e obter dicas de uso consciente de energia, com premissas e referências verificáveis. O Cadu **não é canal oficial**, não pede CPF e não atesta elegibilidade a benefícios.

## Arquivos
- `energia.json`: exemplos de aparelhos, premissas, orientações e referências.
- `calculo_energia.py`: estimativa de kWh e comparação dos cenários.
- `integracao_cadu.py`: interface `responder_energia(acao, parametros)` com saída em linguagem simples.
- `comparacao_alternativas_SERS.md`: comparação fundamentada, custos e limitações.
- `testes_sers.py`: testes automáticos.
- `registro_testes_usuarios.md`: formulário a preencher **após** testes reais.

## Execução (Python 3.10+; sem bibliotecas de terceiros)
```bash
python calculo_energia.py
python integracao_cadu.py
python testes_sers.py
```
No assistente do Gabriel, importar `responder_energia` de `integracao_cadu.py`; disponibilizar as ações `consumo`, `comparar` e `dicas`. O Cadu pode passar parâmetros para simulação; exemplo: `responder_energia('comparar', {'potencia_w':5500, 'horas_base_dia':1/3, 'horas_reduzidas_dia':1/6, 'dias_mes':30, 'fracao_substituida_solar':0.7})`.

## Comparação de alternativas
**Necessidade:** água quente para banho durante 30 dias. Base: 5.500 W × 20 min/dia × 30 dias = **55,0 kWh/mês**. Banho com metade da duração: **27,5 kWh/mês**. Solar térmico substituindo hipoteticamente 70% da eletricidade de aquecimento, com a mesma duração base: **16,5 kWh/mês** para apoio elétrico.

A opção de banho curto reduz o tempo do serviço, diferente da proposta solar. O valor de 70% é uma **hipótese de simulação**, não garantia de desempenho. O custo de instalação solar **não foi cotado**; não existe preço de mercado ou retorno do investimento validado neste projeto. Pode-se informar a tarifa de um usuário para estimar economia elétrica, sem confundir com a fatura total.

## Dados e referências
O cálculo usa potência, tempo e dias de uso; não requer dados pessoais. Valores dos equipamentos são cenários ilustrativos, não medições. O arquivo `energia.json` identifica as fontes técnicas e a base da EPE. Leia a análise completa em `comparacao_alternativas_SERS.md`.

## Evidências de integração e testes ainda necessárias
1. Com o Gabriel, integrar estas funções ao fluxo do Cadu e testar perguntas completas.
2. Registrar testes de compreensão e utilidade com pessoas externas, sem dados pessoais.
3. Documentar correções feitas após comentários e incluir capturas ou transcrição anônima.
4. Gravar vídeo técnico **não listado** de até **3 minutos** demonstrando os recursos e limitações.
5. Publicar o conteúdo no GitHub, identificado como contribuição SERS, e enviar ao Portal **apenas um `.txt`** com nomes/RMs e links do repositório e do vídeo.

## Equipe (conferir grafia antes de submeter)
- Guilherme Henrique Garbelini Alberto — RM 571150
- Hebert Soares de Jesus — RM 571507
- Gabriel de Almeida Santos — RM 569395
