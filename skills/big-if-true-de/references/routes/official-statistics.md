# Route: amtliche Statistik

Bevölkerung, Arbeitslosigkeit, Kriminalität, Migration, Gesundheit,
Wahlen, Haushalte, Handel, Emissionen. Jedes Land veröffentlicht diese
Zahlen; die Aufgabe ist, die Stelle zu erreichen, die die Zahl erhebt,
in ihrer eigenen Veröffentlichung, statt der Kopie eines Aggregators.
(Markt- und Makroreihen mit API, also Renditen, Inflation, Schulden,
BIP, stehen in markets-economy.md.)

## Wo die Zahl entsteht

| Art der Zahl | Erzeuger |
|---|---|
| Arbeitsmarkt, Preise, BIP, Handel (jedes Land) | das nationale Statistikamt: Destatis und die Statistischen Landesämter, Bundesagentur für Arbeit (Arbeitsmarkt), Statistik Austria, BFS (Schweiz), BLS, BEA und Census (USA), ONS (GB), INSEE, ISTAT, INE, Statistics Canada, ABS, Stats NZ, e-Stat (Japan), NBS (China), MOSPI (Indien), IBGE (Brasilien) … sonst „<Land> statistics office“ suchen |
| Ländervergleiche | Eurostat (EU), OECD (Mitglieder), World Bank Open Data (api.worldbank.org, ohne Schlüssel), IWF WEO, UN Data, ILOSTAT; und nenne die Quelle, denn die Definitionen unterscheiden sich |
| Wahlen | Bundeswahlleiterin und Landeswahlleitungen; sonst Wahlkommission oder Innenministerium; in den USA die Secretaries of State und die FEC; eine Nachrichtenagentur für Hochrechnungen |
| Kriminalität | Polizeiliche Kriminalstatistik (BKA) und Strafverfolgungsstatistik (Destatis); FBI Crime Data Explorer (USA), ONS/Home Office (England und Wales), Eurostat; polizeilich „erfasste“ Fälle ≠ in Befragungen „erlebte“ Kriminalität, und die PKS zählt Verdachtsfälle, keine Verurteilungen |
| Migration, Asyl | BAMF, Ausländerzentralregister über Destatis, Eurostat-Datensätze migr_, UNHCR-Datenportal, DHS/CBP (USA), Home Office (GB) |
| Gesundheit | Robert Koch-Institut, Gesundheitsberichterstattung des Bundes (gbe-bund.de), WHO GHO, OECD Health, nationale Gesundheitsministerien, CDC WONDER, ECDC |
| Klima, Emissionen, Energie | Umweltbundesamt, AG Energiebilanzen, Bundesnetzagentur (SMARD), EIA (USA, `marketdata.py eia`), IEA, Our World in Data (ein kuratierter Aggregator, der seine Quelle nennt: folge dem Link), Copernicus, NOAA, nationale Inventare an die UNFCCC |
| Öffentliche Finanzen, Haushalte | Bundesfinanzministerium und Finanzministerien, Bundesrechnungshof, Stabilitätsrat; CBO, OBR, IFS; Eurostat-Datensätze gov_ |
| Entwicklung, Armut | Weltbank PovcalNet/PIP, UNDP HDR |

## Methode

1. Bestimme die genaue Statistik: die Reihe, den Zeitraum, die
   Definition (Gesamt- oder Kernrate, saisonbereinigt oder nicht, brutto
   oder netto, pro Kopf oder insgesamt). Die meisten „falschen“ Zahlen
   sind richtige Zahlen für eine andere Definition.
2. Ruf die Veröffentlichung oder die Tabelle ab; viele Ämter bieten CSV
   oder eine API (Eurostat und EZB über `marketdata.py`; die Weltbank
   unter api.worldbank.org/v2/country/CODE/indicator/INDICATOR?format=json;
   Destatis über GENESIS-Online, die meisten anderen als herunterladbare
   Tabellen; den Browser für interaktive Datenportale).

## Fallen

- Haushaltsjahre, Kalenderjahre und gleitende zwölf Monate.
- Ranglisten („der höchste Wert in Europa“) hängen davon ab, welche
  Länder die Quelle einbezieht; nenne die Liste.
- Datenaggregatoren sind bequem, aber sekundär; hängt ein Urteil an einer
  Zahl, zitiere den Erzeuger.
- Prozent und Prozentpunkte.
