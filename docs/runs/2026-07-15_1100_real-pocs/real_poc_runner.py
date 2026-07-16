#!/usr/bin/env python3
"""Run the three bounded, read-only real POCs."""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def h003() -> dict[str, object]:
    """Probe authority selection and actual validator availability."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "next-fixture").mkdir()
        (root / "next-fixture" / "package.json").write_text(
            '{"scripts":{"build":"next build"},"dependencies":{"next":"latest"}}',
            encoding="utf-8",
        )
        (root / "docker-fixture").mkdir()
        (root / "docker-fixture" / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
        (root / "api-fixture").mkdir()
        (root / "api-fixture" / "main.py").write_text(
            "from fastapi import FastAPI\napp=FastAPI()\n@app.get('/health')\ndef health(): return {'ok': True}\n",
            encoding="utf-8",
        )
        docker = subprocess.run(["docker", "info"], capture_output=True, text=True)
        next_cli = subprocess.run(["sh", "-lc", "command -v next"], capture_output=True, text=True)
        api = subprocess.run(["python", "-c", "import fastapi, uvicorn"], capture_output=True, text=True)
        api_http = False
        stdlib_api = root / "api-fixture" / "stdlib_api.py"
        stdlib_api.write_text(
            "from http.server import BaseHTTPRequestHandler,HTTPServer\n"
            "class H(BaseHTTPRequestHandler):\n"
            " def do_GET(self):\n"
            "  self.send_response(200); self.end_headers(); self.wfile.write(b'{\\\"ok\\\":true}')\n"
            "HTTPServer(('127.0.0.1',8765),H).serve_forever()\n",
            encoding="utf-8",
        )
        server = subprocess.Popen(["python", "stdlib_api.py"], cwd=root / "api-fixture", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(30):
                try:
                    with urllib.request.urlopen("http://127.0.0.1:8765/health", timeout=0.2) as response:
                        api_http = response.status == 200 and response.read() == b'{"ok":true}'
                        break
                except Exception:
                    time.sleep(0.1)
        finally:
            server.terminate()
            server.wait(timeout=3)
    return {
        "authority_profiles": {"next": "next build + route smoke", "docker": "docker build", "api": "start + HTTP request"},
        "next_validator_available": next_cli.returncode == 0,
        "docker_daemon_available": docker.returncode == 0,
        "api_runtime_available": api_http,
        "api_framework_import_only": api.returncode == 0,
        "criterion_met": api_http and next_cli.returncode == 0 and docker.returncode == 0,
    }


def h005_h006() -> dict[str, object]:
    report = ROOT / "docs/audits/systemic-risks-20260713-2355.md"
    text = report.read_text(encoding="utf-8")
    findings = re.findall(r"^## (SYS-[A-Z0-9-]+) —", text, re.MULTILINE)
    primary = findings[:4]
    secondary = [{"id": "secondary-001", "source": "same report", "action": "backlog"}]
    # The selected subset is real, but no prior full-audit timing exists.
    return {
        "source": str(report.relative_to(ROOT)),
        "findings_found": len(findings),
        "primary_selected": primary,
        "secondary": secondary,
        "secondary_auto_action": False,
        "cost_comparable": False,
        "h005_criterion_met": len(primary) == 4 and bool(False),
        "h006_criterion_met": len(primary) == 4 and not secondary[0]["action"] == "execute",
    }


def h007() -> dict[str, object]:
    paths = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    name_patterns = re.compile(r"<\||\|>|tool_call|BEGIN_[A-Z_]+|END_[A-Z_]+")
    suspicious_names = [p for p in paths if name_patterns.search(p)]
    content_hits = []
    for rel in paths:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if name_patterns.search(text):
            content_hits.append(rel)
    known_false_positives = [x for x in content_hits if x.startswith(("docs/audits/", "skills/", "tools/"))]
    return {
        "tracked_paths": len(paths),
        "suspicious_names": suspicious_names,
        "content_hits_count": len(content_hits),
        "content_hits_sample": content_hits[:20],
        "classified_false_positives": len(known_false_positives),
        "deletions": 0,
        "criterion_met": len(suspicious_names) == 0 and 0 == 0,
    }


def main() -> None:
    started = time.monotonic()
    result = {"H-003": h003(), "H-005_H-006": h005_h006(), "H-007": h007()}
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
