// Mapa dos CRAS de São Paulo (Leaflet + OpenStreetMap). A posição da pessoa nunca sai do aparelho.
(function () {
  const CENTRO_SP = [-23.5505, -46.6333];
  const LIMITE_KM = 45; // mais longe que isso, a pessoa não está em São Paulo
  const mapa = L.map("mapa").setView(CENTRO_SP, 10);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18, attribution: "© OpenStreetMap",
    referrerPolicy: "strict-origin-when-cross-origin"
  }).addTo(mapa);

  const $lista = document.getElementById("lista");
  const $aviso = document.getElementById("aviso-mapa");
  let marcaVoce = null;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function km(a, b) {
    const R = 6371, rad = Math.PI / 180;
    const dLat = (b[0] - a[0]) * rad, dLon = (b[1] - a[1]) * rad;
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(a[0] * rad) * Math.cos(b[0] * rad) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  function aviso(txt) { $aviso.textContent = txt || ""; $aviso.hidden = !txt; }

  const cras = POSTOS.filter(p => p.tipo === "CRAS");
  cras.forEach(function (p) {
    L.marker([p.lat, p.lon]).addTo(mapa).bindPopup("<strong>" + esc(p.nome) + "</strong><br>" + esc(p.endereco));
  });

  function cartao(p, dist) {
    const dest = p.lat + "," + p.lon;
    const li = document.createElement("li");
    li.className = "rounded-2xl border-2 border-cadu-claro bg-white p-4";
    li.innerHTML =
      '<p class="text-xl font-bold">' + esc(p.nome) +
      (dist != null ? ' <span class="text-base font-normal text-slate-600">· ' + dist.toFixed(1).replace(".", ",") + " km</span>" : "") + "</p>" +
      '<p class="mt-1 text-lg">' + esc(p.endereco) + (p.cep ? " · CEP " + esc(p.cep) : "") + "</p>" +
      '<div class="mt-3 flex flex-wrap gap-2 text-base font-semibold">' +
      '<a class="min-h-toque inline-flex items-center rounded-xl bg-cadu px-4 py-2 text-white" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=' + dest + '">Google Maps</a>' +
      '<a class="min-h-toque inline-flex items-center rounded-xl bg-cadu-claro px-4 py-2 text-cadu-escuro" target="_blank" rel="noopener" href="https://waze.com/ul?ll=' + dest + '&navigate=yes">Waze</a>' +
      '<a class="min-h-toque inline-flex items-center rounded-xl bg-cadu-claro px-4 py-2 text-cadu-escuro" target="_blank" rel="noopener" href="https://maps.apple.com/?daddr=' + dest + '">Apple Maps</a></div>';
    return li;
  }

  function mostrar(origem) {
    $lista.innerHTML = "";
    let itens = cras.map(p => ({ p: p, d: origem ? km(origem, [p.lat, p.lon]) : null }));
    if (origem) {
      itens.sort((a, b) => a.d - b.d);
      itens = itens.slice(0, 5);
      document.getElementById("titulo-lista").textContent = "Os 5 CRAS mais perto";
    } else {
      itens.sort((a, b) => a.p.nome.localeCompare(b.p.nome, "pt-BR"));
      document.getElementById("titulo-lista").textContent = "Todos os CRAS (" + itens.length + ")";
    }
    itens.forEach(i => $lista.appendChild(cartao(i.p, i.d)));
  }

  function irPara(origem) {
    aviso("");
    if (km(origem, CENTRO_SP) > LIMITE_KM) {
      aviso("Esse lugar fica fora de São Paulo. O mapa só tem a cidade de São Paulo. Em outras cidades, ligue 121 ou procure o CRAS no site da prefeitura.");
      mostrar(null);
      return;
    }
    if (marcaVoce) marcaVoce.remove();
    marcaVoce = L.circleMarker(origem, { radius: 9, color: "#F5B72E", fillColor: "#F5B72E", fillOpacity: 0.9 }).addTo(mapa).bindPopup("Você");
    mostrar(origem);
    mapa.invalidateSize();
    const perto = cras.map(p => [p.lat, p.lon]).sort((a, b) => km(origem, a) - km(origem, b)).slice(0, 3);
    mapa.fitBounds(L.latLngBounds([origem].concat(perto)).pad(0.3));
  }

  document.getElementById("usar-local").addEventListener("click", function () {
    if (!navigator.geolocation) { aviso("Seu aparelho não deixa usar a localização. Digite o CEP."); return; }
    navigator.geolocation.getCurrentPosition(
      pos => irPara([pos.coords.latitude, pos.coords.longitude]),
      () => aviso("Não consegui pegar sua localização. Digite o CEP."),
      { timeout: 10000 });
  });

  async function buscarCep() {
    const cep = document.getElementById("cep").value.replace(/\D/g, "");
    if (cep.length !== 8) { aviso("O CEP tem 8 números."); return; }
    aviso("");
    try {
      const v = await (await fetch("https://viacep.com.br/ws/" + cep + "/json/")).json();
      if (v.erro) { aviso("Não achei esse CEP. Confira os números."); return; }
      const q = [v.logradouro, v.bairro, v.localidade, v.uf, "Brasil"].filter(Boolean).join(", ");
      const g = await (await fetch("https://nominatim.openstreetmap.org/search?format=json&limit=1&q=" + encodeURIComponent(q))).json();
      if (!g.length) { aviso("Não consegui achar esse endereço no mapa. Tente usar a localização."); return; }
      irPara([parseFloat(g[0].lat), parseFloat(g[0].lon)]);
    } catch (e) {
      aviso("Sem conexão agora. Tente de novo.");
    }
  }
  document.getElementById("buscar-cep").addEventListener("click", buscarCep);
  document.getElementById("cep").addEventListener("keydown", e => { if (e.key === "Enter") buscarCep(); });

  window.addEventListener("resize", function () { mapa.invalidateSize(); });
  mostrar(null);
})();
