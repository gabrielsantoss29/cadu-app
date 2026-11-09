// Funções comuns a todas as páginas.
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

  // Botão "Ouvir": lê o texto em voz alta com a voz do navegador (placeholder; voz melhor virá depois).
  ouvir(texto) {
    if (!("speechSynthesis" in window)) { alert("Seu aparelho não tem leitura em voz alta."); return; }
    speechSynthesis.cancel();
    const fala = new SpeechSynthesisUtterance(texto);
    fala.lang = "pt-BR";
    speechSynthesis.speak(fala);
  },
};

document.addEventListener("click", function (e) {
  const botao = e.target.closest("[data-ouvir]");
  if (!botao) return;
  const alvo = document.querySelector(botao.dataset.ouvir);
  if (alvo) CadU.ouvir(alvo.textContent);
});
