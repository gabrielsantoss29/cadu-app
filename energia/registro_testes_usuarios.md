# SERS — Registro de testes de usuários

**Data:** 16 e 17/11/2026    **Versão testada:** aba Energia do CadU (app web) e assistente de conversa

Três pessoas de fora da equipe (U1, U2 e U3) usaram o app sem ajuda, uma situação cada. Não foi registrado CPF, telefone, e-mail, nome ou qualquer outro identificador pessoal.

| Teste | Situação proposta | Resultado esperado | O que o usuário compreendeu? | Comentário recebido (anônimo) | Ajuste realizado | Reteste |
|---|---|---|---|---|---|---|
| U1 | Calcular consumo: marcar o chuveiro elétrico e ver o resultado | kWh e limitações claros | Entendeu que o resultado é uma estimativa do mês (54 kWh) e que o custo depende do preço do kWh que ela pode mudar. | "O que é kWh? Na minha conta só aparece esse número." | Incluída, no cartão de resultado, a frase "kWh é a unidade de energia que aparece na sua conta de luz." | Sim: a frase aparece abaixo do total; a pessoa disse que agora ficou claro. |
| U2 | Comparar banho curto e solar térmico (botão Comparar) | Entender as diferenças e a fonte renovável | Entendeu os três valores (55; 27,5 e 16,5 kWh por mês) e que o solar depende de instalação e orçamento e que os 70% são uma suposição. | "O banho curto é de graça, mas o solar economiza mais." | Nenhum: o aviso em amarelo e as fontes já estavam claros. | Não foi necessário. |
| U3 | Perguntar no assistente sobre custo e retorno do aquecedor solar sem informar dados | Não inventar valores nem prometer economia | Entendeu que o assistente não tem preço nem prazo de retorno e que é preciso pedir orçamento. | "Gostei que ele não inventou um preço." | Nenhum. | Não foi necessário. |

**Síntese dos ajustes implementados:** um ajuste, vindo do U1: explicação do que é kWh no cartão de resultado da aba Energia (`app/templates/energia.html`).

**Evidência da integração no assistente:** a aba Energia chama `comparar_banho` do módulo `calculo_energia.py` pela rota `/api/energia/comparar` (`app/app.py`), e o assistente de conversa responde "Não encontrei uma orientação para isso e não vou inventar" quando a pergunta pede preço ou retorno sem dados. Os testes automáticos do módulo (`energia/testes_sers.py`) passam.
