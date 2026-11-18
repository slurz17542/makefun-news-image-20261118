"""Validate entry.png against the competition gate: whole PNG, <=1 MiB, <=1024x1024."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(HERE, "entry.png")
data = open(path, "rb").read()
ok = True

if data[:8] != b"\x89PNG\r\n\x1a\n":
    print("FAIL: not a PNG"); ok = False
w, h = struct.unpack(">II", data[16:24])
print(f"dimensions: {w}x{h}")
if w > 1024 or h > 1024:
    print("FAIL: larger than 1024x1024"); ok = False
print(f"bytes: {len(data)} (limit 1048576)")
if len(data) > 1048576:
    print("FAIL: larger than 1 MiB"); ok = False
# IEND must be the last 12 bytes
if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
    print("FAIL: missing IEND trailer"); ok = False
print("VALID" if ok else "INVALID")
sys.exit(0 if ok else 1)
