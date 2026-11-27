from __future__ import annotations

import datetime
import json
import pathlib
import subprocess

BASE = "https://github.io"
LAVA = "https://lava.top"
PARTNER = "https://apumia.space"

OFFERS: list[tuple[str, str, str, str]] = [
    (
        "APUMIA Year-End Tax, 1099-NEC & Section 179 Shield ($149)",
        "Zero-Float Dec 31 equipment write-off & IRS 1099-NEC penalty shield",
        f"{BASE}/year-end-tax-shield-demo/",
        f"{LAVA}/e72dd355-94b0-4f12-913f-f624a401971e",
    ),
    (
        "APUMIA Merchant Fee Overcharge & Basis-Point Auditor ($249)",
        "Zero-Float bps & junk-fee recovery engine",
        f"{BASE}/merchant-fee-auditor-demo/",
        f"{LAVA}/592e0c6e-49b6-4dd9-a119-be60e5c952e1",
    ),
    (
        "APUMIA Certified Payroll & Prevailing Wage Field Guard ($299)",
        "Zero-Float Davis-Bacon WH-347 crew & 1.5x overtime shield",
        f"{BASE}/certified-payroll-guard-demo/",
        f"{LAVA}/69b0e2cf-3d84-47ef-b7f3-027cb252e45d",
    ),
    (
        "APUMIA Carbon-CBAM Border Ledger ($499)",
        "Zero-Float EU Reg. 2023/956 Scope 1+2 & default-markup savings",
        f"{BASE}/carbon-cbam-ledger-demo/",
        f"{LAVA}/6e56c5e9-8c33-4750-a699-cc005068d34a",
    ),
    (
        "APUMIA FinCEN BOI & AML Guard ($399)",
        "Zero-Float 31 CFR 1010.380 multi-entity UBO + BSA smurfing shield",
        f"{BASE}/fincen-boi-aml-demo/",
        f"{LAVA}/43497c7c-b630-447e-9bb7-3368ba1ccd6a",
    ),
]


def main() -> None:
    now = datetime.datetime.now(datetime.timezone.utc)  # noqa: UP017
    idx = (now.day * 4 + (now.hour // 6)) % len(OFFERS)
    title, desc, demo, lic = OFFERS[idx]
    pr_dir = pathlib.Path("press")
    pr_dir.mkdir(exist_ok=True)
    stamp = now.strftime("%Y-%m-%d-%H")
    md = (
        f"# APUMIA Release & Partner Bulletin ({stamp} UTC)\n\n"
        f"**Featured Software Core:** {title}\n\n"
        f"{desc}\n\n"
        f"- **Free Air-Gapped Calculator:** {demo}\n"
        f"- **Commercial Core License:** {lic}\n"
        f"- **Partner Page & 20% Settlement:** {PARTNER}\n"
        f"- **MCP Registry:** {BASE}/mcp.json\n"
    )
    pathlib.Path(pr_dir, f"release-{stamp}.md").write_text(md, encoding="utf-8")
    pathlib.Path(pr_dir, "latest.md").write_text(md, encoding="utf-8")
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<rss version="2.0"><channel>'
        "<title>APUMIA Tax, Finance &amp; Partner Bulletin</title>"
        f"<link>{BASE}/</link>"
        "<description>Air-Gapped Zero-Float Tax &amp; Finance Verifiers + 20% Partner Settlement</description>"
        f"<item><title>{title}</title><link>{demo}</link>"
        f"<description>{desc} - Partner Exchange: {PARTNER}</description>"
        f"<guid>apumia-{stamp}</guid></item>"
        "</channel></rss>"
    )
    pathlib.Path(pr_dir, "feed.xml").write_text(rss, encoding="utf-8")
    payload = json.dumps(
        {
            "host": "apumiaaifund.github.io",
            "key": "apumia2026spaceindexnow8841",
            "keyLocation": f"{BASE}/apumia2026spaceindexnow8841.txt",
            "urlList": [demo, f"{BASE}/press/latest.md", f"{BASE}/press/feed.xml", f"{BASE}/mcp.json", f"{BASE}/"],
        }
    )
    res = subprocess.check_output(
        [
            "curl",
            "-sS",
            "-w",
            "HTTP:%{http_code}",
            "-X",
            "POST",
            "https://indexnow.org",
            "-H",
            "Content-Type: application/json",
            "-d",
            payload,
        ],
        text=True,
    )
    print("PR_SYNDICATE_OK:", title, res)


if __name__ == "__main__":
    main()
