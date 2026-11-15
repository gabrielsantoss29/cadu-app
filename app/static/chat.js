// Chat do CadU (estilo WhatsApp).
// - Quem ainda não fez a triagem vai para /triagem.
// - A conversa NÃO é salva: só o perfil da triagem fica no localStorage.
// - Todo texto entra na tela com textContent (CadU.el), nunca com innerHTML.
(function () {
  const $msgs = document.getElementById("mensagens");
  const $sug = document.getElementById("sugestoes");
  const $form = document.getElementById("form-chat");
  const $campo = document.getElementById("campo");
  const $mic = document.getElementById("microfone");
  const el = CadU.el.bind(CadU);

  const perfil = CadU.lerPerfil();
  const abrir = new URLSearchParams(location.search).get("abrir");   // atalho: /cadu?abrir=codigo
  // Sem triagem feita (e sem atalho), vai primeiro para as perguntinhas.
  if (perfil.etapa !== "concluida" && !abrir) { location.replace("/triagem"); return; }

  // ---------- desenho das mensagens ----------
  function rolar() { $msgs.scrollTop = $msgs.scrollHeight; }

  function balao(quem) {
    const linha = el("div", "flex " + (quem === "cadu" ? "justify-start" : "justify-end"));
    const b = el("div", "max-w-[88%] md:max-w-[70%] rounded-2xl px-4 py-3 shadow-sm " +
      (quem === "cadu" ? "rounded-tl-sm bg-white" : "rounded-tr-sm bg-cadu text-white"));
    linha.appendChild(b);
    $msgs.appendChild(linha);
    return b;
  }

  function botaoOuvir(texto) {
    const b = el("button", "mt-2 inline-flex min-h-[48px] items-center gap-2 rounded-xl bg-cadu-claro px-4 text-base font-semibold text-cadu-escuro");
    b.type = "button";
    b.appendChild(CadU.icone("ouvir", "h-5 w-5"));
    b.append("Ouvir");
    b.addEventListener("click", () => CadU.ouvir(texto));
    return b;
  }

  function falaCadu(texto) {
    const b = balao("cadu");
    b.appendChild(el("p", "whitespace-pre-line", texto));
    b.appendChild(botaoOuvir(texto));
    rolar();
    return b;
  }

  function falaVoce(texto) {
    balao("voce").appendChild(el("p", "whitespace-pre-line break-words", texto));
    rolar();
  }

  function linhaInfo(pai, rotulo, valor) {
    if (!valor) return;
    const p = el("p", "mt-2");
    p.appendChild(el("strong", "", rotulo + ": "));
    p.append(valor);
    pai.appendChild(p);
  }

  // Mostra uma orientação da base: título, resposta, passo a passo, fonte e avisos.
  function falaOrientacao(r) {
    const o = r.orientacao;
    const b = balao("cadu");

    const selo = el("span", "inline-block rounded-full px-3 py-0.5 text-base font-bold " +
      (r.confianca === "ALTA" ? "bg-green-600 text-white" : "bg-cadu-amarelo text-cadu-texto"),
      r.confianca === "ALTA" ? "Achei a resposta" : "Acho que é isso. Confira:");
    b.appendChild(selo);
    b.appendChild(el("p", "mt-2 text-xl font-bold", o.titulo));
    b.appendChild(el("p", "mt-1", o.resposta));

    const det = el("details", "mt-2 rounded-xl bg-cadu-fundo p-3");
    det.appendChild(el("summary", "min-h-[48px] cursor-pointer py-2 font-bold text-cadu-escuro", "Ver passo a passo"));
    linhaInfo(det, "Quem pode", o.quem_pode);
    linhaInfo(det, "Como pedir", o.como_pedir);
    if (o.documentos && o.documentos.length) linhaInfo(det, "Documentos", o.documentos.join("; "));
    linhaInfo(det, "Onde", o.onde);
    linhaInfo(det, "Prazo", o.renovacao);
    linhaInfo(det, "Se bloquear ou acabar", o.se_bloquear);
    b.appendChild(det);

    // Fonte e data (o link só é criado se for http/https)
    const fonte = el("p", "mt-3 text-base text-slate-600");
    fonte.append("Fonte: ");
    if (/^https?:\/\//.test(o.fonte)) {
      const a = el("a", "inline-flex min-h-[48px] items-center underline text-cadu", o.fonte_nome || o.fonte);
      a.href = o.fonte; a.target = "_blank"; a.rel = "noopener noreferrer";
      fonte.appendChild(a);
    } else {
      fonte.append(o.fonte_nome || o.fonte);
    }
    fonte.append(" · conferido em " + o.verificado_em);
    b.appendChild(fonte);
    if (!o.conferido_por_humano) {
      b.appendChild(el("p", "mt-1 text-base text-amber-700", "Informação ainda em conferência pela equipe."));
    }
    b.appendChild(el("p", "mt-1 text-base text-slate-600", "O CadU não é canal oficial."));
    b.appendChild(botaoOuvir(o.titulo + ". " + o.resposta));
    rolar();

    // Depois da resposta: alternativas e "isso ajudou?"
    const opcoes = [];
    (r.alternativas || []).forEach(alt =>
      opcoes.push(["Talvez seja: " + alt.titulo, () => abrirCodigo(alt.codigo, alt.titulo)]));
    opcoes.push(["Ajudou", () => { falaVoce("Ajudou"); falaCadu("Que bom! Quer perguntar mais alguma coisa?"); sugestoesPadrao(); }]);
    opcoes.push(["Não ajudou", () => {
      falaVoce("Não ajudou");
      falaCadu("Tente escrever de outro jeito ou veja a aba Benefícios. Se preferir, ligue 121 ou procure o CRAS da sua cidade.");
      sugestoesPadrao();
    }]);
    sugestoes(opcoes);
  }

  // ---------- botões rápidos ----------
  function sugestoes(lista) {
    $sug.replaceChildren();
    lista.forEach(function ([rotulo, acao]) {
      const b = el("button", "min-h-[48px] shrink-0 rounded-full border-2 border-cadu bg-white px-4 text-base font-bold text-cadu-escuro hover:bg-cadu-claro", rotulo);
      b.type = "button";
      b.addEventListener("click", () => { $sug.replaceChildren(); acao(); });
      $sug.appendChild(b);
    });
  }

  function sugestoesPadrao() {
    sugestoes([
      ["Meu benefício bloqueou", () => abrirCodigo("bolsa-familia-bloqueio-cancelamento", "Meu benefício bloqueou")],
      ["Atualizar cadastro", () => abrirCodigo("cadunico-atualizar", "Atualizar cadastro")],
      ["Quando cai o pagamento?", () => abrirCodigo("bolsa-familia-calendario", "Quando cai o pagamento?")],
      ["Golpes", () => abrirCodigo("golpes-cuidados", "Golpes")],
    ]);
  }

  // ---------- conversa com o servidor ----------
  async function chamar(url, opcoes) {
    try {
      const resp = await fetch(url, opcoes);
      return await resp.json();
    } catch (e) {
      return { erro: "Estou sem conexão agora. Tente de novo ou ligue 121." };
    }
  }

  function mostrarResposta(r) {
    if (r.tipo === "encontrada") { falaOrientacao(r); return; }
    if (r.erro) { falaCadu(r.erro); return; }
    falaCadu(r.mensagem);
    if (r.tipo === "nao_encontrei") {
      sugestoes((r.categorias || []).map((c, i) => [c, () => { location.href = "/beneficios#cat-" + (i + 1); }]));
    }
  }

  async function perguntar(texto) {
    const r = await chamar("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem: texto }),
    });
    mostrarResposta(r);
  }

  async function abrirCodigo(codigo, comoPergunta) {
    if (comoPergunta) falaVoce(comoPergunta);
    if (!/^[a-z0-9-]{1,60}$/.test(codigo)) { falaCadu("Não achei esse assunto."); return; }
    const r = await chamar("/api/orientacao/" + codigo);
    mostrarResposta(r.erro ? { erro: "Ainda não tenho esse assunto. Ligue 121 ou procure o CRAS." } : r);
  }

  $form.addEventListener("submit", function (e) {
    e.preventDefault();
    const texto = $campo.value.trim();
    if (!texto) { $campo.focus(); return; }
    falaVoce(texto);
    $campo.value = "";
    $sug.replaceChildren();
    perguntar(texto);
  });

  // ---------- microfone (voz do navegador; provisório até a voz própria) ----------
  const Reconhecer = window.SpeechRecognition || window.webkitSpeechRecognition;
  $mic.addEventListener("click", function () {
    if (!Reconhecer) {
      falaCadu("Seu navegador ainda não deixa falar comigo por voz. Escreva sua dúvida, por favor.");
      return;
    }
    const rec = new Reconhecer();
    rec.lang = "pt-BR";
    rec.interimResults = false;
    $mic.classList.add("animate-pulse", "ring-4", "ring-cadu");
    rec.onresult = function (ev) {
      const texto = ev.results[0][0].transcript;
      $campo.value = texto.slice(0, 300);
      $form.requestSubmit();
    };
    rec.onerror = function (ev) {
      falaCadu(ev.error === "not-allowed" || ev.error === "service-not-allowed"
        ? "Preciso da sua permissão para usar o microfone. Libere no navegador ou escreva sua dúvida."
        : "Não consegui ouvir. Tente de novo ou escreva.");
    };
    rec.onend = () => $mic.classList.remove("animate-pulse", "ring-4", "ring-cadu");
    rec.start();
  });

  document.getElementById("recomecar").addEventListener("click", function () {
    if (!confirm("Apagar suas respostas deste aparelho e recomeçar?")) return;
    CadU.apagarDados();
    location.href = "/triagem";
  });

  // ---------- abertura (passo 4 da triagem) ----------
  const tem = (perfil.beneficios || []);
  if (perfil.cadastrado === "Sim") {
    falaCadu(tem.length ? "Entendi, você tem " + tem.join(", ") + ". Com o que posso te ajudar?"
                        : "Entendi. Com o que posso te ajudar?");
    sugestoesPadrao();
  } else if (perfil.cadastrado === "Ainda não" || perfil.cadastrado === "Não sei") {
    falaCadu("Você quer entrar no CadÚnico ou tirar dúvidas?");
    const lista = [
      ["Quero entrar", () => abrirCodigo("cadunico-como-fazer", "Quero entrar")],
      ["Tirar dúvidas", () => { falaVoce("Tirar dúvidas"); falaCadu("Pode escrever sua dúvida aqui embaixo, ou tocar no microfone para falar."); sugestoesPadrao(); }],
    ];
    if (perfil.cadastrado === "Não sei") {
      lista.splice(1, 0, ["Saber se já estou cadastrado", () => abrirCodigo("cadunico-estou-no-cadastro", "Saber se já estou cadastrado")]);
    }
    sugestoes(lista);
  } else {
    falaCadu("Oi, eu sou o CadU! Com o que posso te ajudar?");
    sugestoesPadrao();
  }

  // Atalho vindo de outra tela: /cadu?abrir=codigo
  if (abrir) abrirCodigo(abrir);
})();
