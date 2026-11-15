# O que falta (atualizado em 15/11/2026)

Prazo no Portal: 19/11, 23h59. Meta do grupo: fechar tudo até 17/11.

## 1. Ligar o banco (Neon): passo a passo

1. Entre em https://console.neon.tech, abra o projeto `my-first-project` e clique no botão verde **Connect** (esquerda).
2. Copie a *connection string* (começa com `postgresql://`). Ela é uma senha: não mande no chat, não coloque em arquivo do repositório.
3. No app do Claude, abra o painel **Terminal** e a aba que ficou aberta (chamada "vercel login"). Ela está parada numa pergunta do comando `vercel env add DATABASE_URL`.
   - Escolha **Secret** (Enter).
   - Cole a connection string quando pedir o valor (Enter).
   - Escolha o ambiente **Production** (espaço para marcar, Enter).
   - Se a aba sumiu: abra um terminal na pasta do projeto e rode `& 'C:\Users\gabri\AppData\Roaming\npm\vercel.cmd' env add DATABASE_URL production`.
4. Avise o Claude para republicar o app (ou rode `& 'C:\Users\gabri\AppData\Roaming\npm\vercel.cmd' deploy --prod --yes`).
5. Para conferir: abra https://cadu-app.vercel.app/api/contadores. Depois de usar o app, deve aparecer `"ativo": true` e os números.

Os contadores guardam só números (triagens feitas, assuntos consultados, "ajudou" e "não ajudou"). Nunca guardam texto digitado nem IP.

## 2. Testes com pessoas de fora (PCP e pessoa 3)

- O teste que vale para o PCP é no **assistente de terminal** (`cadu-assistente`): 3 ou mais pessoas de fora, 10 ou mais atendimentos no total. Os indicadores saem do menu 3 e vão no README. Não anotar nomes.
- O app web (link da Vercel) pode ser mandado para mais gente. O banco só tem contadores; para a pessoa 3 usar, abrir `/api/contadores` e copiar os números.

## 3. Entregas

- **PCP:** vídeo técnico de 5 a 8 minutos (todos falam, sem voz de IA), link no README e arquivo `.txt` no Portal (nome do assistente, público, integrantes e RM, link do GitHub, link do vídeo).
- **DSA:** pasta `dsa/` (código, README, `EVIDENCIAS.md` com saídas do terminal).
- **Computer Science:** a pessoa 2 faz a lógica à mão (sem IA) e o relatório em PDF com prints do simulador.
- **Pessoa 3:** Prompt e IA e Modelagem Matemática.
