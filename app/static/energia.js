// Calculadora de energia.
// kWh por mês de um aparelho = potência (W) x horas por dia x 30 dias x quantidade / 1000
// Custo = kWh por mês x preço do kWh
(function () {
  const DIAS = 30;
  const $tarifa = document.getElementById("tarifa");
  const reais = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

  // Lê um número de um campo, respeitando mínimo e máximo (campo vazio ou errado = mínimo).
  function numero(campo, minimo, maximo) {
    const v = parseFloat(String(campo.value).replace(",", "."));
    if (!isFinite(v)) return minimo;
    return Math.min(Math.max(v, minimo), maximo);
  }

  function calcular() {
    let kwh = 0;
    document.querySelectorAll(".aparelho").forEach(function (ap) {
      if (!ap.querySelector(".usar").checked) return;
      const potencia = Number(ap.dataset.potencia);
      const qtd = numero(ap.querySelector(".qtd"), 1, 20);
      const horas = numero(ap.querySelector(".horas"), 0, 24);
      kwh += potencia * horas * DIAS * qtd / 1000;
    });
    compararRegiao(kwh);
    const tarifa = numero($tarifa, 0, 10);
    document.getElementById("kwh").textContent = Math.round(kwh) + " kWh";
    // Preço vazio, errado ou zero: pede para conferir em vez de mostrar R$ 0,00
    document.getElementById("custo").textContent = tarifa > 0 ? reais.format(kwh * tarifa) : "Falta o preço";

    // Comparação com o limite
    const pct = Math.min(100, (kwh / LIMITE_KWH) * 100);
    const barra = document.getElementById("barra-limite");
    barra.style.width = pct + "%";
    // Cor direto no estilo: amarelo (destaque) se passou do limite, verde se está dentro
    barra.style.backgroundColor = kwh > LIMITE_KWH ? "#F5B72E" : "#16A34A";
    document.getElementById("comparacao").textContent = kwh > LIMITE_KWH
      ? "Passou " + Math.round(kwh - LIMITE_KWH) + " kWh do limite de " + LIMITE_KWH + ". Veja as dicas."
      : "Dentro do limite de " + LIMITE_KWH + " kWh por mês.";
  }

  // Comparação com a média da região (dado da EPE, só como referência)
  const $regiao = document.getElementById("regiao");
  function compararRegiao(kwh) {
    const alvo = document.getElementById("media-regiao");
    const media = parseFloat($regiao.value);
    if (!isFinite(media)) { alvo.textContent = ""; return; }
    alvo.textContent = kwh > 0
      ? "Média da região: " + Math.round(media) + " kWh por mês. A sua conta, pelos aparelhos marcados: " + Math.round(kwh) + " kWh."
      : "Média da região: " + Math.round(media) + " kWh por mês.";
  }

  // Mexer em quantidade ou horas já marca o aparelho
  document.querySelectorAll(".aparelho").forEach(function (ap) {
    ap.querySelectorAll(".qtd, .horas").forEach(c => c.addEventListener("input", function () {
      ap.querySelector(".usar").checked = true;
    }));
  });
  document.addEventListener("input", calcular);
  document.addEventListener("change", calcular);
  calcular();
})();
