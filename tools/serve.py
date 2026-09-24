"""Local live dashboard for Shelf-Life Clock. Runs on this computer only, outside Claude.

    py tools/serve.py            then open http://127.0.0.1:8765

Serves the dashboard and lets you run tools/run_agent.py for chosen batches from the
page. Standard library only. The API key is read from the ANTHROPIC_API_KEY environment
variable of this process and is never sent to the page or written to a file.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from build_dashboard import build_data, render_page  # noqa: E402
from run_agent import DECISION_COLUMNS, QUEUE_COLUMNS  # noqa: E402

MAX_BATCHES = 10
BATCH_TIMEOUT_S = 300
ID_RE = re.compile(r"^LF-\d{5}$")

LOCK = threading.Lock()
JOB = {"running": False, "total": 0, "results": []}
PORT = 8765


def known_batches():
    with open(ROOT / "inventory_clean.csv", newline="", encoding="utf-8") as f:
        return {r["batch_id"] for r in csv.DictReader(f)}


def read_rows(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def upsert(path, columns, new_rows):
    """Replace rows with the same batch_id, keep the rest in order, add new ones at the end."""
    rows = read_rows(path)
    index = {r["batch_id"]: i for i, r in enumerate(rows)}
    for n in new_rows:
        if n["batch_id"] in index:
            rows[index[n["batch_id"]]] = n
        else:
            index[n["batch_id"]] = len(rows)
            rows.append(n)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, restval="", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run_one(batch_id):
    tmp = f"_live_{batch_id}.csv"
    stem = f"_live_{batch_id}"
    files = [ROOT / tmp, ROOT / f"{stem}_requests.md", ROOT / f"{stem}_decisions.csv"]
    try:
        p = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "run_agent.py"), batch_id, "--out", tmp],
            cwd=ROOT, capture_output=True, text=True, timeout=BATCH_TIMEOUT_S, env=os.environ.copy())
        rows = read_rows(files[0])
        if p.returncode != 0 or not rows:
            tail = (p.stderr or p.stdout or "no output").strip().splitlines()[-1:]  # last line only
            return {"batch_id": batch_id, "ok": False, "error": (tail[0] if tail else "run failed")[:300]}
        row = rows[0]
        decision = (read_rows(files[2]) or [{}])[0]
        request = ""
        if files[1].exists():
            request = re.sub(r"^# Drafted requests \(API run\)\s*|^## .*$", "", files[1].read_text(encoding="utf-8"),
                             flags=re.M).strip()
        upsert(ROOT / "action_queue_api.csv", QUEUE_COLUMNS, [row])
        if decision:
            upsert(ROOT / "decisions_api.csv", DECISION_COLUMNS, [{"batch_id": batch_id, **decision}])
        return {"batch_id": batch_id, "ok": True, "row": row, "request": request,
                "ruled_out": decision.get("ruled_out_clauses", ""), "reason": decision.get("reason", ""),
                "notes": decision.get("notes", "")}
    except subprocess.TimeoutExpired:
        return {"batch_id": batch_id, "ok": False, "error": f"timed out after {BATCH_TIMEOUT_S}s"}
    finally:
        for f in files:
            f.unlink(missing_ok=True)


def worker(ids):
    for b in ids:
        result = run_one(b)
        with LOCK:
            JOB["results"].append(result)
    with LOCK:
        JOB["running"] = False


class Handler(BaseHTTPRequestHandler):
    server_version = "ShelflifeLocal"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, self.path))

    def reply(self, code, body, ctype="application/json"):
        raw = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def error(self, code, message):
        self.reply(code, json.dumps({"error": message}))

    def guarded(self):
        """Only this computer's own page may talk to the server (it spends API credit)."""
        if self.headers.get("Host", "") not in (f"127.0.0.1:{PORT}", f"localhost:{PORT}"):
            self.error(403, "bad host")
            return False
        if self.path != "/" and self.headers.get("X-Requested-With") != "shelflife":
            self.error(403, "missing header")
            return False
        origin = self.headers.get("Origin")
        if origin and origin not in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"):
            self.error(403, "bad origin")
            return False
        return True

    def do_GET(self):
        if not self.guarded():
            return
        if self.path == "/":
            self.reply(200, render_page(build_data(), live=True), "text/html")
        elif self.path == "/data.json":
            self.reply(200, json.dumps(build_data()))
        elif self.path == "/status":
            with LOCK:
                self.reply(200, json.dumps({
                    "running": JOB["running"], "total": JOB["total"], "results": JOB["results"],
                    "key_set": bool(os.environ.get("ANTHROPIC_API_KEY")), "max_batches": MAX_BATCHES}))
        else:
            self.error(404, "not found")

    def do_POST(self):
        if not self.guarded():
            return
        if self.path != "/run":
            return self.error(404, "not found")
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return self.error(400, "ANTHROPIC_API_KEY is not set for this server")
        try:
            length = int(self.headers.get("Content-Length", "0"))
            ids = json.loads(self.rfile.read(length) or b"{}").get("batches", [])
        except (ValueError, AttributeError):
            return self.error(400, "invalid request")
        ids = list(dict.fromkeys(str(i).strip().upper() for i in ids))
        if not ids or len(ids) > MAX_BATCHES:
            return self.error(400, f"give 1 to {MAX_BATCHES} batch IDs")
        bad = [i for i in ids if not ID_RE.match(i)]
        if bad:
            return self.error(400, f"not a batch ID: {bad[0]}")
        unknown = [i for i in ids if i not in known_batches()]
        if unknown:
            return self.error(400, f"{unknown[0]} is not in inventory_clean.csv")
        with LOCK:
            if JOB["running"]:
                return self.error(409, "a run is already in progress")
            JOB.update(running=True, total=len(ids), results=[])
        threading.Thread(target=worker, args=(ids,), daemon=True).start()
        self.reply(200, json.dumps({"started": ids}))


def main():
    global PORT
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    PORT = a.port
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Note: ANTHROPIC_API_KEY is not set here, so the page can show results but cannot run batches.")
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Shelf-Life Clock live dashboard: http://127.0.0.1:{PORT}   (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
