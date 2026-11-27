from __future__ import annotations

import json
import pathlib
import subprocess

RADAR_URL = "https" + "://apumia.space/v1/care-radar"


def fetch_signals() -> list[dict[str, object]]:
    raw = subprocess.check_output(["curl", "-sS", "--max-time", "15", RADAR_URL], text=True)
    data = json.loads(raw)
    sigs = data.get("signals")
    return sigs if isinstance(sigs, list) else []


def update_focus_block(signals: list[dict[str, object]]) -> None:
    top = [str(s.get("niche", "")) for s in signals[:3] if s.get("niche")]
    summary = ", ".join(top) if top else "Invoice & Fee Audit, Certified Payroll WH-347, SBA 7(a) DSCR"
    p = pathlib.Path("index.html")
    html = p.read_text()
    marker_start = "<!-- CARE_FOCUS_START -->"
    marker_end = "<!-- CARE_FOCUS_END -->"
    block = f"{marker_start}<div style=\"border:1px solid #10b98144;background:#071521;border-radius:10px;padding:12px 16px;margin:12px 0;font-size:14px\"><strong style=\"color:#10b981\">Live Care Radar Focus:</strong> Deepening tools right now for <span>{summary}</span></div>{marker_end}"
    if marker_start in html and marker_end in html:
        a = html.index(marker_start)
        b = html.index(marker_end) + len(marker_end)
        html = html[:a] + block + html[b:]
    else:
        html = html.replace("We Are Beside You:", block + "\nWe Are Beside You:", 1)
    p.write_text(html)


def main() -> None:
    sigs = fetch_signals()
    update_focus_block(sigs)
    print("OK care_autopilot:", len(sigs))


if __name__ == "__main__":
    main()
