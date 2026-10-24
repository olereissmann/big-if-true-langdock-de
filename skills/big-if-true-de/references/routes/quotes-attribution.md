# Route: Zitate und Zuschreibungen

„X sagte Y“ ist der häufigste Aussagetyp und der am häufigsten
verfälschte: Worte gestrafft, Kontext weggelassen, falscher Ort, falsches
Datum, oder ein Satz, der nie gefallen ist. Das Urteil hat zwei Teile,
und beide müssen geklärt werden: Wurden diese Worte gesagt (oder
geschrieben), und von dieser Person in diesem Rahmen?

## Wo der Beleg liegt

Geh zur Aufnahme oder zum Transkript, nicht zu anderen Medien, die
zitieren (die Unabhängigkeitsregel in SKILL.md setzt die Messlatte).
Bleibt es bei could_not_verify, nenne die Aufnahme oder die Notizen,
die es klären würden.

| Sprecher / Rahmen | Primärer Beleg |
|---|---|
| Bundestag, Plenum und Ausschüsse | dip.bundestag.de (Plenarprotokolle, Drucksachen), bundestag.de/mediathek mit Zeitmarken |
| Bundesregierung | bundesregierung.de (Mitschriften der Regierungspressekonferenz, Reden, Interviews), die Websites der Ministerien |
| Landtage | die Parlamentsdokumentation des jeweiligen Landtags (Plenarprotokolle) |
| Österreich, Schweiz | parlament.gv.at (Stenographische Protokolle), parlament.ch (Amtliches Bulletin) |
| US-Präsident, Weißes Haus | whitehouse.gov/briefings-statements (Transkripte); das öffentliche Videoarchiv der Sitzungen, durchsuchbar und mit Zeitmarken |
| US-Kongress, Anhörungen, Plenum | congress.gov (Congressional Record), Videokanäle der Ausschüsse |
| Federal Reserve | federalreserve.gov/newsevents (Reden im Volltext, Transkripte der Pressekonferenzen) |
| US-Finanzministerium, Behörden | home.treasury.gov/news, der Newsroom der Behörde |
| Britisches Parlament | hansard.parliament.uk (durchsuchbar, tagesaktuell); parliamentlive.tv |
| Britische Regierung | gov.uk/government/speeches |
| EU-Institutionen | ec.europa.eu/commission/presscorner; ecb.europa.eu/press (Reden, Pressekonferenzen, wörtlich); Europäisches Parlament: europarl.europa.eu (Ausführliche Sitzungsberichte) |
| Andere Parlamente | die meisten veröffentlichen wörtliche Protokolle: Assemblée nationale (assemblee-nationale.fr/dyn/comptes-rendus), Diet (kokkai.ndl.go.jp), Lok Sabha (sansad.in) |
| Zentralbanken, Ministerien anderswo | die Website der Institution, in ihrer Sprache; such in dieser Sprache |
| Erklärungen vor Gericht | das Urteil oder die Akte (siehe companies-courts.md) |
| Führungskräfte von Unternehmen | Transkripte der Telefonkonferenzen zu Quartalszahlen (Investor-Relations-Seite; SEC-8-K-Anhänge über `evidence.py edgar`), Pressemitteilungen |
| Social-Media-Posts | siehe web-social-archives.md: der Post selbst oder sein Archiv |
| Donald Trump auf Truth Social | trumpstruth.org (durchsuchbares Archiv); beweist, dass ein Post existiert, nie, dass er stimmt |
| TV- und Radiointerviews | der eigene Clip oder die Transkriptseite des Senders (Mediatheken von ARD, ZDF, Deutschlandfunk und anderen); meist ist der Browser nötig |
| Podcasts, YouTube | die Folge, im Browser geöffnet, an der Zeitmarke |
| Analystennotizen, Research-Berichte | nicht öffentlich; das Zitat beruht auf dem Reporter: could_not_verify, und sag das klar |
| Interviews des Reporters selbst | beruhen auf dem Reporter: could_not_verify, und sag das klar |

## Methode

1. Such die exakt zitierten Worte in Anführungszeichen, dazu den Namen.
   Dann ein markantes Stück aus vier Wörtern: Paraphrasen verrutschen an
   den Rändern, ein Bruchstück übersteht das.
2. Wenn der Beleg gefunden ist, lies das Umfeld des Zitats: War es
   eingeschränkt, an eine Bedingung geknüpft, eine Frage, oder das Zitat
   eines anderen? Abgeschnittener Kontext ist ein needs_review-Befund,
   auch wenn die Worte exakt stimmen.
3. Gleich den Rahmen ab: Ort, Datum und Form im Text („sagte vor
   Journalisten“, „in einem Fernsehinterview“, „schrieb in einer Notiz“,
   „schrieb auf X“) sind ebenfalls Aussagen. Ein richtiges Zitat am
   falschen Ort ist ein Befund.
4. Titel und Zugehörigkeiten sind eigene Aussagen, geprüft am eigenen
   Beleg der Person: ihre Seite bei der Institution, ihr Lebenslauf,
   `evidence.py wikidata "Name"` als erster Anhaltspunkt, LinkedIn als
   letzter Ausweg; nie daran, ob andere Medien die Bezeichnung
   wiederholen. Eine aktuelle Zugehörigkeit, die der Text weglässt, oder
   ein früherer Titel, der als aktuell dasteht, ist ein Befund, wenn es
   ändert, wie Leser das Zitat gewichten würden. Eine frühere Funktion,
   ein Stipendium, ein Aufsichtsratssitz oder eine lockere Fachangabe
   („Ökonom“, „Analystin“) ist keiner.
5. Übersetzte Zitate: Finde den Beleg in der Originalsprache und beurteile
   die Übersetzung, nicht die Nacherzählung. Ein deutsches Zitat, das
   aus dem Englischen übersetzt ist, wird am englischen Original
   gemessen.

## Fallen

- Zitatsammlungen im Netz sind kein Beleg.
- Ein Transkript von Dritten ist schwächer als das der Institution
  selbst; sag, welches du benutzt hast.
- „Sagte vergangene Woche“ ohne Ort: Erst den Ort finden, dann die Worte.
