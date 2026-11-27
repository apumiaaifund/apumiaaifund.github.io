(function(){
  const CFG={
    "sba-dscr-calculator":{name:"APUMIA DealGuard (SBA 7a / M&A)",price:"$399",uuid:"cf81703d-737e-4804-bdab-48163b7c5154"},"wh347-overtime-calculator":{name:"APUMIA Compliance OS",price:"$499",uuid:"0e50d35b-a58e-438a-b35e-98094d1de60e"},"insurance-renewal-calculator":{name:"APUMIA InsureProof Risk Passport",price:"$399",uuid:"57a3163c-41b4-49b2-85f5-596ee58e1293"},"eu-ai-act-fine-calculator":{name:"APUMIA AIAct-NIST Auditor (EU AI Act & NIST)",price:"$499",uuid:"84b5b45a-92e2-4e83-a6fa-8a15eb008f2e"},"ai-finops-burn-calculator":{name:"APUMIA AgentSpend Firewall (AI FinOps)",price:"$299",uuid:"26129651-3b9f-4c0b-aae3-5a8f558e6f9e"},"cpa-suite":{name:"APUMIA Multi-Client CPA & Auditor Pro Suite",price:"$199",uuid:"723f8cbd-4405-4041-a217-b68443c0bd25"},"compliance-os-demo":{name:"APUMIA Compliance OS",price:"$499",uuid:"0e50d35b-a58e-438a-b35e-98094d1de60e"},
    "deal-guard-demo":{name:"APUMIA DealGuard (SBA 7a / M&A)",price:"$399",uuid:"cf81703d-737e-4804-bdab-48163b7c5154"},
    "insure-proof-demo":{name:"APUMIA InsureProof Risk Passport",price:"$399",uuid:"57a3163c-41b4-49b2-85f5-596ee58e1293"},
    "coldchain-ledger-demo":{name:"APUMIA ColdChain Ledger (FDA FSMA 204)",price:"$249",uuid:"dc30635a-ffe4-45e8-a135-7734590f6daa"},
    "agentspend-firewall-demo":{name:"APUMIA AgentSpend Firewall (AI FinOps)",price:"$299",uuid:"26129651-3b9f-4c0b-aae3-5a8f558e6f9e"},
    "grantaudit-2cfr-demo":{name:"APUMIA GrantAudit 2CFR (US Federal 200)",price:"$299",uuid:"3ca7d525-9932-4a54-af3d-e6e03badc092"},
    "orbital-sim-demo":{name:"APUMIA Orbital-Sim Core (no_std Rust LEO)",price:"$349",uuid:"85de1430-da5b-4665-8d06-62557dc3a04d"},
    "aiact-nist-auditor-demo":{name:"APUMIA AIAct-NIST Auditor (EU AI Act & NIST)",price:"$499",uuid:"84b5b45a-92e2-4e83-a6fa-8a15eb008f2e"}
  };
  const slug=Object.keys(CFG).find(k=>location.pathname.includes(k))||"cpa-suite";
  const meta=CFG[slug];
  const buyUrl="https"+"://app.lava.top/products/"+meta.uuid;
  async function sha256(txt){
    const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(txt));
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,"0")).join("");
  }
  function snapshotText(){
    const box=document.querySelector("#result,#output,.result,.output,main")||document.body;
    return (box.innerText||"").replace(/\s+/g," ").trim().slice(0,1200);
  }
  async function buildReceipt(){
    const ts=new Date().toISOString();
    const snap=snapshotText();
    const digest=await sha256(meta.name+"|"+ts+"|"+snap);
    return [
      "============================================================",
      "APUMIA DETERMINISTIC AUDIT RECEIPT (DEMO PREVIEW)",
      "============================================================",
      "SYSTEM:      "+meta.name,
      "STATUS:      UNVERIFIED DEMO PREVIEW (WATERMARKED)",
      "TIMESTAMP:   "+ts,
      "SHA-256:     "+digest,
      "SNAPSHOT:    "+snap.slice(0,320)+"...",
      "------------------------------------------------------------",
      "NOTICE: Demo preview is for internal evaluation only.",
      "Unlock Full Deterministic Core & Notary Seal ("+meta.price+"):",
      buyUrl,
      "============================================================"
    ].join("\n");
  }
  function mount(){
    if(document.getElementById("apumia-demo-seal-box")) return;
    const wrap=document.createElement("div");
    wrap.id="apumia-demo-seal-box";
    wrap.style.cssText="max-width:860px;margin:24px auto;padding:18px;border:1px solid #10b98166;border-radius:12px;background:#070d19;color:#e2e8f0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px";
    wrap.innerHTML=`
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px">
        <div>
          <span style="color:#10b981;font-weight:700">● CRYPTOGRAPHIC AUDIT RECEIPT (PREVIEW)</span>
          <div style="color:#94a3b8;font-size:12px;margin-top:2px">Generate a SHA-256 deterministic preview check or unlock the full air-gapped Rust/Decimal core.</div>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px">
          <button id="apumia-gen-chk" style="cursor:pointer;background:#1e293b;color:#f8fafc;border:1px solid #38bdf866;border-radius:8px;padding:9px 14px;font-weight:600">Generate Demo Receipt (.txt)</button>
          <a href="${buyUrl}" target="_blank" rel="noopener" style="text-decoration:none;background:#10b981;color:#04130d;border-radius:8px;padding:9px 16px;font-weight:700">Unlock Full Core (${meta.price}) ↗</a>
        </div>
      </div>
      <pre id="apumia-chk-out" style="display:none;white-space:pre-wrap;word-break:break-all;background:#030712;border:1px solid #1e293b;border-radius:8px;padding:12px;color:#38bdf8;margin:0"></pre>
    `;
    (document.querySelector("main")||document.body).appendChild(wrap);
    document.getElementById("apumia-gen-chk").addEventListener("click",async()=>{
      const rec=await buildReceipt();
      const pre=document.getElementById("apumia-chk-out");
      pre.style.display="block";
      pre.textContent=rec;
      const blob=new Blob([rec],{type:"text/plain;charset=utf-8"});
      const a=document.createElement("a");
      a.href=URL.createObjectURL(blob);
      a.download=slug+"-audit-preview.txt";
      a.click();
    });
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",mount); else mount();
})();