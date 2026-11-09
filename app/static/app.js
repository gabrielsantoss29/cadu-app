// Funções comuns a todas as páginas do CadU.
const CadU = {
  CHAVE: "cadu_perfil",

  // localStorage pode falhar (aba anônima, bloqueio): sempre dentro de try/catch.
  lerPerfil() {
    try { return JSON.parse(localStorage.getItem(this.CHAVE)) || {}; } catch (e) { return {}; }
  },
  salvarPerfil(p) {
    try { localStorage.setItem(this.CHAVE, JSON.stringify(p)); } catch (e) { /* sem armazenamento: segue sem salvar */ }
  },
  apagarDados() {
    try { localStorage.removeItem(this.CHAVE); } catch (e) { /* nada a fazer */ }
  },

  // Botão "Ouvir": lê o texto em voz alta com a voz do navegador
  // (provisório; a voz própria do CadU virá depois).
  ouvir(texto) {
    if (!("speechSynthesis" in window)) { alert("Seu aparelho não tem leitura em voz alta."); return; }
    speechSynthesis.cancel();
    const fala = new SpeechSynthesisUtterance(texto);
    fala.lang = "pt-BR";
    fala.rate = 0.95;
    speechSynthesis.speak(fala);
  },

  // Ícones para o JavaScript (texto FIXO do código, nunca vem do usuário).
  ICONES: {
    ouvir: '<path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a10 10 0 0 1 0 14"/>',
    check: '<path d="M20 6 9 17l-5-5"/>',
    x: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    alerta: '<path d="m21.7 18-8-14a2 2 0 0 0-3.5 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    link: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    telefone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
  },
  icone(nome, classe) {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    svg.setAttribute("stroke-linejoin", "round");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("class", (classe || "h-6 w-6") + " shrink-0");
    svg.innerHTML = this.ICONES[nome] || "";
    return svg;
  },

  // Cria um elemento com classes e texto (o texto entra com textContent: HTML não é interpretado).
  el(tag, classe, texto) {
    const e = document.createElement(tag);
    if (classe) e.className = classe;
    if (texto !== undefined && texto !== null) e.textContent = texto;
    return e;
  },
};

// Qualquer botão com data-ouvir="#id" lê o texto daquele elemento.
document.addEventListener("click", function (e) {
  const botao = e.target.closest("[data-ouvir]");
  if (!botao) return;
  const alvo = document.querySelector(botao.dataset.ouvir);
  if (alvo) CadU.ouvir(alvo.textContent.replace(/\s+/g, " ").trim());
});
