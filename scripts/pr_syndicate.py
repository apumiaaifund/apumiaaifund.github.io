from __future__ import annotations

import datetime
import json
import pathlib
import subprocess

BASE = "https" + "://apumiaaifund.github.io"
LAVA = "https" + "://app.lava.top/products"
PARTNER = "https" + "://apumia.space/partner"

OFFERS = [
    ("APUMIA Merchant & Marketplace Fee Overcharge Auditor ($249)", "Zero-Float bps & junk-fee recovery engine", BASE + "/merchant-fee-auditor-demo/", LAVA + "/592e0c6e-49b6-4dd9-a119-be60e5c952e1"),
    ("APUMIA Certified Payroll & Prevailing Wage Field Guard ($299)", "Zero-Float Davis-Bacon WH-347 crew & 1.5x overtime shield", BASE + "/certified-payroll-guard-demo/", LAVA + "/69b0e2cf-3d84-47ef-b7f3-027cb252e45d"),
    ("APUMIA Carbon-CBAM Border Ledger ($499)", "Zero-Float EU Reg. 2023/956 Scope 1+2 & default-markup savings", BASE + "/carbon-cbam-ledger-demo/", LAVA + "/6e56c5e9-8c33-4750-a699-cc005068d34a"),
    ("APUMIA FinCEN BOI & AML Guard ($399)", "Zero-Float 31 CFR 1010.380 multi-entity UBO + BSA smurfing shield", BASE + "/fincen-boi-aml-demo/", LAVA + "/43497c7c-b630-447e-9bb7-3368ba1ccd6a"),
    ("APUMIA HIPAA-BAA & HHS OCR Breach Penalty Auditor ($449)", "Zero-Float 45 CFR 164.502(e) vendor BAA & OCR Tier 1-4 penalty auditor", BASE + "/hipaa-baa-ocr-demo/", LAVA + "/79d47619-5296-446e-8faa-db92fa864763"),
    ("APUMIA Compliance OS ($499)", "Unified US small business fine-exposure & WH-347 overtime auditor", BASE + "/wh347-overtime-calculator/", LAVA + "/0e50d35b-a58e-438a-b35e-98094d1de60e"),
    ("APUMIA DealGuard ($399)", "Zero-Float SBA 7(a) 1.25x DSCR & M&A due diligence verifier", BASE + "/sba-dscr-calculator/", LAVA + "/38a7a28e-194e-4240-b584-868b40fe3b77"),
    ("APUMIA InsureProof ($399)", "Commercial insurance renewal credit passport (15-25% savings)", BASE + "/insurance-renewal-calculator/", LAVA + "/df177b1b-16e7-427f-b95d-67cbe2a609fd"),
    ("US Enterprise & M&A Full-Stack Bundle ($999 - Save $298)", "All 3 flagship cores with automated multi-repo access", BASE + "/", LAVA + "/7f76c41c-cc31-4130-bb8e-636d47e7749c"),
]

def main() -> None:
    now = datetime.datetime.now(datetime.UTC)
    idx = (now.day * 4 + (now.hour // 6)) % len(OFFERS)
    title, desc, demo, lic = OFFERS[idx]
    pr_dir = pathlib.Path("press")
    pr_dir.mkdir(exist_ok=True)
    stamp = now.strftime("%Y/%m/%d/%H").replace("/", "-")
    md = f"# APUMIA Release Bulletin ({stamp} UTC)\n\n**Featured System:** {title}\n\n{desc}\n\n- **Free Air-Gapped Calculator:* {demo}\n- **Commercial License (Auto-GitHub Delivery):** {lic}\n- **Partner Page & 20% Referral Settlement:** {PARTNER}\n- **MCP Registry & llms.txt:** {BASE}/mcp.json\n"
    pathlib.Path(pr_dir, f"release-{stamp}.md").write_text(md)
    pathlib.Path(pr_dir, "latest.md").write_text(md)
    payload = json.dumps({"host": "apumiaaifund.github.io", "key": "apumia2026spaceindexnow8841", "keyLocation": BASE + "/apumia2026spaceindexnow8841.txt", "urlList": [demo, BASE + "/press/latest.md", BASE + "/mcp.json", BASE + "/"]})
    res = subprocess.check_output(["curl", "-sS", "-w", "HTTP:%{http_code}", "-X", "POST", "https" + "://api.indexnow.org/indexnow", "-H", "Content-Type: application/json", "-d", payload], text=True)
    print("PR_SYNDICATE_OK:", title, res)

if __name__ == "__main__":
    main()
