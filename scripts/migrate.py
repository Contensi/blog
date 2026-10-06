#!/usr/bin/env python3
"""One-off import of the blog posts from the former contensi.com blog pages."""
import html
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

SITE = "https://contensi.com/"
ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"
TEAM = ROOT / "static" / "img" / "team"
UA = {"User-Agent": "contensi-blog-migrate/1.0"}

MAIN_SITE_PAGE = re.compile(r'href="(?!https?:|mailto:|tel:|#|/)([a-z0-9-]+)\.html(#[^"]*)?"')
BLOG_PAGE = re.compile(r'href="blog-(?:([a-z0-9-]+?)(-en)?|en)\.html"')


def fetch(path):
    with urllib.request.urlopen(urllib.request.Request(SITE + path, headers=UA)) as r:
        return r.read()


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def tiles(index_html):
    for m in re.finditer(r'<a class="blog-kachel" href="blog-([a-z0-9-]+?)(?:-en)?\.html">(.*?)</a></li>', index_html, re.S):
        slug, body = m.groups()
        datum = text(re.search(r'beitrag-datum">(.*?)</span>', body, re.S).group(1))
        day, author = [s.strip() for s in datum.split("·")]
        d, mth, y = day.split(".")
        logo = re.search(r'blog-kachel-logo"><img src="assets/img/([^"]+)"', body)
        image = re.search(r'<img class="blog-kachel-bild" src="assets/img/([^"]+)"', body)
        yield slug, {
            "date": f"{y}-{mth}-{d}",
            "author": author,
            "summary": text(re.search(r'beitrag-text">(.*?)</p>', body, re.S).group(1)),
            "logo": logo.group(1) if logo else None,
            "image": image.group(1) if image else None,
        }


def rewrite_links(fragment):
    def blog(m):
        slug, en = m.group(1), m.group(2)
        if slug is None:
            return 'href="/blog/en/"'
        return f'href="/blog/{"en/" if en else ""}{slug}/"'
    fragment = BLOG_PAGE.sub(blog, fragment)
    return MAIN_SITE_PAGE.sub(lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', fragment)


def to_markdown(fragment):
    result = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none", "--shift-heading-level-by=-2"],
        input=fragment, capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def yaml_str(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def contact_id(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def post(slug, lang, meta, contacts):
    page = fetch(f"blog-{slug}{'-en' if lang == 'en' else ''}").decode("utf-8")
    title = text(re.search(r'<section class="seitenkopf">.*?<h1>(.*?)</h1>', page, re.S).group(1))
    description = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', page).group(1))
    body = re.search(r'<div class="doc-body"[^>]*>(.*?)</div>\s*<p style="margin-top:2rem;">', page, re.S).group(1)

    sources = None
    note = re.search(r'<p class="note"[^>]*>(.*?)</p>', body, re.S)
    if note:
        sources = re.sub(r"^(Quellen|Sources):\s*", "", text(note.group(1)))
        body = body.replace(note.group(0), "")

    images = re.findall(r'<img[^>]+src="assets/img/([^"]+)"', body)
    body = re.sub(r'src="assets/img/([^"]+)"', r'src="\1"', body)

    person = re.search(
        r'<figure class="p-karte">(?:<img class="p-bild" src="assets/img/([^"]+)")?.*?'
        r'p-name">(.*?)</span><span class="p-rolle">(.*?)</span>',
        page, re.S)
    photo, name, role = person.group(1), text(person.group(2)), text(person.group(3))
    cid = contact_id(name)
    contacts.setdefault(cid, {"name": name, "photo": photo, "role": {}})["role"][lang] = role

    front = [
        "---",
        f"title: {yaml_str(title)}",
        f"date: {meta['date']}",
        f"author: {yaml_str(meta['author'])}",
        f"description: {yaml_str(description)}",
        f"summary: {yaml_str(meta['summary'])}",
        f"contact: {cid}",
    ]
    if meta["image"]:
        front.append(f"image: {meta['image']}")
        images.append(meta["image"])
    if meta["logo"]:
        front.append(f"logo: {meta['logo']}")
        images.append(meta["logo"])
    if sources:
        front.append(f"sources: {yaml_str(sources)}")
    front.append("---")

    bundle = POSTS / slug
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / f"index.{lang}.md").write_text("\n".join(front) + "\n\n" + to_markdown(rewrite_links(body)) + "\n")
    for name in set(images):
        target = bundle / name
        if not target.exists():
            target.write_bytes(fetch(f"assets/img/{name}"))


def write_contacts(contacts):
    TEAM.mkdir(parents=True, exist_ok=True)
    lines = []
    for cid, c in sorted(contacts.items()):
        lines += [f"{cid}:", f"  name: {yaml_str(c['name'])}"]
        if c["photo"]:
            (TEAM / c["photo"]).write_bytes(fetch(f"assets/img/{c['photo']}"))
            lines.append(f"  photo: img/team/{c['photo']}")
        lines.append("  role:")
        lines += [f"    {lang}: {yaml_str(role)}" for lang, role in sorted(c["role"].items())]
    (ROOT / "data" / "contacts.yaml").write_text("\n".join(lines) + "\n")


def main():
    contacts = {}
    for lang, index in (("de", "blog"), ("en", "blog-en")):
        for slug, meta in tiles(fetch(index).decode("utf-8")):
            post(slug, lang, meta, contacts)
            print(f"{lang} {slug}", file=sys.stderr)
    write_contacts(contacts)


if __name__ == "__main__":
    main()
