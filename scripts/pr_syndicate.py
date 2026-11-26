from __future__ import annotations

import datetime
import http.client
import json
import os
import pathlib


def main() -> None:
    now = datetime.datetime.now(datetime.UTC)
    ts = now.strftime("%Y-%m-%d-%H")
    token = os.environ.get("GITHUB_TOKEN", "")
    gh = http.client.HTTPSConnection("api."+"github.com", timeout=20)
    hdr = {"User-Agent": "APUMIA-Space-PR/1.0", "Accept": "application/vnd.github+json"}
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    gh.request("GET", "/orgs/apumiaaifund/repos?per_page=100&type=public", headers=hdr)
    repos = [r for r in json.loads(gh.getresponse().read().decode()) if not r.get("fork") and r.get("name") != ".github"]
    gh.close()
    pick = repos[int(now.timestamp() // 43200) % max(len(repos), 1)]
    name = pick.get("name", "apumia-space")
    desc = pick.get("description") or "Deterministic Zero-Float Autonomous System by APUMIA AI Fund"
    link = pick.get("homepage") or pick.get("html_url") or "https://github.io"
    press_url = "https://ainotary-edge." + "apumia-notary.workers.dev/press"
    md = (
        f"# APUMIA Space & SMB Press Release: {name} ({ts} UTC)\n\n"
        f"**BORISOGLEBSK / AUSTIN** — APUMIA AI Fund today highlighted **{name}** ({desc}), "
        f"part of its expanding suite of {len(repos)} deterministic, zero-float software systems engineered to eliminate manual spreadsheet drift and regulatory risk for small businesses.\n\n"
        f"Operators can test the live browser sandbox immediately with zero registration at {link}. "
        f"100% of commercial proceeds fund APUMIA Space deterministic orbital engineering.\n\n"
        f"### Media & Creator Barter Exchange\n"
        f"Journalists, bloggers, and SaaS reviewers who publish a live page featuring any APUMIA Space system can claim an instant **Barter Pro Key** (free APUMIA-BP-2026 Zero-Float business plan calculation, 100 Notary AI SHA-256 cryptographic stamps, and 20% referral share) at {press_url}.\n"
    )
    pathlib.Path(f"press-releases/dispatch-{ts}.md").write_text(md, encoding="utf-8")
    idx = http.client.HTTPSConnection("api.indexnow.org", timeout=10)
    body = json.dumps({"host": "apumiaaifund.github.io", "key": "apumia2026spaceindexnow8841", "urlList": [f"https://github.iopress-releases/dispatch-{ts}.md"]})
    try:
        idx.request("POST", "/indexnow", body=body, headers={"Content-Type": "application/json"})
        idx.getresponse().read()
    except OSError as exc:
        print("INDEXNOW_WARN:", exc)
    finally:
        idx.close()
    print("PUBLISHED_OK:", name, "TOTAL_LIVE:", len(repos))


if __name__ == "__main__":
    main()
