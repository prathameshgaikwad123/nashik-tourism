#!/usr/bin/env python3
"""
Rewrite the shared chrome of every page from tools/chrome.py.

The site grew with its nav and footer copied inline into thirty-five pages.
They had already drifted: three different footer layouts, four different
mobile-menu link sets, and the same ~1.7 KB of nav JavaScript pasted into
twenty-eight files. This script makes tools/chrome.py the only definition.

WHAT IT TOUCHES — deliberately narrow:
  * the <header> ... </header> block          -> chrome.nav_html(page)
  * the <footer> ... </footer> block          -> chrome.footer_html(page)
  * inline <script> blocks that only carry nav/hamburger/dropdown/reveal
    behaviour, plus <script src="/nav.js">    -> removed, replaced by /site.js
  * adds <script src="/site.js" defer>        -> once, before </body>

WHAT IT NEVER TOUCHES:
  * anything inside <main>, the <head>, page-level <style>, or JSON-LD
  * Google Analytics: pages that carry it keep it, pages that do not stay
    without it. Adding tracking to pages the owner never tagged is not this
    script's call to make.

Behaviour removed from the inline blocks is carried by /site.js: mobile menu,
dropdown toggles, Escape-to-close, nav scroll state, hero zoom-in, scroll
reveal and the contact form submit handler.

Usage:  python3 tools/apply-chrome.py [--check]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))
SKIP = {"nav-template.html"}

HEADER_RE = re.compile(r"<header>.*?</header>", re.S)
FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.S)
NAVJS_RE = re.compile(r'[ \t]*<script src="/nav\.js"[^>]*></script>\n?')
SITEJS_RE = re.compile(r'[ \t]*<script src="/site\.js"[^>]*></script>\n?')
INLINE_RE = re.compile(r"[ \t]*<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>\n?", re.S)


def page_path(full):
    rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel  # 404.html


# ─────────────────────────────────────────────────────────────────────────────
# Which inline scripts may be deleted.
#
# FAIL CLOSED. A script is removed only when every identifier in it appears in
# the vocabulary below — the union of the twenty-four byte-identical nav blocks,
# plus the homepage's hero/reveal/scroll extras and the contact form's submit
# handler, all three of which /site.js now implements.
#
# This matters: blog/is-nashik-worth-visiting/index.html hides fifteen image
# carousels in a block that also carries the nav code, and blog/index.html
# builds its whole card grid in one. A "contains hamburger" heuristic deletes
# both. Token-subset matching keeps them, because initGallery, dotsContainer,
# blogGrid and friends are not in this list.
# ─────────────────────────────────────────────────────────────────────────────
SAFE_TOKENS = set("""
Close Escape IntersectionObserver Open String a add addEventListener aria
body btn chevron classList click closeDd const contains controls
document e el expanded fade false focus forEach function
getAttribute getElementById hamburger hb hidden if isIntersecting isOpen key
keydown label menu mm mobileMenu new null observe open
openDd overflow preventDefault querySelectorAll remove return setAttribute setMenu style
target threshold toggle true up var visible x
Anything CSS Dropdowns Hero LCP Mobile Observing Scroll above
accessible adds already and at away browser buttons complete
decoded elements else entries entry every explicit fold for
getBoundingClientRect handles has hash heroImg hover image in including
innerHeight io is keyboard landing leave load loaded mainNav
markLoaded nav observer once one or passive past position
px restored reveal rootMargin scroll scrollY scrolled shared shown
straight stuck the them this those top touch unobserve
window within would zoom
Accept Form FormData Formspree Message Nav Network POST Please
Send Sending Something action again alert application async await
block catch contactForm disabled display error fetch form
formSuccess handler headers json method none ok querySelector res
submit success textContent try went with works wrong
""".split())

IDENT_RE = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")

skipped = []


def is_chrome_script(body, page):
    """True only for boilerplate /site.js provably replaces."""
    if "documentElement.className" in body or '"@context"' in body:
        return False
    if "dataLayer" in body or "gtag(" in body:
        return False
    if "hamburger" not in body or "mobileMenu" not in body:
        return False
    unknown = set(IDENT_RE.findall(body)) - SAFE_TOKENS
    if unknown:
        skipped.append((page, len(body), sorted(unknown)[:8]))
        return False
    return True


def apply(html, page):
    notes = []

    new_header = "<header>\n%s\n</header>" % chrome.nav_html(page)
    html, n = HEADER_RE.subn(lambda _: new_header, html, count=1)
    if n != 1:
        raise SystemExit("ERROR: %s has %d <header> blocks" % (page, n))
    notes.append("header")

    html, n = FOOTER_RE.subn(lambda _: chrome.footer_html(page), html, count=1)
    if n != 1:
        raise SystemExit("ERROR: %s has %d <footer> blocks" % (page, n))
    notes.append("footer")

    html, n = NAVJS_RE.subn("", html)
    if n:
        notes.append("-nav.js")

    removed = []

    def drop(m):
        if is_chrome_script(m.group(1), page):
            removed.append(len(m.group(0)))
            return ""
        return m.group(0)

    html = INLINE_RE.sub(drop, html)
    if removed:
        notes.append("-%d inline script(s), %d bytes" % (len(removed), sum(removed)))

    # One shared, cached behaviour file — inserted once, just before </body>.
    html = SITEJS_RE.sub("", html)
    html = html.replace("</body>", chrome.SITE_JS + "\n</body>", 1)
    notes.append("+site.js")

    # Tidy the blank runs left where inline blocks used to be.
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html, notes


def main():
    check = "--check" in sys.argv
    changed = 0
    for dirpath, _dirs, files in os.walk(ROOT):
        for name in sorted(files):
            if not name.endswith(".html") or name in SKIP:
                continue
            full = os.path.join(dirpath, name)
            page = page_path(full)
            with open(full, encoding="utf-8") as fh:
                before = fh.read()
            after, notes = apply(before, page)
            if after == before:
                continue
            changed += 1
            delta = len(after) - len(before)
            print("  %-56s %+7d  %s" % (page, delta, ", ".join(notes)))
            if not check:
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write(after)
    print("%s %d page(s)" % ("would rewrite" if check else "rewrote", changed))
    if skipped:
        print("\nkept %d inline script(s) — they do more than the shared chrome:" % len(skipped))
        for page, size, sample in skipped:
            print("  %-50s %5d bytes  (%s…)" % (page, size, ", ".join(sample[:5])))


if __name__ == "__main__":
    main()
