# Route: Märkte und Wirtschaft

Renditen, Indizes, Öl, Devisen, Inflation, Schulden, BIP. Jede Quelle
unten ist kostenlos, und `scripts/marketdata.py` deckt sie alle ab. Diese
Datei ordnet zu, welche Quelle welche Aussage beantwortet, welche
Reihen-IDs übergeben werden und wo die Fallen liegen. Lies den Abschnitt,
den du brauchst, nicht die ganze Datei.

## Welche Quelle für welche Aussage

| Aussage im Text | Primärquelle | Befehl |
|---|---|---|
| Rendite von US-Staatsanleihen, Schlusskurs des Tages (2/10/30 Jahre) | Treasury Daily Par Yield Curve (amtlich, jeden Nachmittag veröffentlicht) | `treasury`, `treasury --tenor BC_30YEAR` |
| Verlauf der US-Renditen, „höchster Stand seit“ | FRED (Fed H.15, nächster Geschäftstag) | `fred DGS10 --above 4.79` |
| Rendite britischer Gilts, Leitzins der Bank of England, Pfund | Datenbank der Bank of England (täglich seit den 1970ern, etwa 3 Tage Verzug) | `boe IUDMNPY --above 5.26` |
| Rendite der Bundesanleihe | Bundesbank (täglich, am selben Tag) | `bundesbank` |
| Zehnjährige Renditen Japan, Frankreich, Italien, jedes OECD-Land (monatlich) | OECD | `oecd JPN`, `oecd FRA` |
| Indexschluss des Tages, Tageshoch, Futures, Devisen | der kostenlose Chart-Endpunkt hinter dem Befehl `yahoo` (inoffiziell) | `yahoo ^STOXX`, `yahoo ^TNX --field high`, `yahoo BZ=F` |
| Verlauf von S&P 500, Nasdaq, Dow, Nikkei | FRED (lizenziert von S&P/Nikkei, nächster Geschäftstag) | `fred SP500`, `fred NIKKEI225` |
| Brent / WTI Spot | EIA (täglich, etwa eine Woche Verzug) oder FRED-Spiegel | `eia RBRTE`, `fred DCOILBRENTEU --change 2026-02-27` |
| US-Benzin- und Dieselpreise, Henry-Hub-Gas | FRED wöchentlich/täglich | `fred GASREGW`, `fred GASDESW`, `fred DHHNGSP` |
| EUR/USD und andere EZB-Referenzkurse, beliebiges Datum | Frankfurter (EZB-Daten) | `fx EUR USD 2026-02-27` |
| Inflation im Euroraum (endgültig, monatlich) | EZB-Datenportal / Eurostat | `ecb`, `eurostat prc_hicp_manr geo=EA coicop=CP00` |
| Inflation im Euroraum, Schnellschätzung (laufender Monat) | Pressemitteilungsseite der Euro-Indikatoren bei Eurostat (abrufen) | (Seite abrufen) |
| Deutsche Inflation (VPI, HVPI) | Destatis-Pressemitteilung und GENESIS-Online (Tabelle 61111) | (Seite abrufen) |
| US-Verbraucherpreise, PCE | FRED | `fred CPIAUCSL`, `fred PCEPI` |
| US-Bruttostaatsschuld | Treasury Fiscal Data (täglich) | `usdebt` |
| Nominales US-BIP (für die Schuldenquote) | FRED (quartalsweise, annualisiert) | `fred GDP` |
| US-Schuldenquote wie veröffentlicht | FRED | `fred GFDEGDQ188S` |
| EZB-Einlagensatz, Zielspanne der Fed | EZB-Datenportal / FRED | `ecb FM/B.U2.EUR.4F.KR.DFR.LEV`, `fred DFEDTARU` |
| Schulden und BIP Frankreichs, Japans, Großbritanniens, Deutschlands | Veröffentlichungen von INSEE, MOF/Cabinet Office, ONS, Destatis (abrufen) | (Seite abrufen) |

## Kurse vom selben Tag

