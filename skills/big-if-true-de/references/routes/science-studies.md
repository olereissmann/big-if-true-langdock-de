# Route: Studien, Fachaufsätze und wissenschaftliche Aussagen

„Eine Studie hat ergeben …“ verbirgt vier getrennte Aussagen: Die Studie
existiert, sie sagt, was der Text sagt, sie ist die Art Studie, die der
Text nahelegt (begutachtet? Preprint? von der Industrie finanziert? an
Mäusen?), und die zitierte Zahl ist die Zahl der Studie und nicht die
Rundung einer Pressemitteilung.

## Den Aufsatz finden

- `python3 scripts/evidence.py crossref "Titelwörter oder Thema"` liefert
  DOIs, Zeitschriften, Daten und Autoren. `evidence.py doi 10.xxxx/…`
  löst eine DOI auf, die der Text oder eine Pressemitteilung nennt.
- Medizin und Lebenswissenschaften: `evidence.py pubmed "Suchanfrage"`
  (PMIDs, zu öffnen unter pubmed.ncbi.nlm.nih.gov/PMID). Preprints:
  `evidence.py arxiv "Suchanfrage"`; bioRxiv/medRxiv über die Suche oder
  den Browser.
- Klinische Studien: clinicaltrials.gov (Registrierung, Endpunkte,
  Sponsor), das EU-Register CTR und das Deutsche Register Klinischer
  Studien (drks.de). Der registrierte primäre Endpunkt gegenüber dem
  berichteten ist ein klassischer Befund.
- Rückzüge: retractiondatabase.org (Retraction Watch; im Browser) und das
  Feld `update-to` im Crossref-Eintrag. Ein zurückgezogener oder
  korrigierter Aufsatz, der als gültig zitiert wird, ist needs_review.
- Nichts in Crossref, PubMed oder auf den Preprint-Servern, und das
  Medium nennt keine Zeitschrift: Die „Studie“ ist vielleicht eine
  Umfrage, ein Whitepaper eines Unternehmens oder eine Pressemitteilung.
  Sag das.

## Den Aufsatz lesen, nicht die Berichterstattung

- Öffne den Aufsatz (DOI-Link; den Browser, wenn die Zeitschrift den
  Abruf blockiert; den institutionellen Zugang der Nutzerin, falls sie
  einen hat). Lies den Abstract, den Methodenteil und die Tabelle, aus
  der die Zahl stammt.
- Prüfe: Stichprobengröße und Population, Effektgröße mit ihrem
  Intervall, relatives gegenüber absolutem Risiko („verdoppelt das
  Risiko“ von 1 zu 10.000 auf 2 zu 10.000), Korrelation gegenüber
  Kausalität in den eigenen Worten des Aufsatzes, Tier- oder
  In-vitro-Versuch gegenüber Menschen, Finanzierung und Angaben zu
  Interessenkonflikten.
- Pressemitteilungen (Verteilerdienste wie idw, Pressestellen der
  Hochschulen) sind die übliche Quelle von Übertreibung; eine Aussage,
  die zur Mitteilung passt, aber nicht zum Aufsatz, ist ein Befund.

## Zitate von Fachleuten

- Bestätige, dass die Person existiert und die genannte Position innehat
  (Hochschulseite, ORCID auf orcid.org, Google Scholar,
  `evidence.py wikidata`). „Wissenschaftler sagen“ ohne Namen ist nicht
  prüfbar; vermerke das.

## Amtliche Wissenschafts- und Gesundheitsstellen

- WHO, ECDC, RKI, Paul-Ehrlich-Institut, BfArM, CDC, EMA, FDA
  veröffentlichen den Beleg auf ihren eigenen Websites; zieh sie der
  Berichterstattung vor. Statistik: siehe official-statistics.md.

## Fallen

- Zeitschriftennamen, die echte nachahmen; prüfe Verlag und ISSN im
  Crossref-Eintrag.
- Alte Studien, die als neu präsentiert werden; das Crossref-Datum klärt
  es.
- Eine Metaanalyse und eine der Studien darin sind nicht zwei Quellen.
