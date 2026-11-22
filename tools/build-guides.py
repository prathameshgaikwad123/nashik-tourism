#!/usr/bin/env python3
"""
Build the generated guides: the Nashik <-> Trimbakeshwar distance hub, the two transport
guides, and Bhandardara. Content lives in tools/guides/*.py and reads its figures from
data/distances.json, data/facts.json and data/sources.json.

    python3 tools/build-guides.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides import distance_hub  # noqa: E402

MODULES = [distance_hub]
for name in ("station_to_trimbak", "trimbak_to_ramkund", "bhandardara"):
    try:
        MODULES.append(__import__("guides." + name, fromlist=["build"]))
    except ModuleNotFoundError as exc:
        if exc.name != "guides." + name:
            raise

if __name__ == "__main__":
    for m in MODULES:
        m.build()
        print("built %s" % m.PATH)
