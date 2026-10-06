# Contensi Blog

Hier liegen alle Beiträge von [contensi.com/blog](https://contensi.com/blog/). Jeder Beitrag ist eine Textdatei. Wer einen Beitrag ändert oder neu anlegt, schlägt das als **Pull Request** vor (kurz PR, ein Änderungsvorschlag). Nach der Freigabe erscheint der Beitrag nach wenigen Minuten online.

Git-Kenntnisse brauchst du nicht. Am einfachsten lässt du deinen KI-Agenten die Arbeit machen.

## Einmalig: Zugang einrichten

1. Lass dir vom Admin Schreibrechte auf dieses Repository geben.
2. Erstelle auf GitHub einen Zugangsschlüssel (Token), der nur für dieses Repository gilt:
   - Rechts oben auf dein Profilbild → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**
   - **Resource owner:** Contensi
   - **Expiration:** 90 Tage
   - **Repository access:** Only select repositories → `Contensi/blog`
   - **Permissions:** Contents → *Read and write*, Pull requests → *Read and write*
   - **Generate token**, dann den Token kopieren. GitHub zeigt ihn nur einmal an.
3. Übergib den Token deinem KI-Agenten, zum Beispiel als Umgebungsvariable `GH_TOKEN`. Schreib ihn nie in eine Datei im Repository und nie in einen Beitrag.

Läuft der Token ab, erstellst du einfach einen neuen.

## Einen Beitrag veröffentlichen

Gib deinem KI-Agenten den Text (oder Stichpunkte) und diesen Auftrag:

> Lege im Repository Contensi/blog einen neuen Blogbeitrag an. Halte dich an das Format in der README. Erstelle die deutsche und die englische Fassung, arbeite auf einem neuen Branch und öffne einen Pull Request gegen `main`.

Danach:

1. Der Agent öffnet den PR. GitHub prüft automatisch, ob die Seite fehlerfrei baut (Check **build**).
2. Eine zweite Person liest den PR und gibt ihn frei.
3. Nach dem Merge ist der Beitrag nach wenigen Minuten online.

## Format eines Beitrags

Jeder Beitrag ist ein eigener Ordner in `content/posts/`. Der Ordnername ist die Adresse des Beitrags.

```
content/posts/proxmox-backup-2026/
├── index.de.md        deutscher Text
├── index.en.md        englischer Text
└── titelbild.jpg      optional: Bilder des Beitrags
```

Daraus werden `contensi.com/blog/proxmox-backup-2026/` und `contensi.com/blog/en/proxmox-backup-2026/`.

**Ordnername:** nur Kleinbuchstaben, Ziffern und Bindestriche, keine Umlaute. Also `digitale-souveraenitaet-2026`, nicht `Digitale Souveränität`.

**Kopfbereich:** Jede Datei beginnt mit einem Block zwischen zwei `---`-Zeilen:

```markdown
---
title: "Proxmox Backup Server 4: Was sich für Backups ändert"
date: 2026-10-15
author: "Nicola Anastassia"
description: "Ein bis zwei Sätze für Suchmaschinen."
summary: "Ein bis zwei Sätze als Vorschau in der Beitragsliste."
contact: daniel-heitmann
logo: proxmox-logo.svg
sources: "Proxmox Server Solutions GmbH, Release Notes (Oktober 2026)."
---

Der erste Absatz führt ins Thema ein.

## Erste Zwischenüberschrift

Text …
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `title` | ja | Überschrift des Beitrags |
| `date` | ja | Datum im Format `JJJJ-MM-TT`. Heute oder früher: Beiträge mit Datum in der Zukunft erscheinen nicht. |
| `author` | ja | Name der Autorin oder des Autors |
| `description` | ja | Text für Google und Vorschauen beim Teilen |
| `summary` | ja | Vorschautext auf der Blog-Startseite |
| `contact` | ja | Ansprechpartner im Kasten unter dem Beitrag: `daniel-heitmann`, `guido-serra`, `jens-peter-reincke`, `knut-ahlers`, `moataz-elmasry` oder `sebastian-lehninger` |
| `image` | nein | Foto im Ordner, das auf der Startseite erscheint, solange der Beitrag der neueste ist |
| `logo` | nein | Herstellerlogo im Ordner (am besten SVG), erscheint neben dem Beitrag in der Liste |
| `sources` | nein | Quellenangabe unter dem Beitrag |
| `draft` | nein | `true` hält den Beitrag unveröffentlicht |

**Text:** normales Markdown.

- Zwischenüberschriften mit `## ` (zwei Rauten). Sie werden automatisch nummeriert und bilden das Inhaltsverzeichnis. Keine `# `-Überschrift im Text, der Titel kommt aus `title`.
- Aufzählungen mit `- `, Hervorhebungen mit `**fett**`.
- Links auf die Hauptseite ohne Domain: `[Proxmox-Seite](/proxmox)`, im englischen Text `[Proxmox page](/proxmox-en)`.
- Bild mit Bildunterschrift:
  `{{< figure src="titelbild.jpg" alt="Was auf dem Bild zu sehen ist" caption="Bildunterschrift" >}}`

**Deutsch und Englisch:** Beide Fassungen haben dieselbe Struktur, also dieselben Zwischenüberschriften, Aufzählungen, Bilder und Felder im Kopfbereich. Nur der Text ist übersetzt.

## Vorher prüfen

- [ ] Ordnername in Kleinbuchstaben mit Bindestrichen
- [ ] `index.de.md` und `index.en.md` vorhanden, gleich aufgebaut
- [ ] alle Pflichtfelder ausgefüllt, Datum nicht in der Zukunft
- [ ] Bilder und Logos liegen im Beitragsordner
- [ ] Check **build** im PR ist grün

Technische Details zu Theme, Build und Hosting stehen in [docs/TECHNIK.md](docs/TECHNIK.md).
