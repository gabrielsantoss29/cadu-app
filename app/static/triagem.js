// Triagem em 4 passos, uma pergunta por tela:
// 1 abertura -> 2 "já está no CadÚnico?" -> 3 "quais benefícios?" (só se Sim) -> 4 chat (/cadu).
// As respostas ficam só no localStorage deste aparelho.
(function () {
  const secoes = document.querySelectorAll("section[data-passo]");
  const perfil = CadU.lerPerfil();

  function mostrar(passo) {
    secoes.forEach(s => { s.hidden = s.dataset.passo !== String(passo); });
    document.getElementById("passo-texto").textContent = "Passo " + passo + " de 4";
    document.getElementById("barra-cheia").style.width = (passo * 25) + "%";
    document.getElementById("barra").setAttribute("aria-valuenow", passo);
    const titulo = document.querySelector('section[data-passo="' + passo + '"] h1, section[data-passo="' + passo + '"] p');
    if (titulo) { titulo.setAttribute("tabindex", "-1"); titulo.focus(); }
    window.scrollTo(0, 0);
  }

  function irParaChat() {
    perfil.etapa = "concluida";
    CadU.salvarPerfil(perfil);
    location.href = "/cadu";
  }

  // Botões "Vamos lá" e "Voltar"
  document.querySelectorAll("[data-ir]").forEach(b =>
    b.addEventListener("click", () => mostrar(Number(b.dataset.ir))));

  // Passo 2
  document.querySelectorAll("[data-cadastrado]").forEach(b =>
    b.addEventListener("click", function () {
      perfil.cadastrado = b.dataset.cadastrado;
      if (perfil.cadastrado === "Sim") {
        mostrar(3);
      } else {
        perfil.beneficios = [];   // quem não está no cadastro vai direto ao chat
        irParaChat();
      }
    }));

  // Passo 3: "Nenhum ainda" desmarca os outros, e vice-versa
  const caixas = document.querySelectorAll("#lista-beneficios input");
  const nenhum = document.getElementById("nenhum");
  caixas.forEach(c => c.addEventListener("change", function () {
    if (c === nenhum && c.checked) caixas.forEach(o => { if (o !== nenhum) o.checked = false; });
    if (c !== nenhum && c.checked) nenhum.checked = false;
  }));
  // Se já respondeu antes, deixa marcado
  (perfil.beneficios || []).forEach(n => caixas.forEach(c => { if (c.value === n) c.checked = true; }));

  document.getElementById("confirmar").addEventListener("click", function () {
    perfil.beneficios = Array.from(caixas).filter(c => c.checked && c !== nenhum).map(c => c.value);
    irParaChat();
  });

  // "Pular" também conta como triagem feita (sem respostas)
  document.getElementById("pular").addEventListener("click", function (e) {
    e.preventDefault();
    irParaChat();
  });

  mostrar(1);
})();
