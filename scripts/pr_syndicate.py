from __future__ import annotations

import datetime
import http.client
import json
import os
import pathlib

FLAGSHIPS = [
    ("APUMIA Compliance OS ($499)", "Unified US Business Fine-Exposure & Multi-Regulator Audit Suite (DOT, NFPA 96, EPA FOG, ASME A17.1, FIFRA, Mechanics Liens)", "https://github.io", "https://lava.top"),
    ("APUMIA DealGuard ($399)", "US Small Business M&A & SBA 7(a) Due Diligence & 1.25x DSCR Verifier", "https://github.io", "https://lava.top"),
    ("APUMIA InsureProof ($399)", "Cryptographic Commercial Insurance Risk-Proof Passport for 15%-25% Renewal Credits", "https://github.io", "https://lava.top"),
    ("APUMIA AIAct-NIST Auditor ($499)", "Deterministic EU AI Act Art. 12/14 & NIST AI RMF 1.0 Audit Core with SHA-256 Seals", "https://apumiaaifund.github.io/aiact-nist-auditor-demo/", "https://app.lava.top/products/84b5b45a-92e2-4e83-a6fa-8a15eb008f2e"),
    ("APUMIA AgentSpend Firewall ($299)", "Zero-Float AI Agent Budget & Liability Circuit Breaker", "https://apumiaaifund.github.io/agentspend-firewall-demo/", "https://app.lava.top/products/26129651-3b9f-4c0b-aae3-5a8f558e6f9e"),
    ("APUMIA Multi-Client CPA & Auditor Pro Suite ($199)", "Bank-Ready APUMIA-BP-2026 Plans, 3-Way Match, WH-347 & Merchant Fee Audits for 20-80 Clients", "https://apumiaaifund.github.io/cpa-suite/", "https://app.lava.top/products/723f8cbd-4405-4041-a217-b68443c0bd25"),
    ("APUMIA FinCEN BOI & AML Guard ($399)", "Zero-Float 31 CFR 1010.380 Beneficial Ownership & BSA CTR/Structuring Verifier", "https://apumiaaifund.github.io/fincen-boi-aml-demo/", "https://app.lava.top/products/43497c7c-b630-447e-9bb7-3368ba1ccd6a"),
]


def main() -> None:
    now = datetime.datetime.now(datetime.UTC)
    ts = now.strftime("%Y-%m-%d-%H")
    token = os.environ.get("GITHUB_TOKEN", "")
    gh = http.client.HTTPSConnection("api." + "github.com", timeout=20)
    hdr = {"User-Agent": "APUMIA-Space-PR/1.0", "Accept": "application/vnd.github+json"}
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    gh.request("GET", "/orgs/apumiaaifund/repos?per_page=100&type=public", headers=hdr)
    repos = [r for r in json.loads(gh.getresponse().read().decode()) if not r.get("fork") and r.get("name") != ".github"]
    gh.close()
    f_name, f_desc, f_demo, f_buy = FLAGSHIPS[int(now.timestamp() // 43200) % len(FLAGSHIPS)]
    press_url = "https://ainotary-edge." + "apumia-notary.workers.dev/press"
    md = (
        f"# APUMIA US Flagship Campaign Dispatch: {f_name} ({ts} UTC)\n\n"
        f"**AUSTIN / GLOBAL** — APUMIA AI Fund today spotlighted **{f_name}** — {f_desc}, "
        f"anchoring its live ecosystem of {len(repos)} deterministic, zero-float software systems for US small businesses, M&A buyers, and commercial property operators.\n\n"
        f"- **Live Zero-Float Sandbox (Zero Login):** {f_demo}\n"
        f"- **Turnkey Commercial License & Instant GitHub Provisioning:** {f_buy}\n\n"
        f"### Media, Broker & Creator Barter Exchange\n"
        f"Business journalists, SBA brokers, and SaaS reviewers who publish a live page featuring any APUMIA Space system can claim an instant **Barter Pro Key** (free APUMIA-BP-2026 Zero-Float business plan calculation, 100 Notary AI SHA-256 cryptographic stamps, and 20% referral share) at {press_url}.\n"
    )
    pathlib.Path(f"press-releases/dispatch-{ts}.md").write_text(md, encoding="utf-8")
    idx = http.client.HTTPSConnection("api.indexnow.org", timeout=10)
    body = json.dumps({"host": "apumiaaifund.github.io", "key": "apumia2026spaceindexnow8841", "urlList": [f"https://github.io{ts}.md"]})
    try:
        idx.request("POST", "/indexnow", body=body, headers={"Content-Type": "application/json"})
        idx.getresponse().read()
    except OSError as exc:
        print("INDEXNOW_WARN:", exc)
    finally:
        idx.close()
    print("FLAGSHIP_CAMPAIGN_PUBLISHED:", f_name, "LIVE_SYSTEMS:", len(repos))


if __name__ == "__main__":
    main()
