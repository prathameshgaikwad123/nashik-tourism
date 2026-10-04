"""AI-assisted extraction and classification of source changes — with a leash.

The monitor (tools/monitor-sources.py) detects that a watched page changed and
hands the new text to `classify`. This module turns it into a *candidate*: a
proposed update that a human must approve. It never publishes anything.

Safeguards, in order:
  1. No API key  -> a plain heuristic candidate with low confidence and a note
     that an editor must read the source. The pipeline still works.
  2. The model is told to use only facts present in the text, to return verbatim
     supporting quotes, and to say `relevant: false` for anything unrelated.
  3. Every quote must appear VERBATIM in the source text. If any does not, or if
     there are none, confidence is capped at 0.2 and the candidate is flagged.
     This is the confidence check that catches a summary the page does not support.
  4. Output is validated against the enums in tools/nt/enums.py; anything
     malformed falls back to the heuristic candidate.
  5. tools/nt/risk.py then assesses the result; high-risk always needs a person.

Configuration (environment only — never committed):
  ANTHROPIC_API_KEY       enables the model call
  NT_CLASSIFIER_MODEL     model id (default: claude-haiku-4-5-20251001)
"""
import json
import os
import re
import urllib.error
import urllib.request

from . import enums

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"

CATEGORY_FOR_SOURCE = {"kumbh": "Kumbh", "government": "Government", "transport": "Transport", "railway": "Railways",
                       "airport": "Airport", "roads": "Roads", "police": "Safety", "tourism": "Tourism",
                       "events": "Events", "weather": "Weather", "attractions": "Tourism", "accommodation": "Accommodation",
                       "accessibility": "Local", "safety": "Safety", "news": "Local"}

PROMPT = """You help an independent Nashik travel-information site triage changes on official and news web pages.

Below is NEW TEXT that appeared on a page since the last check. Source: {source} ({tier}). Decide whether it contains a
concrete, traveller-relevant announcement about Nashik, Trimbakeshwar or the Simhastha Kumbh Mela 2026-28.

Rules — follow exactly:
- Use ONLY facts stated in the NEW TEXT. Do not add background, dates, numbers or names that are not in it.
- If the text is navigation, boilerplate, an unrelated topic, or has no concrete announcement, return {{"relevant": false}}.
- "summary" is 1-3 plain sentences, no marketing language, no speculation.
- "quotes" are 1-3 SHORT passages copied verbatim from the NEW TEXT that support the summary.
- "category" must be one of: {categories}.
- "status" must be one of: developing, confirmed, changed, cancelled. Use "developing" unless the text itself says a decision is final.
- "confidence" is 0 to 1: how sure you are that title+summary are fully supported by the quotes.
Return ONLY a JSON object: {{"relevant": true, "title": "...", "summary": "...", "category": "...", "status": "...", "tags": ["..."], "quotes": ["..."], "confidence": 0.0}}

NEW TEXT:
\"\"\"
{text}
\"\"\"
"""


def heuristic(source, added_text):
    """What we can say without a model: that something changed, and where."""
    first = next((ln.strip() for ln in added_text.splitlines() if len(ln.strip()) > 40), added_text.strip()[:200])
    return {
        "title": "Change detected on %s" % source["name"],
        "summary": first[:280],
        "category": CATEGORY_FOR_SOURCE.get(source.get("category"), "Local"),
        "status": "developing",
        "tags": [],
        "confidence": 0.2,
        "relevant": True,
        "note": "No AI classification configured or it was unusable. The text shown is the first new line on the page; an editor must read the source.",
    }


def _normalise_for_match(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def validate_model_output(out, added_text):
    """Return (clean_dict or None, notes). Enforces the verbatim-quote check."""
    if not isinstance(out, dict):
        return None, "model output was not an object"
    if out.get("relevant") is False:
        return {"relevant": False}, "model judged the change irrelevant"
    notes = []
    title, summary = str(out.get("title") or "").strip(), str(out.get("summary") or "").strip()
    if not title or not summary:
        return None, "missing title or summary"
    category = out.get("category")
    if category not in enums.UPDATE_CATEGORIES:
        return None, "category %r is not allowed" % category
    status = out.get("status") if out.get("status") in enums.UPDATE_STATUS else "developing"
    try:
        conf = max(0.0, min(1.0, float(out.get("confidence"))))
    except (TypeError, ValueError):
        conf = 0.0
    quotes = [q for q in (out.get("quotes") or []) if isinstance(q, str) and q.strip()]
    hay = _normalise_for_match(added_text)
    verbatim = [q for q in quotes if _normalise_for_match(q) in hay]
    if not quotes or len(verbatim) != len(quotes):
        conf = min(conf, 0.2)
        notes.append("quote check failed: %d of %d quotes are not verbatim in the source text" % (len(quotes) - len(verbatim), len(quotes)))
    return {"title": title[:140], "summary": summary[:500], "category": category, "status": status,
            "tags": [str(t)[:30] for t in (out.get("tags") or [])][:6], "confidence": conf, "relevant": True,
            "quotes": verbatim, "note": "; ".join(notes) if notes else None}, "; ".join(notes)


def call_model(prompt, api_key=None, model=None, transport=None):
    """POST to the Messages API. `transport` can be injected for tests."""
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and transport is None:
        return None
    body = json.dumps({"model": model or os.environ.get("NT_CLASSIFIER_MODEL", DEFAULT_MODEL), "max_tokens": 700,
                       "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    if transport is not None:
        return transport(body)
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "content-type": "application/json", "x-api-key": api_key, "anthropic-version": "2023-06-01"})
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    except (urllib.error.URLError, OSError, ValueError):
        return None


def classify(source, tier, added_text, transport=None):
    """Return a dict: relevant, title, summary, category, status, tags, confidence, note."""
    text = added_text.strip()[:6000]
    raw = call_model(PROMPT.format(source=source["name"], tier=tier, categories=", ".join(enums.UPDATE_CATEGORIES), text=text),
                     transport=transport)
    if not raw:
        return heuristic(source, text)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        parsed = json.loads(m.group(0)) if m else None
    except ValueError:
        parsed = None
    clean, note = validate_model_output(parsed, text)
    if clean is None:
        h = heuristic(source, text)
        h["note"] = "Model output rejected (%s). %s" % (note, h["note"])
        return h
    return clean
