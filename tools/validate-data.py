#!/usr/bin/env python3
"""
Validate every file in /data against the editorial rules (tools/nt/validate.py).

    python3 tools/validate-data.py            # exit 1 on any error
    python3 tools/validate-data.py --strict   # warnings fail too

Run by tools/build-all.py before anything is generated, and by CI on every push,
so a record that breaks the verification policy never reaches the site.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import validate  # noqa: E402


def main():
    r = validate.validate_all()
    for w in r.warnings:
        print("  warn  " + w)
    for e in r.errors:
        print("  ERROR " + e)
    print("\ndata validation: %d error(s), %d warning(s)" % (len(r.errors), len(r.warnings)))
    if r.errors or ("--strict" in sys.argv and r.warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
