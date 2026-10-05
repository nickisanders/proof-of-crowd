/* Free scan. Reads a static JSON the pipeline publishes, so the site stays on
   GitHub Pages with no backend and the API key never reaches a browser.
   A token the population does not cover is the most valuable case here: it is
   someone naming the token they care about, so it asks rather than apologises. */
(function () {
  "use strict";

  // People type tickers; the data is keyed by LunarCrush topic.
  var ALIAS = {
    btc: "bitcoin", eth: "ethereum", sol: "solana", xrp: "ripple", doge: "dogecoin",
    ada: "cardano", link: "chainlink", avax: "avalanche", dot: "polkadot",
    ltc: "litecoin", matic: "polygon", trx: "tron", shib: "shiba-inu",
    uni: "uniswap", arb: "arbitrum", op: "optimism", apt: "aptos",
    inj: "injective", tia: "celestia", hbar: "hedera", xlm: "stellar", fil: "filecoin"
  };

  var METRICS = [
    ["creator_concentration", "Creator concentration",
     "Share of interactions from the three loudest accounts"],
    ["duplicate_text", "Repeated wording",
     "Share of posts whose text repeats across three or more accounts"],
    ["cross_token_overlap", "Cross-token accounts",
     "Share of interactions from accounts posting in three or more other tokens"]
  ];

  var el = function (id) { return document.getElementById(id); };
  var pct = function (v) { return v === null || v === undefined ? "n/a" : (v * 100).toFixed(1) + "%"; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  var data = null;

  function normalise(raw) {
    var k = raw.trim().toLowerCase().replace(/^\$/, "").replace(/\s+/g, "-");
    return ALIAS[k] || k;
  }

  function render(topic) {
    var out = el("result");
    var t = data.tokens[topic];
    out.hidden = false;

    if (!t) {
      out.innerHTML =
        '<div class="card"><h3>Not scanned yet</h3>' +
        '<p>Nothing on <strong>' + esc(topic) + '</strong> in this run. The population is ' +
        data.population + ' tokens and grows with each one requested.</p>' +
        '<p style="margin-top:14px"><a class="cta" href="./#contact">Ask for it to be scanned</a></p></div>';
      return;
    }

    var rows = METRICS.map(function (m) {
      var key = m[0], value = t[key], p = t.percentiles[key];
      var width = p === null || p === undefined ? 0 : Math.round(p * 100);
      var hot = p !== null && p !== undefined && p >= 0.75;
      return '' +
        '<div class="metric' + (hot ? " hot" : "") + '">' +
          '<div class="metric-head"><span class="metric-name">' + m[1] + '</span>' +
          '<span class="metric-val">' + pct(value) + '</span></div>' +
          '<div class="bar"><span style="width:' + width + '%"></span></div>' +
          '<div class="metric-foot">' + m[2] +
            '<span>' + (p === null || p === undefined ? "" :
              Math.round(p * 100) + "th percentile of " + data.population) + '</span>' +
          '</div>' +
        '</div>';
    }).join("");

    out.innerHTML =
      '<div class="scanresult">' +
        '<div class="scanhead">' +
          '<h2 style="margin:0">' + esc(topic) + '</h2>' +
          '<span class="badge flags-' + t.flags + '">' + t.band + '</span>' +
        '</div>' +
        '<p class="sub" style="font-size:14px">' + t.posts + ' posts read. ' +
          'Percentiles rank this token against the ' + data.population +
          ' scanned, not against a fixed threshold.</p>' +
        rows +
      '</div>';
  }

  function go() {
    var v = el("q").value;
    if (!v.trim()) { el("result").hidden = true; return; }
    render(normalise(v));
  }

  fetch("assets/scans.json")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (j) {
      data = j;
      var list = el("tokens");
      Object.keys(j.tokens).forEach(function (k) {
        var o = document.createElement("option"); o.value = k; list.appendChild(o);
      });
      el("meta").textContent =
        j.population + " tokens scanned " + j.generated.slice(0, 10) + ".";
      el("q").addEventListener("input", go);
      var pre = new URLSearchParams(location.search).get("t");
      if (pre) { el("q").value = pre; go(); }
    })
    .catch(function () {
      el("meta").textContent = "Scan data could not be loaded. Try again shortly.";
    });
})();
