// Chat do CadU + triagem de 4 passos.
// 1 abertura -> 2 "já está no CadÚnico?" -> 3 "quais benefícios?" (só se Sim) -> 4 chat livre.
// Tudo que a pessoa responde fica só no localStorage deste aparelho.
(function () {
  const $mensagens = document.getElementById("mensagens");
  const $opcoes = document.getElementById("opcoes");
  const $form = document.getElementById("form-chat");
  const $campo = document.getElementById("campo");
  const $passo = document.getElementById("passo");
  const $aviso = document.getElementById("aviso-dados");
  const $recomecar = document.getElementById("recomecar");

  const BENEFICIOS = ["Bolsa Família", "Pé-de-Meia", "Tarifa Social", "BPC", "Gás do Povo", "Outro", "Nenhum ainda"];

  let perfil = CadU.lerPerfil();

  // ---- desenho na tela (sempre textContent: nunca interpreta HTML) ----
  function mensagem(quem, texto, resp) {
    const div = document.createElement("div");
    const eh_cadu = quem === "cadu";
    div.className = "max-w-[90%] rounded-2xl p-4 whitespace-pre-line " +
      (eh_cadu ? "self-start bg-white border border-slate-200" : "self-end bg-emerald-600 text-white");
    const p = document.createElement("p");
    p.textContent = texto;
    div.appendChild(p);

    if (eh_cadu) {
      if (resp && resp.fonte_url && resp.fonte_url.startsWith("https://")) {
        const f = document.createElement("p");
        f.className = "mt-2 text-base text-slate-600";
        f.append("Fonte: ");
        const a = document.createElement("a");
        a.href = resp.fonte_url; a.target = "_blank"; a.rel = "noopener noreferrer";
        a.className = "underline text-sky-700";
        a.textContent = resp.fonte_nome;
        f.appendChild(a);
        f.append(" · verificado em " + resp.data_verificacao);
        div.appendChild(f);
      }
      const ouvir = document.createElement("button");
      ouvir.type = "button";
      ouvir.className = "mt-2 rounded-lg bg-sky-600 px-3 py-1 text-base font-semibold text-white";
      ouvir.textContent = "🔊 Ouvir";
      ouvir.addEventListener("click", () => CadU.ouvir(texto));
      div.appendChild(ouvir);
    }
    $mensagens.appendChild(div);
    div.scrollIntoView({ block: "end", behavior: "smooth" });
  }

  function opcoes(lista, aoEscolher) {
    $opcoes.replaceChildren();
    lista.forEach(function (rotulo) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "rounded-xl bg-white border-2 border-emerald-600 px-5 py-3 font-bold text-emerald-800 hover:bg-emerald-50";
      b.textContent = rotulo;
      b.addEventListener("click", () => { $opcoes.replaceChildren(); aoEscolher(rotulo); });
      $opcoes.appendChild(b);
    });
  }

  function mostrarPasso(n) { $passo.textContent = n ? "Passo " + n + " de 4" : ""; }

  // ---- passos da triagem ----
  function passo1() {
    mostrarPasso(1);
    mensagem("cadu", "Oi, eu sou o CadU! Vou te fazer umas perguntinhas. Não sei quem você é e não guardo nome, CPF nem renda.");
    opcoes(["Vamos lá"], passo2);
  }

  function passo2() {
    mostrarPasso(2);
    mensagem("cadu", "Você já está no CadÚnico?");
    opcoes(["Sim", "Ainda não", "Não sei"], function (r) {
      mensagem("voce", r);
      perfil.cadastrado = r;
      CadU.salvarPerfil(perfil);
      if (r === "Sim") passo3(); else passo4SemCadastro(r);
    });
  }

  function passo3() {
    mostrarPasso(3);
    mensagem("cadu", "Quais benefícios você recebe? Marque e toque em Confirmar.");
    $opcoes.replaceChildren();
    const marcados = new Set();
    BENEFICIOS.forEach(function (nome) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "rounded-xl bg-white border-2 border-emerald-600 px-5 py-3 font-bold text-emerald-800";
      b.textContent = nome;
      b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", function () {
        if (marcados.has(nome)) { marcados.delete(nome); b.setAttribute("aria-pressed", "false"); b.classList.remove("bg-emerald-600", "text-white"); }
        else { marcados.add(nome); b.setAttribute("aria-pressed", "true"); b.classList.add("bg-emerald-600", "text-white"); }
      });
      $opcoes.appendChild(b);
    });
    const ok = document.createElement("button");
    ok.type = "button";
    ok.className = "rounded-xl bg-emerald-600 px-6 py-3 font-bold text-white";
    ok.textContent = "Confirmar";
    ok.addEventListener("click", function () {
      const lista = Array.from(marcados).filter(n => n !== "Nenhum ainda");
      perfil.beneficios = lista;
      perfil.etapa = "concluida";
      CadU.salvarPerfil(perfil);
      $opcoes.replaceChildren();
      mensagem("voce", lista.length ? lista.join(", ") : "Nenhum ainda");
      passo4(lista.length ? "Entendi, você tem " + lista.join(", ") + ". Com o que posso te ajudar?"
                          : "Entendi. Com o que posso te ajudar?");
    });
    $opcoes.appendChild(ok);
  }

  // Quem não está (ou não sabe) vai direto ao chat, que pergunta o que a pessoa quer.
  function passo4SemCadastro(r) {
    perfil.etapa = "concluida";
    CadU.salvarPerfil(perfil);
    abrirChat();
    mensagem("cadu", "Tudo bem! Você quer entrar no CadÚnico ou tirar dúvidas?");
    const lista = ["Quero entrar", "Tirar dúvidas"];
    if (r === "Não sei") lista.push("Saber se já estou cadastrado");
    opcoes(lista, function (esc) {
      mensagem("voce", esc);
      if (esc === "Tirar dúvidas") mensagem("cadu", "Pode escrever sua dúvida logo abaixo.");
      else if (esc === "Quero entrar") perguntar("como fazer o cadastro no cadunico");
      else perguntar("como saber se estou no cadunico");
    });
  }

  function passo4(abertura) {
    mostrarPasso(4);
    abrirChat();
    mensagem("cadu", abertura);
  }

  function abrirChat() {
    mostrarPasso(4);
    $form.classList.remove("hidden");
    $form.classList.add("flex");
    $aviso.classList.remove("hidden");
    $recomecar.classList.remove("hidden");
  }

  // ---- conversa com a API ----
  async function perguntar(texto) {
    try {
      const r = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensagem: texto }),
      });
      const dados = await r.json();
      mensagem("cadu", dados.texto || dados.erro || "Não consegui responder agora.", dados);
    } catch (e) {
      mensagem("cadu", "Estou sem conexão agora. Tente de novo ou ligue 121.");
    }
  }

  $form.addEventListener("submit", function (e) {
    e.preventDefault();
    const texto = $campo.value.trim();
    if (!texto) return;
    mensagem("voce", texto);
    $campo.value = "";
    perguntar(texto);
  });

  $recomecar.addEventListener("click", function () {
    if (!confirm("Apagar suas respostas deste aparelho e recomeçar?")) return;
    CadU.apagarDados();
    location.reload();
  });

  // ---- início ----
  if (perfil.etapa === "concluida") {
    const tem = (perfil.beneficios || []).length ? "Você tem " + perfil.beneficios.join(", ") + ". " : "";
    passo4("Oi de novo! " + tem + "Com o que posso te ajudar?");
  } else {
    passo1();
  }
})();
