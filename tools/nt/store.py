"""Reading and writing /data, plus the one definition of "now".

Every date the site shows is computed against `now()`. Setting NT_NOW (an ISO
timestamp) pins it, so builds are reproducible and expiry/lifecycle logic can be
tested without waiting for the calendar.
"""
import datetime as dt
import json
import os

from .paths import DATA

IST = dt.timezone(dt.timedelta(hours=5, minutes=30), "IST")


def now():
    pinned = os.environ.get("NT_NOW")
    if pinned:
        return parse_dt(pinned)
    return dt.datetime.now(IST)


def today():
    return now().date()


def parse_dt(value, end_of_day=False):
    """Accept 'YYYY-MM-DD' or a full ISO timestamp; always return aware IST time.

    A bare date means the whole of that day in India: midnight when it marks a
    start, 23:59:59 when `end_of_day` is set (used for expiry, so "expires on
    10 Oct" keeps the item live through 10 Oct).
    """
    if value is None or value == "":
        return None
    if isinstance(value, dt.datetime):
        return value if value.tzinfo else value.replace(tzinfo=IST)
    s = str(value).strip()
    if len(s) == 10:
        d = dt.date.fromisoformat(s)
        t = dt.time(23, 59, 59) if end_of_day else dt.time(0, 0)
        return dt.datetime.combine(d, t, tzinfo=IST)
    parsed = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=IST)


def is_date(value):
    try:
        dt.date.fromisoformat(str(value))
        return len(str(value)) == 10
    except (TypeError, ValueError):
        return False


def is_datetime(value):
    try:
        parse_dt(value)
        return True
    except (TypeError, ValueError):
        return False


def path(name):
    return os.path.join(DATA, name + ".json")


def load(name, default=None):
    p = path(name)
    if not os.path.isfile(p):
        if default is not None:
            return default
        raise FileNotFoundError("data/%s.json is missing" % name)
    with open(p, encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError as exc:
            raise SystemExit("data/%s.json is not valid JSON: %s" % (name, exc))


def dump(name, obj):
    """Stable, diff-friendly output: 2-space indent, UTF-8, trailing newline."""
    os.makedirs(os.path.dirname(path(name)), exist_ok=True)
    with open(path(name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
