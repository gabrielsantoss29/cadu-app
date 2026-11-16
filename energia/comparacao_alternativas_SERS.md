# Global Solution 2026.2 | SERS — Cadu
## Comparação técnica e econômica: aquecimento de água para banho

**Público:** famílias que desejam compreender e reduzir o uso de energia elétrica, inclusive usuários que buscam informações sobre o CadÚnico. O simulador **não** solicita nem verifica renda, CPF ou elegibilidade à Tarifa Social.

**Necessidade comum às alternativas:** fornecer água aquecida para o banho durante 30 dias. As alternativas são (1) reduzir o tempo de banho com o chuveiro elétrico existente e (2) instalar aquecimento solar **térmico**, mantendo apoio elétrico quando necessário. A segunda usa energia renovável (radiação solar convertida em calor), e não painéis solares fotovoltaicos.

### 1. Premissas transparentes (cenário didático, NÃO medição domiciliar)

- Potência elétrica do chuveiro: **5.500 W = 5,5 kW**, na regulagem simulada.
- Uso-base da residência: **20 minutos totais por dia** = 1/3 hora/dia.
- Alternativa A: **10 minutos totais por dia** = 1/6 hora/dia.
- Alternativa B: manter 20 minutos de banho e supor que o solar térmico substitui **70%** da energia elétrica usada para aquecer a água. **70% é hipótese de cenário, não taxa garantida.**
- Período: **30 dias**; funcionamento e potência considerados constantes somente para fins de comparação.
- Preço: ilustrar a fórmula com **R$ 0,90/kWh como valor hipotético, NÃO tarifa oficial nem preço médio de mercado**; a implementação pode receber a tarifa efetiva informada pelo usuário.
- Não se consideram água, energia de bombas, perdas do reservatório, variações de temperatura, tarifas progressivas, impostos, iluminação pública, bandeiras ou tarifa social. Valores de fatura podem divergir.

**Equação:** E(kWh/mês) = Potência(W) / 1000 × horas de uso por dia × dias por mês.

### 2. Resultado lado a lado (mesma necessidade / mesmo período)

| Indicador | Chuveiro convencional (referência) | A — banho mais curto | B — solar térmico (hipótese 70%) |
|---|---:|---:|---:|
| Tempo de banho total ao dia | 20 min | 10 min | 20 min |
| Eletricidade calculada para aquecimento | 55,0 kWh/mês | 27,5 kWh/mês | 16,5 kWh/mês |
| Eletricidade economizada vs. referência | — | 27,5 kWh/mês | 38,5 kWh/mês |
| Redução relativa de eletricidade de aquecimento | — | 50% | 70% |
| Custo energético parcial a **R$ 0,90/kWh hipotéticos** | R$ 49,50/mês | R$ 24,75/mês | R$ 14,85/mês |
| Economia energética ilustrativa vs. referência | — | R$ 24,75/mês | R$ 34,65/mês |
| Economia elétrica anual se cenário constante | — | 330 kWh/ano | 462 kWh/ano |
| Investimento inicial | Equipamento existente | R$ 0 adicional no cenário | **Solicitar orçamento local** de coletor, reservatório, instalação e eventuais adaptações |
| Custos recorrentes | Fatura e manutenção do chuveiro | Fatura e manutenção do chuveiro | Energia de apoio, inspeção e manutenção de coletor/reservatório |
| Viabilidade | Disponibilidade elétrica/hidráulica | Alta quando a redução de tempo for possível | Depende de propriedade/autorizações, cobertura, sombreamento, clima, instalação e recursos financeiros |
| Impacto ambiental | Consumo elétrico de referência | Reduz demanda elétrica e tende a reduzir uso de água | Substitui parte da eletricidade pelo calor solar; fabricação, instalação e manutenção também têm impactos |

**Atenção à comparabilidade:** diminuir o tempo do banho significa menor duração do serviço, enquanto o solar térmico busca preservar a duração. Portanto, ambas atendem ao propósito de banho com água quente, mas **não entregam conforto/tempo idênticos**. A diferença deve ser explicitada ao usuário. Se a exigência for preservar estritamente o mesmo tempo de banho, comparar solar térmico a outra tecnologia de aquecimento eficiente, com parâmetros justificados.

### 3. Como apresentar custos e retorno sem inventar preços

