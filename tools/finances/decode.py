"""Turns a Drive download_file_content result into the original file.

python decode.py SOURCE OUT
SOURCE is either a saved tool-result JSON ({"content": "<base64>", ...}) or a file holding the bare base64 text.
"""
import base64
import json
import sys

src, out = sys.argv[1], sys.argv[2]
raw = open(src).read().strip()
try:
    raw = json.loads(raw)["content"]
except (ValueError, KeyError, TypeError):
    pass
open(out, "wb").write(base64.b64decode(raw))
print("wrote", out)
