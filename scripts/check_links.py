#!/usr/bin/env python3
"""Check that every internal /blog/ link and asset in the built site exists.

Links to the main site (other paths on contensi.com) are outside this repo
and are not checked.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

PUBLIC = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
PREFIX = "/blog/"
ATTR = re.compile(r'(?:href|src)=["\']?([^"\'\s>]+)')


def target(path):
    file = PUBLIC / unquote(path[len(PREFIX):])
    return file / "index.html" if path.endswith("/") or file.is_dir() else file


def main():
    broken = []
    for page in PUBLIC.rglob("*.html"):
        for ref in ATTR.findall(page.read_text(encoding="utf-8")):
            parsed = urlparse(ref)
            if parsed.netloc in ("", "contensi.com") and parsed.path.startswith(PREFIX):
                if not target(parsed.path).exists():
                    broken.append(f"{page.relative_to(PUBLIC)} -> {ref}")
    for line in sorted(set(broken)):
        print(line)
    if broken:
        sys.exit(f"{len(set(broken))} broken internal links")
    print("all internal links resolve")


if __name__ == "__main__":
    main()
