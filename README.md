# Big If True, deutsche Fassung für Langdock

Dies ist ein Fork von [Verso-Lab/big-if-true-plugin](https://github.com/Verso-Lab/big-if-true-plugin),
dem Faktencheck-Skill von [Verso](https://verso.ink/), übersetzt und
angepasst von Ole Reissmann für [THEFUTURE](https://olereissmann.com/newsletter/),
einen Newsletter über KI und Journalismus. Die Methode und ihre Regeln
stammen von Verso.

## Warum es diesen Fork gibt

Zwei Gründe: Der Skill soll auf Deutsch arbeiten, und er soll in Langdock
laufen. Manche KI-Plattformen, darunter Langdock, blockieren aus
Sicherheitsgründen JavaScript in HTML-Seiten. Die Originalseite baut sich
mit JavaScript auf und bleibt dort leer.

## Was geändert wurde

- **Alles auf Deutsch.** Die Anleitung (`SKILL.md`), die
  Extraktionsregeln, die Recherche-Routen, die Berichtsseite und die
  Exporte sind übersetzt. Die Urteile heißen Nachprüfen, Nicht
  verifizierbar und Belegt. Technische Werte bleiben englisch, weil die
  Skripte sie lesen: die Urteile `r`, `c`, `s`, die Markierungen `[fact]`
  und `[attribution]`, die Feldnamen in `check.json`.
- **Deutsche Quellen ergänzt.** Die Recherche-Routen nennen zusätzlich
  Destatis, Bundestag, RKI, Handelsregister, deutsche Gerichte und
  Faktenchecker im deutschsprachigen Raum.
- **Die Berichtsseite ist reines HTML mit Fußnoten.** `scripts/assemble.py`
  schreibt die ganze Seite fertig als HTML, ohne JavaScript und ohne
  interaktives CSS. Die einzige Interaktion ist, Links zu folgen:
  - jede geprüfte Stelle im Artikel ist markiert und trägt eine
    Fußnotenzahl; sie führt zu Urteil, Begründung und Quellen der Aussage
    in einer nummerierten Liste unter dem Artikel
  - jeder Eintrag dort führt zurück zu seiner Stelle
  - der farbige Balken oben und die Zeile „Nachprüfen“ führen direkt zu
    den Aussagen
  - der Export-Bereich unten zeigt Markdown, CSV und JSON in Textfeldern
    zum Kopieren, dazu Download-Links, wo die Anzeige sie zulässt
  - weggefallen, weil sie ein Skript oder interaktives CSS brauchen: die
    Filter nach Urteil, der Wechsel Artikel / Aussagen, die aufklappenden
    Notizen, die Kopier-Buttons und die Hover-Effekte
  - die Seite bleibt lesbar, auch wenn eine Anzeige ihre Styles entfernt
- **Der Footer** nennt diese Fassung neben Verso.
- **Dokumentkommentare** sind „von einem KI-Assistenten gepostet“ statt
  „von Claude“, weil in Langdock auch andere Modelle laufen.

Die Seite funktioniert weiterhin auch in Claude, Codex und jedem Browser.

Hinweis: Verso hat die Methode an einem Testset gemessen, die englischen
Anweisungen sind darauf abgestimmt. Die Übersetzung ist nicht gegen
dieses Testset geprüft.

## In Langdock installieren

Den *Inhalt* von `skills/big-if-true-de` zippen, sodass `SKILL.md` direkt
im Wurzelverzeichnis des Archivs liegt, neben `assets/`, `references/` und
`scripts/` (nicht in einem übergeordneten Ordner), und das Zip als Skill
importieren. Für die Berichtsseite braucht der Skill Code-Ausführung; ohne
sie gibt es einen Textbericht.

## Fragen und Fehler

Probleme mit dieser Fassung bitte als Issue in diesem Repository melden,
nicht bei Verso. Probleme mit der Methode selbst meldet man am besten
Verso.

Lizenz: MIT, wie das Original. Die Methode und alle Verdienste daran
gehören Verso.

---

## The original README

*Darunter steht Versos README, unverändert. Die Installationslinks darin
richten die englische Originalfassung ein, nicht diese.*

A fact-checking plugin for Claude by [Verso](https://verso.ink). Give it an
article, a draft, a newsletter or a press release: it finds every checkable
claim, verifies each against primary records and the live web, and delivers
an annotated report where every claim carries a verdict and its sources.

- **Supported**: two independent sources agree, or one definitive source settles it.
- **Couldn't verify**: the evidence doesn't settle it either way.
- **Needs review**: something could be off here. Have a look.

More, including how we tested it: [verso.ink/big-if-true](https://verso.ink/big-if-true).

## Install

**Claude app and Cowork**: find Big If True in the plugin directory under
Customize → Plugins → Discover, or
[add it from this repository](https://claude.ai/customize/plugins/new?marketplace=Verso-Lab/big-if-true-plugin&plugin=big-if-true):
Sync, then Add next to Big If True.

**Claude Code**: add this repository as a marketplace:

```
/plugin marketplace add Verso-Lab/big-if-true-plugin
/plugin install big-if-true@verso
```

Then ask Claude to fact-check something. The plugin needs web search; with
code execution it builds the report page and runs the official-data lookups.

## What it connects to

Big If True needs no accounts or API keys and keeps no data of its own. To
check a text, Claude searches the web and opens the pages the evidence is
on, in the browser when the session has one. It writes its working files and the report page in the session's own
folder. The bundled scripts in `skills/big-if-true/scripts/` only read
public records, and each call sends only the search term, identifier or
data series it looks up:

- `evidence.py`: Internet Archive (archive.org, web.archive.org), Crossref,
  PubMed (NCBI), arXiv, SEC EDGAR, Wikidata and CourtListener.
- `marketdata.py`: FRED, US Treasury (home.treasury.gov and Fiscal Data),
  Yahoo Finance, Bank of England, Bundesbank, ECB, Eurostat, OECD,
  Frankfurter and the US EIA.
- `assemble.py` builds the report page locally and makes no network calls.

## What's in here

`skills/big-if-true/` is the skill: the method (`SKILL.md`), the claim
extraction rules and per-topic evidence routes (`references/`), the report
builder and data lookups (`scripts/`), and the report page (`assets/`).

This repository is published from Verso's development repository at each
release; changes are made there and measured against a test set before they
ship. Feedback and bug reports: [team@verso.ink](mailto:team@verso.ink) or an
issue here.

## Licence

MIT, © 2026 Verso Lab LLC. See [LICENSE](LICENSE).
