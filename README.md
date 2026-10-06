# Contensi blog

Source of [contensi.com/blog](https://contensi.com/blog/). Posts are Markdown files with Hugo front matter. German is the default language at `/blog/`, English is at `/blog/en/`.

## Write a post

```bash
hugo new content posts/my-topic/index.de.md
```

Add the English version as `index.en.md` in the same folder. Images go into that folder too. The folder name is the URL: `/blog/my-topic/` and `/blog/en/my-topic/`.

Front matter:

| Field | Purpose |
|---|---|
| `title` | Headline |
| `date` | Publication date, `YYYY-MM-DD`. The newest post is shown in full on the blog's start page. |
| `author` | Author name |
| `description` | Search engine description |
| `summary` | Teaser in the post list |
| `contact` | Contact person in the call to action, a key from `data/contacts.yaml` |
| `image` / `logo` | Optional picture or logo file in the post folder, shown in the post list |
| `sources` | Optional sources line under the post |
| `draft` | `true` keeps the post unpublished |

An image with a caption: `{{< figure src="photo.jpg" alt="…" caption="…" >}}`.

## Preview

```bash
hugo server --baseURL http://localhost:1313/blog/ --appendPort=false
```

Then open http://localhost:1313/blog/.

## Publish

Open a pull request into `main`. The `build` check builds the site and verifies every internal link. After the merge, GitHub Actions publishes the site to GitHub Pages.

## How it is served

- GitHub Pages hosts the built site at `contensi.github.io/blog/`.
- The Cloudflare Worker in `worker/` answers `contensi.com/blog/*` and fetches the same path from GitHub Pages, so visitors stay on contensi.com. It is deployed by the `worker` workflow when files in `worker/` change.
- Cloudflare redirect rules send the old URLs (`/blog-<slug>`, `/blog-en`) to the new ones.

## Header and footer

The header and footer copy the main site's markup and styles, so the blog looks like part of contensi.com. When the main site's header changes:

```bash
python3 scripts/vendor_site_css.py
```

This regenerates `themes/contensi/assets/css/site-chrome.css` and the fonts and logo from the live site. Navigation entries are in `data/nav.yaml`.

## Fonts

Work Sans and Comfortaa come from the main site. Commit Mono is licensed under the SIL Open Font License, see `themes/contensi/static/fonts/commit-mono-LICENSE.txt`.
