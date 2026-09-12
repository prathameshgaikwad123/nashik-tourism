#!/usr/bin/env python3
"""
Shared helpers for everything that reads posts.json.

posts.json stays the single source of truth for the blog. This module only
provides the formatting that tools/build-home-guides.py and tools/build-blog.py
would otherwise each implement — reading time counted from the real article
text, date formatting, Cloudinary delivery transforms and HTML escaping.
Nothing here invents post data.
"""
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))

WPM = 220  # average adult reading speed for web prose

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# Category -> (css class, section id, display heading, one-line standfirst).
# Keys are the exact strings used in posts.json; nothing is renamed there.
CATEGORIES = {
    "Kumbh Mela": ("cat-kumbh", "kumbh-mela", "Kumbh Mela 2027",
                   "Dates, ghats, crowds and what the Simhastha Mela means for a trip to Nashik."),
    "Travel Tips": ("cat-travel", "travel-tips", "Getting There &amp; Around",
                    "Routes, distances and the practical business of moving around Nashik district."),
    "Nashik Guides": ("cat-nashik", "nashik-guides", "Nashik Place Guides",
                      "Individual places in and around the city, covered in depth."),
    "Travel Guide": ("cat-nashik", "travel-guide", "Where to Go",
                     "Wider round-ups across the district."),
    "Planning": ("cat-planning", "planning", "Planning &amp; Budget",
                 "Timing, itineraries, costs and what to pack."),
    "Hotels": ("cat-hotels", "hotels", "Where to Stay",
               "Areas, options and what to book early."),
    "International Travel": ("cat-intl", "international-travel", "Visiting from Abroad",
                             "Guidance for travellers arriving from outside India."),
}

# Display order for the category sections: the biggest, most-linked pillars first.
CATEGORY_ORDER = ["Kumbh Mela", "Nashik Guides", "Travel Guide", "Planning",
                  "Travel Tips", "Hotels", "International Travel"]


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def load():
    with open(os.path.join(ROOT, "posts.json"), encoding="utf-8") as fh:
        return json.load(fh)


def reading_time(slug):
    """Word-count the post's article body. Returns None if it isn't on disk."""
    path = os.path.join(ROOT, "blog", slug, "index.html")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    for pattern in (r"<script.*?</script>", r"<style.*?</style>",
                    r"<head.*?</head>", r"<nav.*?</nav>", r"<footer.*?</footer>"):
        html = re.sub(pattern, " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    words = len(re.sub(r"\s+", " ", text).split())
    return max(1, round(words / WPM))


def fmt_date(iso):
    try:
        y, m, d = (int(x) for x in iso.split("-"))
        return "%d %s %d" % (d, MONTHS[m - 1], y), iso
    except (ValueError, IndexError):
        return iso, iso


def cloudinary(url, transform):
    """Insert Cloudinary delivery transformations into an /upload/ URL."""
    if "res.cloudinary.com" in url and "/upload/" in url:
        head, tail = url.split("/upload/", 1)
        if re.match(r"^[a-z]_", tail):  # already transformed
            return url
        return "%s/upload/%s/%s" % (head, transform, tail)
    if "images.unsplash.com" in url:
        sep = "&" if "?" in url else "?"
        return "%s%sauto=format&fit=crop" % (url, sep)
    return url


def short_title(post):
    """Card titles drop the ' | NashikTourism.com' SEO tail."""
    return esc(post["title"].split("|")[0].strip())


def trim(text, limit=155):
    text = text.strip()
    if len(text) <= limit:
        return esc(text)
    return esc(text[: limit - 3].rsplit(" ", 1)[0]) + "&hellip;"
