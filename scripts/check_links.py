#!/usr/bin/env python3
"""Check that every link and asset under /blog/ in the built site exists.

Covers href, src, srcset, data-index and content attributes in HTML, url()
references in CSS, and <loc>/<link> entries in sitemaps and feeds. Links to
the main site (other paths on contensi.com) are outside this repo and are not
checked.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

PUBLIC = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
SITE = "https://contensi.com"
PREFIX = "/blog/"

VALUE = r'(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'>]+))'
HTML_REFS = re.compile(r'\s(href|src|data-index|srcset|content)=' + VALUE)
CSS_REFS = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')
XML_REFS = re.compile(r"<(?:loc|link)>([^<]+)</(?:loc|link)>|href=\"([^\"]+)\"")


def page_url(file):
    rel = file.relative_to(PUBLIC).as_posix()
    return f"{SITE}{PREFIX}{rel}"


def target(path):
    file = PUBLIC / unquote(path[len(PREFIX):])
    return file / "index.html" if path.endswith("/") or file.is_dir() else file


def refs(file):
    text = file.read_text(encoding="utf-8")
    if file.suffix == ".html":
        for name, *quoted in HTML_REFS.findall(text):
            value = next(v for v in quoted if v) if any(quoted) else ""
            if name == "srcset":
                yield from (part.split()[0] for part in value.split(",") if part.strip())
            elif name != "content" or value.startswith(("http://", "https://")):
                yield value
        yield from CSS_REFS.findall(text)
    elif file.suffix == ".css":
        yield from CSS_REFS.findall(text)
    elif file.suffix == ".xml":
        for loc, href in XML_REFS.findall(text):
            yield loc or href


def main():
    broken, checked = set(), 0
    files = [f for f in PUBLIC.rglob("*") if f.suffix in (".html", ".css", ".xml")]
    if not files:
        sys.exit(f"no built pages in {PUBLIC}")
    for file in files:
        for ref in refs(file):
            ref = ref.replace("&amp;", "&").strip()
            if ref.startswith(("data:", "mailto:", "tel:", "#")):
                continue
            url = urlparse(urljoin(page_url(file), ref))
            if url.scheme not in ("http", "https") or url.netloc != "contensi.com":
                continue
            if not url.path.startswith(PREFIX):
                continue
            checked += 1
            if not target(url.path).exists():
                broken.add(f"{file.relative_to(PUBLIC)} -> {ref}")
    for line in sorted(broken):
        print(line)
    if broken:
        sys.exit(f"{len(broken)} broken references")
    print(f"{checked} references checked, all resolve")


if __name__ == "__main__":
    main()