Der Chart-Endpunkt des Befehls `yahoo` ist die einzige kostenlose Quelle
für Indexschlusskurse vom selben Tag, Tageshochs, Frontmonat-Futures und
Devisenkassakurse. Er ist inoffiziell: keine Doku, keine Garantien, und
bei gehäuften Anfragen kommt eine Weile HTTP 429. Ein Symbol pro Aufruf;
scheitert es zweimal, nimm die Zahl aus dem Bericht einer
Nachrichtenagentur oder der Börse und versuch es später wieder. Ein 429
ist kein Beleg. Symbole: ^GSPC, ^DJI, ^IXIC, ^N225, ^STOXX (Stoxx Europe
600), ^GDAXI, ^FTSE, ^FCHI, ^HSI, ^TNX (zehnjährige US-Rendite, in
Prozent), ^TYX (30 Jahre), BZ=F, CL=F, NG=F, GC=F, EURUSD=X, USDJPY=X,
GBPUSD=X. `--field high` für das Tageshoch, `--range 1y` für ein Jahr.
Für Renditen sind die amtlichen Quellen vom selben Tag vorzuziehen
(Treasury, Bundesbank); den Chart-Endpunkt nur für das Tageshoch nutzen.

## Grenzen

Keine Quelle braucht einen Schlüssel oder ein Konto. `fred` lädt
dieselbe CSV, die der „Download“-Button auf jeder Reihenseite liefert,
was für eine Handvoll Abrufe gut funktioniert. `eia` nutzt den
öffentlichen `DEMO_KEY` von api.data.gov, begrenzt auf 30 Aufrufe pro
Stunde und 50 pro Tag und IP-Adresse. Treasury-XML und Fiscal Data, Bank
of England, Bundesbank, EZB, Eurostat, OECD und Frankfurter sind offen.
Fiscal Data und OECD antworten mit HTTP 429, wenn man sie überlastet;
ein Faktencheck braucht eine Handvoll Aufrufe, weit unter jedem Limit.

## Reihen-IDs, die man kennen sollte

**FRED** (`fred SERIES`): DGS2, DGS5, DGS10, DGS30 (Treasury mit
konstanter Laufzeit); T10Y2Y (Zinskurve); DFEDTARU (Obergrenze der Fed
Funds); DCOILBRENTEU, DCOILWTICO (Öl spot); GASREGW, GASDESW (wöchentliche
Benzin-/Dieselpreise); DHHNGSP (Henry-Hub-Gas); DEXUSEU, DEXJPUS,
DEXUSUK (Devisen); CPIAUCSL, CPILFESL, PCEPI (US-Inflation); GDP
(nominal, quartalsweise annualisiert), GDPC1 (real); GFDEBTN
(Bundesschuld, quartalsweise); GFDEGDQ188S (Schuldenquote);
IRLTLT01GBM156N, IRLTLT01DEM156N, IRLTLT01JPM156N, IRLTLT01FRM156N,
IRLTLT01ITM156N (monatliche zehnjährige Renditen); SP500, NASDAQCOM,
DJIA, NIKKEI225 (täglich, am Folgetag); VIXCLS.

**Treasury** (`treasury [YYYYMM] --tenor X`): BC_1MONTH, BC_3MONTH,
BC_6MONTH, BC_1YEAR, BC_2YEAR, BC_5YEAR, BC_10YEAR, BC_20YEAR, BC_30YEAR.
Ein Monat pro Aufruf; für den Verlauf den Monat übergeben.

**Bank of England** (`boe SERIES --start JAHR`): IUDMNPY (nominale
zehnjährige Par-Rendite der Gilts), IUDSNPY (5 Jahre), IUDLNPY (20
Jahre), IUDBEDR (Bank Rate), XUDLUSS (USD je GBP), XUDLERS (EUR je GBP).
Die Hilfeseite der Datenbank dokumentiert die CSV-URL (Datefrom,
Dateto=now, SeriesCodes bis 300, CSVF=TN, UsingCodes=Y).

**EZB-Datenportal** (`ecb FLOW/KEY`): ICP/M.U2.N.000000.4.ANR (HVPI
gesamt), ICP/M.U2.N.XEF000.4.ANR (Kernrate), EXR/D.USD.EUR.SP00.A
(täglicher EUR/USD-Referenzkurs), FM/B.U2.EUR.4F.KR.DFR.LEV
(Einlagensatz). Dokumentierte Parameter: lastNObservations,
startPeriod, endPeriod, format=csvdata.

