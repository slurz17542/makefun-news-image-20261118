"""Render index.html to entry.png at exactly 1024x1024 with headless Chromium.

Build-time tool only: it produces the entry image that main.ts ships.
Usage: python3 render.py  (run from the entry repository directory)
"""
import hashlib
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/.venv-shot/lib/python3.12/site-packages")

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/meta-chromium/chrome"
DOMAINS_FILE = "/var/lib/hatch-browser/rootfs-base/usr/share/hatch/chromium/webgl-allowed-domains.txt"
with open(DOMAINS_FILE, "rb") as f:
    domains_sha256 = hashlib.sha256(f.read()).hexdigest()

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROME,
        args=[
            f"--hatch-webgl-allowed-domains-file={DOMAINS_FILE}",
            f"--hatch-webgl-allowed-domains-sha256={domains_sha256}",
            "--ignore-certificate-errors",
            "--disable-http2",
            "--disable-quic",
            "--no-sandbox",
            "--disable-gpu",
        ],
    )
    page = browser.new_page(viewport={"width": 1024, "height": 1024})
    page.goto("file://" + os.path.join(HERE, "index.html"))
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(HERE, "entry.png"))
    browser.close()

size = os.path.getsize(os.path.join(HERE, "entry.png"))
print(f"entry.png: {size} bytes (limit 1048576)")
