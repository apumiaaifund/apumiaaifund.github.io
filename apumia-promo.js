(function () {
  const DEADLINE = new Date("2026-11-29T23:59:59Z").getTime();
  const PROMO_CODE = "0OPJDP";
  const DEALS_URL = "https://apumiaaifund.github.io/deals/";
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  const isMainOrDeals = path === "/" || path === "/index.html" || path.startsWith("/deals");
  const SANDBOX_ID = isMainOrDeals ? "main-storefront" : path.replace(/^\//, "");

  const params = new URLSearchParams(window.location.search);
  const ref = params.get("ref") || params.get("partner") || localStorage.getItem("apumia_ref");
  if (ref) localStorage.setItem("apumia_ref", ref);

  function decorateLinks() {
    document.querySelectorAll("a[href*=\"/deals\"]").forEach((link) => {
      try {
        const url = new URL(link.href);
        url.searchParams.set("utm_source", isMainOrDeals ? "storefront" : "sandbox");
        url.searchParams.set("utm_campaign", "thanksgiving_2026");
        url.searchParams.set("utm_content", SANDBOX_ID);
        if (ref) url.searchParams.set("ref", ref);
        link.href = url.toString();
      } catch (e) {}
    });
  }

  decorateLinks();
  if (isMainOrDeals) return;

  const bar = document.createElement("div");
  bar.id = "apumia-promo-bar";
  bar.style.cssText = "position:fixed;bottom:0;left:0;right:0;z-index:99999;background:#0f172a;color:#f8fafc;border-top:1px solid #334155;padding:10px 16px;font-family:system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px;font-size:13px;box-shadow:0 -4px 20px rgba(0,0,0,0.4);";

  const targetUrl = new URL(DEALS_URL);
  targetUrl.searchParams.set("utm_source", "sandbox");
  targetUrl.searchParams.set("utm_campaign", "thanksgiving_2026");
  targetUrl.searchParams.set("utm_content", SANDBOX_ID);
  if (ref) targetUrl.searchParams.set("ref", ref);

  bar.innerHTML = "<span>🔥 <b>Thanksgiving Deal:</b> All 27 Kits Bundle — <b>$2,490</b> (Save $2,433) | Ends in <b id=\"apumia-timer\">--:--:--</b></span>" +
    "<button id=\"apumia-copy-btn\" style=\"background:#1e293b;color:#38bdf8;border:1px dashed #38bdf8;padding:4px 10px;border-radius:6px;cursor:pointer;font-weight:600;\">Code: " + PROMO_CODE + " (15% OFF) 📋</button>" +
    "<a href=\"" + targetUrl.toString() + "\" target=\"_blank\" style=\"background:#2563eb;color:#fff;text-decoration:none;padding:6px 14px;border-radius:6px;font-weight:600;\">Claim Bundle →</a>";

  document.body.appendChild(bar);
  document.body.style.paddingBottom = "56px";

  document.getElementById("apumia-copy-btn").addEventListener("click", function () {
    navigator.clipboard.writeText(PROMO_CODE);
    this.textContent = "Copied: " + PROMO_CODE + " ✅";
    setTimeout(() => { this.textContent = "Code: " + PROMO_CODE + " (15% OFF) 📋"; }, 2000);
  });

  function updateTimer() {
    const diff = DEADLINE - Date.now();
    if (diff <= 0) { bar.remove(); return; }
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    document.getElementById("apumia-timer").textContent =
      d + "d " + String(h).padStart(2, "0") + "h " + String(m).padStart(2, "0") + "m " + String(s).padStart(2, "0") + "s";
  }
  updateTimer();
  setInterval(updateTimer, 1000);
})();