**Eurostat** (`eurostat DATASET k=v …`): prc_hicp_manr mit geo=EA
(Euroraum) oder einem Ländercode wie geo=DE und coicop=CP00;
gov_10dd_edpt1 für Staatsschulden (jährlich); namq_10_gdp für das
vierteljährliche BIP. Dokumentierter Parameter: lastTimePeriod.

**OECD** (`oecd LAND`): dreistellige Codes: USA, GBR, DEU, FRA, ITA, ESP,
JPN, CAN, AUS; monatliche durchschnittliche zehnjährige Rendite aus dem
Dataflow DSD_STES@DF_FINMARK.

**EIA** (`eia SERIES`): RBRTE (Brent spot), RWTC (WTI spot).
JSON-Antworten enden bei 5.000 Zeilen; `--n` setzt die Anzahl.

**Frankfurter** (`fx VON NACH [DATUM]`): v1-Endpunkte auf
api.frankfurter.dev (`/v1/latest`, `/v1/YYYY-MM-DD`); EZB-Referenzkurse,
an Arbeitstagen gegen 16 Uhr MEZ veröffentlicht; keine Kontingente.

## Fallen

- **Der Verzug ist unterschiedlich.** Der Chart-Endpunkt ist live;
  Treasury und Bundesbank veröffentlichen am selben Tag; FREDs
  H.15-Renditen und Indexstände am nächsten Geschäftstag; die Datenbank
  der BoE etwa drei Tage später; EIA-Spotpreise etwa eine Woche;
  monatliche Reihen von EZB und Eurostat enthalten nur endgültige Daten,
  die Schnellschätzung von heute Morgen ist also nicht drin. Prüf die
  Zeile `latest:`, die das Skript ausgibt, bevor du „am Dienstag“ in
  eine Begründung schreibst.
- **Par- oder Benchmark-Rendite.** Die BoE-Reihe und die Treasury-Kurve
  sind geglättete Par-Renditen; Nachrichtenagenturen und
  Finanzdatenanbieter nennen die Benchmark-Anleihe. Sie unterscheiden
  sich um einige Basispunkte, also sollte ein Urteil „höchster Stand
  seit“ auf einem klaren Abstand beruhen, nicht auf 2 Basispunkten. Sag,
  welches Maß du benutzt hast.
- **Prozent oder Verhältnis.** Die Schuldenquote braucht das nominale,
  annualisierte BIP desselben Zeitraums (FRED `GDP`, quartalsweise);
  durch das reale BIP oder eine Monatszahl zu teilen ergibt Unsinn. FRED
  `GFDEGDQ188S` ist die veröffentlichte Quote, wenn du nur eine
  bestätigen musst.
- **Dezimalkommas** in den CSVs der Bundesbank; das Skript wandelt sie
  um. Ebenso in deutschen Texten: 4,79 Prozent ist 4.79 für die Skripte.
- **User-Agents.** FRED lehnt browserartige User-Agents von Skripten ab;
  BoE und Treasury lehnen Anfragen ohne einen ab. Das Skript regelt das
  je Quelle; wenn du von Hand abrufst, lass den User-Agent bei FRED weg
  und setz ihn anderswo.
- **Ausgangswerte vor einem Ereignis.** Nimm den letzten Handelstag vor
  dem Ereignis und sag das: `--change 2026-02-27` gibt den Ausgangswert
  aus, damit die Begründung ihn zitieren kann.

## Was hier nicht abgedeckt ist

Das Datenportal des IWF und die meisten Kursseiten sind nicht
eingebunden: Sie antworten Skripten nicht. Indexanbieter
veröffentlichen Verlaufsdateien nur hinter einer Anmeldung oder einer
Browserprüfung; der Browser erreicht sie, wenn eine amtliche Zahl vom
selben Tag nötig ist. Kostenpflichtige Terminaldaten liegen außerhalb
des Rahmens; lässt sich eine Aussage nur damit klären (ein bestimmter
Kurs im Tagesverlauf, das Datum eines Benchmark-Wechsels), sag das in
der Bitte um Unterlagen, statt zu schätzen.
