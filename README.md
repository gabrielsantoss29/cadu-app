# CadU

Aplicativo web gratuito, em linguagem simples, que ajuda famílias do CadÚnico (ou que querem entrar) a entender benefícios, prazos e o que fazer em cada situação. Projeto da Global Solution 2026.2 (CitizenTech), FIAP.

O CadU **não é um canal oficial** do governo e **não pede dados pessoais**.

## Estrutura

- `app/`: aplicativo web (telas, triagem, mapa, voz).
- `assistente/`: assistente virtual em Python (chatbot por regras) com versão de terminal. Entrega do PCP.
- `dados/`: base de conhecimento em JSON, com fonte oficial e data de verificação.
- `dsa/`: entrega de Estruturas de Dados e Algoritmos.
- `cs/`: entrega de Computer Science (lógica booleana).
- `energia/`: dados e cálculos do tema energia.
- `docs/`: documentação.

Cada pasta de entrega terá um README próprio explicando como executar.

## Contribuição de SERS (Soluções em Energias Renováveis e Sustentáveis)

Pasta `energia/`. Faz parte do assistente CadU (aba **Energia** do app).

**Integrantes:** Gabriel de Almeida Santos (RM 569395), Guilherme Henrique Garbelini Alberto (RM 571150), Hebert Soares de Jesus (RM 571507).

**Público e problema:** famílias de baixa renda que querem entender o consumo de energia e gastar menos na conta de luz, sem depender de termos técnicos.

**Funcionalidades de energia:**
- calculadora de consumo por aparelho (potência × horas × dias), com preço do kWh opcional;
- comparação de duas alternativas para a mesma necessidade, banho quente: banho mais curto e aquecimento solar térmico (fonte renovável), com consumo, economia e limitações;
- comparação com a média de consumo residencial da região (dados abertos da EPE);
- dicas de economia.

**Como executar e testar:**
```bash
cd energia
python calculo_energia.py
python integracao_cadu.py
python testes_sers.py
```
O app usa este mesmo código: o arquivo `app/app.py` chama `comparar_banho` em `/api/energia/comparar`.

**Documentos:** `energia/comparacao_alternativas_SERS.md` (cálculos, custos, viabilidade, impacto ambiental e referências), `energia/energia.json` (dados, origem e premissas), `energia/registro_testes_usuarios.md` (testes com usuários e ajustes).
