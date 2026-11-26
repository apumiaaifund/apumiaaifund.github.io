from __future__ import annotations

import datetime
import http.client
import json
import pathlib


def main() -> None:
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d-%H")
    host = "ainotary-edge." + "apumia-notary.workers.dev"
    conn = http.client.HTTPSConnection(host, timeout=30)
    payload = json.dumps({"question": "Write a 3-paragraph US English press dispatch for small business owners showcasing one of our live deterministic Zero-Float systems and inviting media/bloggers to our Partner Barter Exchange at https://" + host + "/press"})
    conn.request("POST", "/pr/ask", body=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    ans = json.loads(conn.getresponse().read().decode()).get("answer", "")
    conn.close()
    pathlib.Path(f"press-releases/dispatch-{ts}.md").write_text(f"# APUMIA Space & SMB Press Dispatch ({ts} UTC)\n\n{ans}\n\n---\n*Partner Barter Portal: https://{host}/press*\n")
    idx_conn = http.client.HTTPSConnection("api.indexnow.org", timeout=10)
    idx_body = json.dumps({"host": "apumiaaifund.github.io", "key": "apumia2026spaceindexnow8841", "urlList": [f"https://github.io{ts}.html"]})
    try:
        idx_conn.request("POST", "/indexnow", body=idx_body, headers={"Content-Type": "application/json"})
        idx_conn.getresponse().read()
    except OSError as exc:
        print("INDEXNOW_WARN:", exc)
    finally:
        idx_conn.close()
    print("PR_DISPATCH_PUBLISHED:", ts)


if __name__ == "__main__":
    main()
