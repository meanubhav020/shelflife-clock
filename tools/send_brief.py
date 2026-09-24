import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True)
    args = parser.parse_args()

    body_path = Path(args.body_file)
    if not body_path.is_absolute():
        body_path = ROOT / body_path
    body_text = body_path.read_text(encoding="utf-8")

    outbox = ROOT / "outbox"
    outbox.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_subject = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in args.subject).strip()
    safe_subject = safe_subject.replace(" ", "_")[:60] or "message"
    out_path = outbox / f"{timestamp}_{safe_subject}.txt"

    out_path.write_text(
        f"To: {args.to}\nSubject: {args.subject}\n\n{body_text}\n",
        encoding="utf-8",
    )
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
