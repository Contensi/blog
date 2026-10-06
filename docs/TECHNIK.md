# Technik

Für alle, die am Blog selbst arbeiten: Theme, Build, Hosting. Wie man Beiträge schreibt, steht in der [README](../README.md).

## Vorschau

```bash
hugo server --baseURL http://localhost:1313/blog/ --appendPort=false
```

Danach http://localhost:1313/blog/ öffnen. Unter `http://localhost:1313/` selbst gibt es nichts, weil der Blog wie in Produktion unter `/blog/` liegt.

## Veröffentlichung

- Jeder Pull Request baut die Seite und prüft alle internen Links und Dateien (`scripts/check_links.py`). Das ist der Check `build`.
- Nach dem Merge in `main` veröffentlicht GitHub Actions die Seite auf GitHub Pages unter `contensi.github.io/blog/`.
- Der Cloudflare Worker in `worker/` beantwortet `contensi.com/blog/*` und holt denselben Pfad von GitHub Pages. Besucher bleiben dadurch auf contensi.com. Der Workflow `worker` deployt ihn, wenn sich Dateien in `worker/` ändern.
- Cloudflare-Weiterleitungen schicken die alten Adressen (`/blog-<slug>`, `/blog-en`) auf die neuen.

## Kopf- und Fußzeile

Kopf- und Fußzeile übernehmen Markup und Styles von contensi.com. Wenn sich die Kopfzeile der Hauptseite ändert:

```bash
python3 scripts/vendor_site_css.py
```

Das erzeugt `themes/contensi/assets/css/site-chrome.css` neu und lädt Schriften und Logo von der Live-Seite. Die Navigationseinträge stehen in `data/nav.yaml`.

## Ansprechpartner

Personen für den Kontaktkasten unter jedem Beitrag stehen in `data/contacts.yaml`, Fotos in `assets/img/team/`. Fotos werden beim Build auf 96 und 192 Pixel verkleinert.

## Schriften

Work Sans und Comfortaa stammen von der Hauptseite. Commit Mono steht unter der SIL Open Font License, siehe `themes/contensi/static/fonts/commit-mono-LICENSE.txt`.
