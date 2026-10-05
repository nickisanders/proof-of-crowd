/* Free scan.

   Two sources, deliberately. The static JSON is the floor: it is published with
   the site, costs nothing, and keeps the page working whether or not a server
   is up. The API is the ceiling: it scans a token nobody pre-scanned, which is
   the token a buyer actually types.

   The static file is always loaded first so the page is usable immediately, and
   the API is only called for a token the population does not already cover. If
   the API is down, unreachable or not deployed, the page silently degrades to
   what it did before, which is why SCAN_API can be left empty. */
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

  // Empty disables live scanning and the page runs on the static file alone.
  var SCAN_API = "";   // set to e.g. "https://api.proofofcrowd.com" once deployed

  var el = function (id) { return document.getElementById(id); };
  var pct = function (v) { return v === null || v === undefined ? "n/a" : (v * 100).toFixed(1) + "%"; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  var data = null;

  function normalise(raw) {
    var k = raw.trim().toLowerCase().replace(/^\$/, "").replace(/\s+/g, "-");
    return ALIAS[k] || k;
  }

  function notice(title, body, cta) {
    return '<div class="card"><h3>' + title + '</h3><p>' + body + '</p>' +
      (cta ? '<p style="margin-top:14px"><a class="cta" href="./#contact">' + cta + '</a></p>' : '') +
      '</div>';
  }

  function render(topic, live) {
    var out = el("result");
    var t = live || data.tokens[topic];
    out.hidden = false;

    if (t && t.insufficient) {
      out.innerHTML = notice("Not enough conversation to judge", esc(t.message),
        "Ask for a full audit");
      return;
    }
    if (!t) {
      if (SCAN_API) {
        out.innerHTML = notice("Scanning " + esc(topic) + "…", "Reading its posts now.", "");
        scanLive(topic);
        return;
      }
      out.innerHTML = notice("Not scanned yet",
        "Nothing on <strong>" + esc(topic) + "</strong> in this run. The population is " +
        data.population + " tokens and grows with each one requested.",
        "Ask for it to be scanned");
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
        '<p class="sub" style="font-size:14px">' + t.posts + ' posts read' +
          (t.source === "live" ? ", scanned just now" : "") + '. ' +
          'Percentiles rank this token against the ' +
          (t.compared_against || data.population) +
          ' scanned, not against a fixed threshold.</p>' +
        rows +
      '</div>';
  }

  var inflight = null;

  function scanLive(topic) {
    if (inflight === topic) { return; }
    inflight = topic;
    fetch(SCAN_API + "/scan?topic=" + encodeURIComponent(topic))
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, body: j }; }); })
      .then(function (res) {
        if (normalise(el("q").value) !== topic) { return; }   // they typed on
        if (!res.ok) {
          el("result").innerHTML = notice("Could not scan that yet",
            esc(res.body.message || "Try again shortly."), "Ask for a full audit");
          return;
        }
        render(topic, res.body);
      })
      .catch(function () {
        el("result").innerHTML = notice("Not scanned yet",
          "Nothing on <strong>" + esc(topic) + "</strong> in this run.",
          "Ask for it to be scanned");
      })
      .finally(function () { inflight = null; });
  }

  var debounce = null;
  function go() {
    var v = el("q").value;
    if (!v.trim()) { el("result").hidden = true; return; }
    var topic = normalise(v);
    // Known tokens render instantly off the static file; only an unknown one
    // waits, so a live call is never fired on every keystroke of a known name.
    if (data.tokens[topic] || !SCAN_API) { render(topic); return; }
    clearTimeout(debounce);
    debounce = setTimeout(function () { render(topic); }, 450);
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
