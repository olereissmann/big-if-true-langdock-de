# Route: Unternehmen, Pflichtveröffentlichungen und Gerichte

Wem was gehört, wer was verdient hat, wer angeklagt, verklagt, mit
Bußgeld belegt oder verurteilt wurde. Der Beleg ist eine
Pflichtveröffentlichung oder eine Gerichtsakte, und fast immer
öffentlich; die Arbeit besteht darin, das richtige Register für die
Rechtsordnung zu finden.

## Unternehmen

- **Börsennotierte US-Unternehmen:** `python3 scripts/evidence.py edgar '"exakte Wendung"' --from DATUM`
  durchsucht den Volltext aller SEC-Einreichungen seit 2001 und verlinkt
  die Dokumente. Für die eigenen Einreichungen eines Unternehmens: seine
  EDGAR-Seite (sec.gov/cgi-bin/browse-edgar?company=NAME) und die
  XBRL-Reiter „Financial Report“. Umsatz, Beschäftigtenzahl,
  Vorstandsvergütung und Risikofaktoren stehen im 10-K, wesentliche
  Ereignisse in 8-Ks.
- **Großbritannien:** find-and-update.company-information.service.gov.uk
  (Companies House: Organe, Jahresabschlüsse, wirtschaftlich
  Berechtigte; kostenlos, ohne Anmeldung). Charity Commission für
  gemeinnützige Organisationen.
- **EU:** nationale Register, viele kostenlos (Deutschland
  handelsregister.de, unternehmensregister.de und bundesanzeiger.de für
  Abschlüsse; Frankreich infogreffe.fr und pappers.fr; Niederlande
  kvk.nl; Italien registroimprese.it). e-justice.europa.eu verlinkt die
  Register aller Mitgliedstaaten. Österreich: Firmenbuch über
  justiz.gv.at; Schweiz: zefix.ch.
- **Anderswo:** OpenCorporates (opencorporates.com, im Browser; die API
  braucht einen Schlüssel) indexiert Register in über 140 Rechtsordnungen
  und verlinkt die Quelle. Sanktionen: OFAC-Sanktionslistensuche,
  EU-Sanktionskarte, britische OFSI-Liste.
- **Eigentum und Leaks:** ICIJ Offshore Leaks Database
  (offshoreleaks.icij.org), OpenSanctions (opensanctions.org).
- **Zahlen privater Unternehmen** (Bewertung, Umsatz, Entlassungen)
  beruhen meist auf Angaben des Unternehmens selbst oder auf Quellen
  eines Reporters; behandle sie als Zuschreibungen, nicht als Tatsachen.

## Gerichte

- **US-Bundesgerichte:** `evidence.py courtlistener "Partei oder Wendung"`
  durchsucht Urteile (anonymer Zugriff ist gedrosselt); Akten und
  Schriftsätze über CourtListeners RECAP-Archiv und PACER im Browser
  (das Konto der Nutzerin, Bezahlung pro Seite). Supreme Court:
  supremecourt.gov.
- **US-Bundesstaaten:** das Fallsuchportal des jeweiligen Staates, im
  Browser; viele sind kostenlos.
- **Großbritannien:** bailii.org und caselaw.nationalarchives.gov.uk der
  National Archives für Urteile; judiciary.uk für Strafzumessungen.
- **Deutschland:** rechtsprechung-im-internet.de (Bundesgerichte), die
  Websites der Gerichte mit ihren Pressemitteilungen, die
  Landesrechtsprechungsdatenbanken; openjur.de als Index. Viele Urteile
  sind nie veröffentlicht: Dann ist die Pressestelle des Gerichts der
  Weg, und das Urteil bleibt bis dahin could_not_verify.
- **EU:** curia.europa.eu (EuGH), hudoc.echr.coe.int (EGMR),
  eur-lex.europa.eu für Rechtsakte.
- **International:** icj-cij.org, icc-cpi.int.
- **Anderswo:** die eigene Website des Gerichts; WorldLII (worldlii.org)
  indexiert viele. Suche in der Landessprache.

## Aufsichtsbehörden, Bußgelder und Durchsetzung

- SEC (sec.gov/litigation), DOJ (justice.gov/news), FTC, CFPB, FCA
  (fca.org.uk/news), BaFin, Bundeskartellamt, die Wettbewerbs-Pressestelle
  der EU-Kommission, nationale Datenschutzbehörden für DSGVO-Bußgelder
  (der Enforcement Tracker auf enforcementtracker.com ist ein guter
  Index).

## Methode und Fallen

- Angeklagt, Anklage zugelassen, verurteilt, ohne Schuldeingeständnis
  verglichen, mit Bußgeld belegt: Das sind verschiedene Tatsachen.
  Übernimm das Wort des Dokuments. Im deutschen Recht ebenso:
  Ermittlungsverfahren, Anklage, Hauptverfahren, Urteil, rechtskräftig
  oder nicht.
- Die Vorwürfe einer Klage sind Vorwürfe; die Klageschrift beweist, dass
  sie erhoben wurden, mehr nicht.
- Firmennamen: Prüfe die genaue juristische Person; Tochtergesellschaften
  und ähnlich benannte Firmen sind eine häufige Fehlerquelle.
- Währungen und Geschäftsjahre sind unterschiedlich definiert; ein
  „Rekordgewinn“ braucht auf beiden Seiten des Vergleichs dieselbe
  Grundlage.
