#!/usr/bin/env python3
"""Print how many seconds to wait after a rate-limited kilo run.

Usage: retry_after.py <since-epoch-ms> <fallback-seconds>

kilo prints only "Too Many Requests"; the response headers are in its event store
(~/.local/share/kilo/kilo.db). Look at the 429 errors created since <since-epoch-ms>, take the
largest `Retry-After` (delta-seconds or HTTP-date), and print it. When no 429 carries one (the
Nvidia endpoint sends none, checked on 81 responses), print <fallback-seconds>.
"""

import json
import os
import sqlite3
import sys
import time
from email.utils import parsedate_to_datetime

since, fallback = int(sys.argv[1]), int(sys.argv[2])
wait = None
try:
    db = sqlite3.connect("file:" + os.path.expanduser("~/.local/share/kilo/kilo.db") + "?mode=ro", uri=True, timeout=5)
    for (raw,) in db.execute("select data from event where data like '%\"statusCode\":429%' order by rowid desc limit 200"):
        try:
            info = json.loads(raw)["info"]
            if info["time"]["created"] < since:
                continue
            headers = {k.lower(): v for k, v in info["error"]["data"].get("responseHeaders", {}).items()}
            val = headers.get("retry-after")
            if val is None:
                continue
            secs = float(val) if val.strip().isdigit() else parsedate_to_datetime(val).timestamp() - time.time()
            wait = max(wait or 0, secs)
        except (KeyError, ValueError, TypeError, json.JSONDecodeError):
            continue
except sqlite3.Error:
    pass
print(int(min(max(wait, 1), 900)) if wait is not None else fallback)