- **A — banho mais curto:** nenhum equipamento adicional é pressuposto. Economia financeira estimada = kWh economizados × tarifa variável informada. Alterações de hábitos têm baixo custo inicial, mas exigem adesão contínua.
- **B — solar térmico:** custo inicial não foi medido nesta atividade. O relatório deve registrar **orçamento real com data, cidade, capacidade, instalação incluída ou não** antes de apresentar preço em reais. Para análise posterior: retorno simples (meses) = investimento instalado ÷ economia elétrica mensal, ajustando quando possível custos adicionais e manutenção. Sem orçamento, **não publicar prazo de retorno como resultado**.
- **Exemplo hipotético de cálculo**, apenas para ensinar, usando investimento arbitrário de R$ 4.000 e a tarifa *hipotética* acima: 4.000 ÷ 34,65 ≈ **115,4 meses (9,6 anos)**, ignorando manutenção, degradação, inflação, juros e substituição de peças. **R$ 4.000 não é cotação verificada e não deve ser mostrado como preço de mercado.**

### 4. Orientações de linguagem acessível para o Cadu

**Pergunta: “Quanto meu chuveiro gasta?”**
“Vamos fazer uma estimativa. Um chuveiro de 5.500 watts, usado por 20 minutos por dia, pode gastar perto de 55 kWh no mês. O valor real muda conforme a potência, o tempo e a regulagem. Veja a etiqueta do seu chuveiro.”

**Pergunta: “Como economizar no banho?”**
“Se o tempo total de banho cair de 20 para 10 minutos por dia, neste exemplo o uso de energia do chuveiro cai de 55 para 27,5 kWh por mês. Isso é uma simulação, não uma promessa de redução da conta.”

**Pergunta: “Vale a pena aquecedor solar?”**
“O aquecedor solar usa o calor do sol para aquecer a água. Neste exemplo, se ele substituir 70% da eletricidade usada no banho, o consumo cairia de 55 para 16,5 kWh no mês. Antes de comprar, é importante conferir se a casa permite instalação e pedir orçamento. A economia depende do sol e do equipamento.”

**Pergunta: “Qual alternativa é melhor?”**
“Para começar sem comprar equipamento, reduzir o tempo de banho pode ser mais viável. O aquecimento solar pode economizar mais eletricidade neste exemplo, mas exige investimento e instalação. As duas opções têm vantagens e limites.”

### 5. Integração funcional necessária

1. Cadu mostra a opção **Energia** e permite selecionar `Calcular consumo`, `Comparar alternativas` ou `Dicas de economia`.
2. `calculo_energia.py`: importar `carregar_energia`, `calcular_consumo_mensal` e `comparar_banho`. Carregar o JSON sem duplicar a base do assistente.
3. Para cálculo: pedir somente potência, tempo, dias e quantidade; tarifa de energia é **opcional**. Se não houver tarifa, mostrar só kWh, não inventar valor em R$.
4. Para comparação: usar a mesma potência e período nas alternativas. Informar claramente que a fração solar é uma **hipótese ajustável**.
5. Retornar texto simples com **fonte oficial e data**, além de aviso de limitação. Nunca solicitar CPF, telefone, número de benefício ou endereço.
6. Registrar evidência de teste com perguntas, resultado esperado, resposta observada, comentário do usuário e ajuste implementado, sem dados pessoais.

### 6. Verificações antes de gravar o vídeo

- Resultado-base = 55,0; tempo reduzido = 27,5; solar = 16,5 kWh/mês.
- Cenário com tarifa não informada **não** deve apresentar economia em reais.
- Potência negativa, tempo negativo ou fração solar fora de 0–1 deve gerar erro controlado.
- Cadu não deve afirmar que a instalação solar custa R$ 4.000 nem garantir retorno financeiro.
- Confirmar que o fluxo do assistente chama o módulo real e apresenta fonte e limitação, não apenas prints de análise separados.

### 7. Fontes utilizadas

- Ministério de Minas e Energia (2026), “Potência e consumo de energia: o que são e como impactam na conta de luz”: https://www.gov.br/mme/pt-br/assuntos/noticias/potencia-e-consumo-de-energia-o-que-sao-e-como-impactam-na-conta-de-luz
- ANEEL, “Aprenda a calcular o consumo de seu aparelho e economize energia”: https://www2.aneel.gov.br/aplicacoes_liferay/noticias_area/arquivo.cfm?idAreaNoticia=1&idNoticia=4101&tipo=PDF
- ProjetEEE/MME, “Equipamentos Solares — Sistema de Aquecimento Solar de Água”: https://projeteee.mme.gov.br/equipamento/equipamentos-solares-sistema-de-aquecimento-solar-de-agua/
- U.S. Department of Energy, manutenção de sistemas solares térmicos: https://www.energy.gov/cmei/femp/equipment-operations-and-maintenance-summaries
- EPE, dados abertos de consumo mensal: https://www.epe.gov.br/pt/publicacoes-dados-abertos/dados-abertos/dados-do-consumo-mensal-de-energia-eletrica

**Estado do material:** comparação técnica pronta como cenário educativo; **pendente** de orçamento real para afirmar custo de instalação e prazo de retorno, integração ao assistente Gabriel e testes com usuários reais.
