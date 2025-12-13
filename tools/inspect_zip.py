import io
import zipfile
from collections import Counter

import requests

URL = "https://codeload.github.com/thiagobodruk/biblia/zip/refs/heads/master"
print("Downloading", URL)
resp = requests.get(URL, timeout=60)
resp.raise_for_status()
archive = zipfile.ZipFile(io.BytesIO(resp.content))
names = archive.namelist()
print("total entries", len(names))
print("sample entries", names[:20])
by_prefix = Counter(parts[1] if len(parts) > 1 else "" for parts in (name.split("/") for name in names))
print("prefixes", by_prefix.most_common(10))
json_entries = [name for name in names if "/json/" in name.lower()]
print("json samples", json_entries[:20])
