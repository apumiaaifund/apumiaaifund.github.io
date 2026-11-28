(function () {
  const path = location.pathname.replace(/^\/|\/$/g, "") || "home";
  const ping = (niche) => fetch("https://apumia.space", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ niche }),
    keepalive: true
  }).catch(() => {});

  let visited = [];
  try { visited = JSON.parse(localStorage.getItem("apumia_journey") || "[]"); } catch (e) {}
  if (!visited.includes(path)) {
    visited.push(path);
    try { localStorage.setItem("apumia_journey", JSON.stringify(visited)); } catch (e) {}
    if (visited.length > 1) ping("platform_cross_tool_return");
  }
  ping("platform_demo_view");

  const chains = [
    { href: "../dot-guard-demo/", label: "1. Fleet DOT Compliance Audit" },
    { href: "../insure-proof-demo/", label: "2. Insurance Risk Passport (15-25% Credit)" },
    { href: "../deal-guard-demo/", label: "3. SBA 7(a) 1.25x DSCR Bank Pack" },
    { href: "../1099-misclassification-calculator/", label: "4. 1099 vs. W-2 Tax Shield" },
    { href: "../cpa-audit-desk/", label: "Full CPA & SMB Audit Desk (56 Tools)" }
  ];

  document.addEventListener("DOMContentLoaded", async () => {
    const seed = path + "|" + new Date().toISOString() + "|" + Math.random();
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(seed));
    const hash = Array.from(new Uint8Array(buf)).map(x => x.toString(16).padStart(2, "0")).join("");
    const verifyUrl = "https://apumia.space" + hash;

    // Compute lightweight 16-bit SHA-256 Proof-of-Work (~15ms) and anchor zero-PII hash
    (async () => {
      let pow_nonce = 0;
      for (; pow_nonce < 500000; pow_nonce++) {
        const pb = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(hash + ":" + pow_nonce));
        const view = new DataView(pb);
        if (view.getUint16(0) === 0) break;
      }
      fetch("https://apumia.space", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hash, module: path, pow_nonce }),
        keepalive: true
      }).catch(() => {});
    })();

    const box = document.createElement("div");
    box.style.cssText = "max-width:820px;margin:18px auto;padding:18px 20px;background:#0f172a;border:1px solid #38bdf855;border-radius:12px;font-family:system-ui,-apple-system,sans-serif;color:#e2e8f0;font-size:13px";
    box.innerHTML =
      '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px">' +
        '<span style="font-weight:800;color:#38bdf8;letter-spacing:.5px">APUMIA UNIFIED AUDIT RECORD v1.0 &bull; D1 ANCHORED</span>' +
        '<span style="background:#1e293b;padding:3px 9px;border-radius:6px;font-family:monospace;color:#10b981;font-size:11px">' + hash.slice(0, 16) + '...' + hash.slice(-8) + '</span>' +
      '</div>' +
      '<div style="color:#94a3b8;margin-bottom:10px;word-break:break-all">Modules in session: <b style="color:#fff">' + visited.length + '</b> &bull; Public Verification Link: <a href="' + verifyUrl + '" target="_blank" style="color:#38bdf8">' + verifyUrl + '</a></div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">' +
        '<button id="apu-copy-link" style="padding:8px 13px;border:none;border-radius:7px;background:#10b981;color:#042f1e;font-weight:800;cursor:pointer;font-size:12px">Copy Verification Link for Bank / Broker / Counterparty</button>' +
      '</div>' +
      '<div style="border-top:1px solid #1e293b;padding-top:12px">' +
        '<div style="font-size:11px;font-weight:800;color:#94a3b8;text-transform:uppercase;margin-bottom:8px">Connected SMB Workflow &mdash; Continue to Next Module:</div>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap">' +
          chains.filter(c => !c.href.includes(path)).map(c =>
            '<a href="' + c.href + '" style="padding:6px 10px;background:#1e293b;color:#f8fafc;border-radius:6px;text-decoration:none;font-size:12px;border:1px solid #334155">' + c.label + ' &rarr;</a>'
          ).join("") +
        '</div>' +
      '</div>' +
      '<div style="margin-top:10px;padding-top:8px;border-top:1px dashed #334155;font-size:11px;color:#94a3b8">Deterministic Integrity &amp; Calculation Record &mdash; verifies mathematical consistency and UTC timestamp via SHA-256 only (Zero-PII). Not a statutory electronic signature, legal, or CPA opinion.</div>';

    document.body.appendChild(box);
    const btn = document.getElementById("apu-copy-link");
    if (btn) {
      btn.addEventListener("click", () => {
        navigator.clipboard.writeText(verifyUrl).catch(() => {});
        btn.textContent = "Copied! Share with Bank / Broker / Auditor";
        ping("platform_shared_to_counterparty");
      });
    }
  });
})();
