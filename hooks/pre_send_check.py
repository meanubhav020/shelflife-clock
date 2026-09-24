import csv
import json
import os
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH_RE = re.compile(r"LF-\d{5}")
SEND_NAME_RE = re.compile(r"(send|reply|forward)", re.IGNORECASE)


def block(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def allow():
    sys.exit(0)


def read_stdin_payload():
    try:
        raw = sys.stdin.read()
        return json.loads(raw)
    except Exception:
        block("Safety check: could not read or understand the tool call input.")


def parse_send_brief_command(command):
    try:
        tokens = shlex.split(command, posix=False)
    except ValueError:
        block("Safety check: could not parse the command being run.")

    def get_flag(name):
        for i, tok in enumerate(tokens):
            if tok == name and i + 1 < len(tokens):
                return tokens[i + 1].strip('"')
        return None

    to_addr = get_flag("--to")
    subject = get_flag("--subject")
    body_file = get_flag("--body-file")

    if to_addr is None or subject is None:
        block("Safety check: could not find --to or --subject in the send_brief.py command.")

    body_text = ""
    if body_file:
        body_path = Path(body_file)
        if not body_path.is_absolute():
            body_path = ROOT / body_path
        try:
            body_text = body_path.read_text(encoding="utf-8")
        except Exception:
            block(f"Safety check: could not read body file {body_file}.")

    return to_addr, subject, body_text


def extract_from_generic_tool_input(tool_input):
    def flatten(obj, out):
        if isinstance(obj, dict):
            for k, v in obj.items():
                flatten(v, out)
        elif isinstance(obj, list):
            for item in obj:
                flatten(item, out)
        elif isinstance(obj, str):
            out.append(obj)

    to_addr = None
    subject = None
    for key in ("to", "recipient", "to_address", "email"):
        if isinstance(tool_input.get(key), str):
            to_addr = tool_input[key]
            break
    for key in ("subject",):
        if isinstance(tool_input.get(key), str):
            subject = tool_input[key]
            break

    strings = []
    flatten(tool_input, strings)
    body_text = "\n".join(strings)

    return to_addr, subject, body_text


def main():
    payload = read_stdin_payload()
    if not isinstance(payload, dict):
        block("Safety check: tool call input was not understood.")

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}

    is_bash = tool_name == "Bash"
    is_send_like = bool(SEND_NAME_RE.search(tool_name or ""))

    if is_bash:
        command = tool_input.get("command", "")
        if "tools/send_brief.py" not in command and "tools\\send_brief.py" not in command:
            allow()
        to_addr, subject, body_text = parse_send_brief_command(command)
    elif is_send_like:
        to_addr, subject, body_text = extract_from_generic_tool_input(tool_input)
        if to_addr is None or subject is None:
            block("Safety check: could not find a recipient and subject for this send.")
    else:
        allow()

    owner_email = os.environ.get("SHELFLIFE_OWNER_EMAIL")
    if not owner_email:
        block("Safety check: SHELFLIFE_OWNER_EMAIL is not set. Blocking the send.")
    if to_addr.strip().lower() != owner_email.strip().lower():
        block(f"Safety check: recipient '{to_addr}' is not the owner's address. Blocking the send.")

    batch_ids = sorted(set(BATCH_RE.findall(body_text)))

    if not batch_ids:
        if subject.strip().upper().startswith("TEST:"):
            allow()
        block("Safety check: message has no batch IDs and its subject does not start with 'TEST:'. Blocking the send.")

    queue_path = ROOT / "action_queue.csv"
    queue = {}
    try:
        with open(queue_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                queue[row["batch_id"]] = row
    except Exception:
        block("Safety check: could not read action_queue.csv.")

    inventory_path = ROOT / "inventory_clean.csv"
    inventory = {}
    try:
        with open(inventory_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                inventory[row["batch_id"]] = row
    except Exception:
        block("Safety check: could not read inventory_clean.csv.")

    sku_path = ROOT / "sku_master.csv"
    sku_master = {}
    try:
        with open(sku_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sku_master[row["sku"]] = row
    except Exception:
        block("Safety check: could not read sku_master.csv.")

    for batch_id in batch_ids:
        row = queue.get(batch_id)
        if row is None:
            block(f"Safety check: batch {batch_id} is not in action_queue.csv. Blocking the send.")
        if row.get("status") != "READY":
            reason = row.get("hold_reason") or f"status is {row.get('status')}"
            block(f"Safety check: batch {batch_id} is not READY ({reason}). Blocking the send.")

        inv_row = inventory.get(batch_id)
        if inv_row is None:
            block(f"Safety check: batch {batch_id} not found in inventory_clean.csv. Blocking the send.")

        trust_flag = inv_row.get("trust_flag")
        if trust_flag != "OK":
            block(f"Safety check: batch {batch_id} has trust_flag {trust_flag}, not OK. Blocking the send.")

        sku_row = sku_master.get(inv_row.get("sku"))
        if sku_row is None:
            block(f"Safety check: SKU for batch {batch_id} not found in sku_master.csv. Blocking the send.")

        if sku_row.get("product_class") == "HEALTHCARE":
            block(f"Safety check: batch {batch_id} is HEALTHCARE per sku_master.csv. Blocking the send.")

        try:
            unit_cost = float(sku_row.get("unit_cost_usd", 0))
            units = float(inv_row.get("units_on_hand", 0))
        except ValueError:
            block(f"Safety check: could not compute value for batch {batch_id}.")
        value = unit_cost * units
        if value > 2000:
            block(f"Safety check: batch {batch_id} value ${value:.2f} is above $2,000. Blocking the send.")

        if row.get("action") == "DISPOSE":
            block(f"Safety check: batch {batch_id} action is DISPOSE. Blocking the send.")

    allow()


if __name__ == "__main__":
    main()
