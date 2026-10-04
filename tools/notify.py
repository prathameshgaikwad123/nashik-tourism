#!/usr/bin/env python3
"""
Send a short notification to a chat webhook (Slack, Teams and Discord all accept {"text": ...}).

    NOTIFY_WEBHOOK_URL=https://hooks.example/... python3 tools/notify.py --file summary.md
    python3 tools/notify.py --message "3 candidates need review"

A no-op (exit 0) when NOTIFY_WEBHOOK_URL is not set, so the workflows can call it
unconditionally. The URL is a secret: it is read from the environment only and is
never printed or written anywhere.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--message")
    ap.add_argument("--file")
    a = ap.parse_args()
    url = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not url:
        print("NOTIFY_WEBHOOK_URL not set; nothing sent")
        return 0
    text = a.message or (open(a.file, encoding="utf-8").read() if a.file else "")
    if not text.strip():
        print("empty message; nothing sent")
        return 0
    req = urllib.request.Request(url, data=json.dumps({"text": text[:3500]}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print("notification sent (HTTP %d)" % r.status)
    except (urllib.error.URLError, OSError) as e:
        print("notification failed: %s" % getattr(e, "reason", e))
    return 0


if __name__ == "__main__":
    sys.exit(main())
