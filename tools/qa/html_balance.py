#!/usr/bin/env python3
"""
Cheap structural check for hand-edited HTML: tags balance, ids are unique, and no
visible 'undefined' / 'null' / 'NaN' / '{{' leaked into the text.

    python3 tools/qa/html_balance.py nashiktourism/blog/foo/index.html [...]
Exit 1 if anything is wrong.
"""
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.text, self.skip = [], [], {}, [], 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            if d["id"] in self.ids:
                self.errors.append("duplicate id %r (line %d)" % (d["id"], self.getpos()[0]))
            self.ids[d["id"]] = 1
        if tag in ("script", "style"):
            self.skip += 1
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append("unexpected </%s> at line %d (open: %s)" % (tag, self.getpos()[0], self.stack[-1] if self.stack else None))
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
        else:
            self.stack.pop()

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def check(path):
    p = P()
    src = open(path, encoding="utf-8").read()
    p.feed(src)
    errs = list(p.errors)
    for tag, line in p.stack:
        errs.append("<%s> opened at line %d never closed" % (tag, line))
    body = " ".join(p.text)
    for bad in ("undefined", "NaN", "{{", "}}", "[object"):
        if bad in body:
            errs.append("visible text contains %r" % bad)
    if re.search(r"\bnull\b", body):
        errs.append("visible text contains 'null'")
    return errs


if __name__ == "__main__":
    bad = 0
    for f in sys.argv[1:]:
        errs = check(f)
        print(("OK   " if not errs else "FAIL ") + f)
        for e in errs[:12]:
            print("      " + e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)
