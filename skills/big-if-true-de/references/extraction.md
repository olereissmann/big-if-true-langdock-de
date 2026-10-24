# Big If True: Durchgang 1, jede Aussage finden

Dies sind die vollständigen Extraktionsregeln der Faktencheck-Methode
Big If True. Deine einzige Aufgabe ist die Aussagendatei, die diese
Regeln beschreiben: Sie zu schreiben ist die ganze Aufgabe, nichts
anderes gehört dazu. Der geprüfte Text liegt in `source.txt`.

Ziel ist die vollständige Liste aller atomaren, von außen prüfbaren
Tatsachenaussagen, in der Reihenfolge des Textes. **Vollständigkeit hat
oberste Priorität: Eine übersehene Tatsache ist ein Fehler, eine kleine
Aussage zu viel ist keiner.**

**Schreib die Extraktion auf, bevor du irgendetwas prüfst.** Lege eine
Aussagendatei an (`claims.md`, oder eine gleichwertige schriftliche
Liste, wenn es kein Code-Werkzeug gibt) und arbeite den Text Absatz für
Absatz durch. Schreib die Aussagen jedes Absatzes auf, jeweils mit ihrem
exakten Zitat verankert, bevor du zum nächsten gehst. Jede Aussage steht
in einer Zeile, ihr Zitat in der Zeile darunter, wörtlich aus dem Text
kopiert:

```
wire: dpa

## P3
- [fact] Die Initiatoren gaben am Sonntag bekannt, genug Unterschriften zu haben.
  > gaben am Sonntag bekannt, dass sie genug Unterschriften haben
- [attribution] Dan Schnur sagte, die Ausgaben würden sich verdreifachen.
  > „verdreifachen“, sagte Dan Schnur
discard: „Holt die Mistgabeln raus“, rhetorisch
```

Die Markierungen `[fact]` und `[attribution]` bleiben englisch, denn die
Datei wird von Code gelesen. Eine Aussage ohne Zitatzeile oder ein
Zitat, das nicht Wort für Wort im Text steht, wird abgelehnt. Ergibt ein
Absatz nichts, schreib „keine prüfbaren Aussagen“ unter seine
Überschrift. Das ist keine Buchhaltung: Eine Extraktion, die nur im Kopf
stattfindet, wird stillschweigend verdichtet, weil jede Aussage sich
wie eine künftige Recherche anfühlt, die man bezahlen muss. Erst die
Liste zu schreiben, ohne dabei zu prüfen, hält die Durchsicht ehrlich.
Extraktion ist billig, und in Durchgang 2 bedient eine gute Suche meist
eine ganze Gruppe von Aussagen. Eine viel längere Liste kostet also nur
etwas mehr Recherche. Lass beim Extrahieren nie eine Aussage weg, weil
sie nebensächlich, offensichtlich oder teuer zu prüfen wirkt.

**Beginne die Datei mit der Agenturzeile.** Die erste Zeile von
claims.md sagt, ob der Text ganz oder teilweise Agenturmaterial ist:
`wire: dpa` (oder `wire: dpa, Reuters`, die Agenturen, die er nennt)
oder `wire: none`. Achte auf eine Ortsmarke wie „Berlin (dpa) -“, ein
Kürzel wie „lb/dpa“, „mit Material von“, „Quelle: dpa“ oder einen Satz,
der eine Agentur als Quelle der Meldung nennt. Halte fest, was der Text
zeigt; rate nicht. Diese Zeile entscheidet später, welche Quellen als
unabhängig zählen können.

**Führe ein Ausschussprotokoll.** Wenn du einen Satz als nicht
extrahierbar übergehst, notiere ihn in der Aussagendatei mit einem
Stichwort als Grund: *Meinung*, *Prognose ohne Tatsachengehalt*,
*rhetorisch*, *hypothetisch*. Ein stilles Überspringen ist unsichtbar,
ein protokolliertes lässt sich prüfen. Die meisten Extraktionsfehler
sind keine falsch beurteilten Sätze, sondern Sätze, die nie bewusst
beurteilt wurden.

- **Atomar, weil Bündel Fehler verstecken.** Teile zusammengesetzte
  Aussagen so, dass jede genau eine prüfbare Tatsache trägt, mit ihren
  wesentlichen Einschränkungen und Bedingungen. Ein Satz mit drei Zahlen
  sind drei Aussagen; Funktion und Name, Datum und Ort, Aussage und
  Größenordnung werden genauso geteilt. Der Grund ist das Urteil, nicht
  Ordnung: Ein Bündel bekommt ein Urteil, also reist eine falsche Zahl
  mit zwei richtigen mit, und das Ganze geht als „ungefähr richtig“
  durch. Geteilt wird der falsche Teil isoliert und benannt, während die
  anderen bestätigt werden.
- **Für sich verständlich.** Löse Pronomen mit dem nötigsten Namen auf,
  damit jede Aussage allein steht. Namen, Zahlen, Einheiten und Zitate
  bleiben exakt.
- **Zuschreibung oder Substanz.** Lege für jedes Zitat und jede
  zugeschriebene Äußerung (sagte, kündigte an, bestritt, glaubte,
  fürchtete, erwartete, warf vor) eine Zuschreibungsaussage an: Die
  Aussage ist, dass X es gesagt hat. Mach den Gegenstand eines Glaubens,
  einer Befürchtung, Erwartung, Anschuldigung, Warnung, Hoffnung, eines
  Plans oder Versprechens nicht zur Tatsachenaussage, außer der Text
  behauptet ihn unabhängig davon als Tatsache. Markiere jede Aussage
  beim Extrahieren mit [attribution] oder [fact].
- **Genre-Prüfung: Wessen Stimme trägt den Text?** Die
  Zuschreibungsregel gilt für berichtende Texte, in denen die Stimme des
  Artikels weitergibt, was Dritte sagen. In einem Interview, Kommentar,
  einer Kolumne oder einem Ich-Essay SIND die Tatsachenbehauptungen der
  sprechenden Person die Substanz des Textes: Die Leser nehmen sie als
  Aussagen über die Welt, und sie werden als [fact] behandelt. In diesen
  Genres gilt die Zuschreibungsregel eine Ebene tiefer: für das, was die
  sprechende Person anderen zuschreibt (einer Studie, einem Papier,
  einer genannten Person). Ein Interview, das nach der Regel für
  Berichte behandelt wird, schrumpft auf fast nichts Prüfbares
  zusammen. Das ist die größte einzelne Quelle übersehener Aussagen.
- **Extrahiere diese, hier stecken die Fehler.** Klassen, die sich
  überspringbar anfühlen, aber regelmäßig Befunde liefern:
  - *Quantifizierte Verallgemeinerungen*: „fast jeder“, „alle“,
    „niemand“, „immer“. An Daten prüfbar und oft die schwächsten
    Aussagen des Textes.
  - *Absolute Aussagen, die das Argument tragen*: „jeder Artikel, der
    je geschrieben wurde, ist darin“. Ein wörtlich falsches Absolut ist
    gerade deshalb wichtig, weil sich das Argument auf seine Größe
    stützt.
  - *Definitionen*: „X heißt Y“, „X bedeutet Z“. Eine falsche Definition
    führt so wirksam in die Irre wie eine falsche Zahl.
  - *Vorsichtige Spekulation*: „man vermutet, dass …“, „könnte …“.
    Extrahiere sie mit der Einschränkung im Aussagetext; das Urteil kann
    gut could_not_verify sein, und eine unprüfbare Verbindung, die als
    wahrscheinliche Erklärung präsentiert wird, ist selbst
    erwähnenswert.
  - *Aussagen in Fragen*: Die Prämissen eines Interviewers (die
    Handlung eines Films, der Aufbau einer Studie, „es kam das Gerücht
    auf, dass …“) werden auch gegenüber den Lesern behauptet.
  - *Hintergrund und Allgemeinwissen*: billig zu prüfen, und dass sie in
    der Liste stehen, beweist, dass die Durchsicht vollständig war.
- **Identitätsangaben im Vorbeigehen.** „Unternehmenssprecherin Maria
  Chen“ behauptet, dass Maria Chen Sprecherin des Unternehmens ist.
  Extrahiere es.
- **Die Formulierung des Auftrags engt Durchgang 1 nie ein.** Eine Bitte,
  „die Prognosen zu prüfen“ oder „zu sehen, ob es hält“, bestimmt, welche
  Befunde du in Durchgang 3 hervorhebst, nicht den Umfang der
  Extraktion. Die Extraktion hängt nicht von der Fragestellung ab:
  Derselbe Text ergibt immer dieselbe Liste.
- **Der Apparat des Artikels ist keine Aussage.** Autorenzeile,
  Autorentitel, Ortsmarke, Zeitstempel, Name des Mediums,
  Rubrikenzeilen, Bildnachweise, „aktualisiert“-Hinweise: Sie
  beschreiben den Artikel, nicht die Welt. Übernimm Autorenzeile und
  Datum als Metadaten des Berichts; extrahiere oder prüfe sie nie.
- **Reihenfolge des Textes, keine Dubletten, kein Wissen von außen, noch
  keine Prüfung.**

Ein Satz, zwei Aussagen:

> „Das Werk wurde 1998 eröffnet und beschäftigt 1.200 Menschen.“
> → [fact] Das Werk wurde 1998 eröffnet.
> → [fact] Das Werk beschäftigt 1.200 Menschen.

Ein Zitat und die Funktion, nebenbei erwähnt:

> „‚Wir haben dieses Produkt nie an Tieren getestet‘, sagte
> Orion-Labs-Sprecherin Dana Reyes.“
> → [attribution] Orion-Labs-Sprecherin Dana Reyes sagte, das
>   Unternehmen habe das Produkt nie an Tieren getestet.
> → [fact] Dana Reyes ist Sprecherin von Orion Labs.

Drei Zahlen, drei Aussagen, und warum das zählt:

> „Gruppe A erreichte 74 Prozent, Gruppe B 76 Prozent und das Modell 95
> Prozent.“
> → drei getrennte Aussagen. Hat die Studie tatsächlich 74 / 76 / 90
> berichtet, isoliert die Teilung ein klares needs_review bei der 95,
> während die anderen belegt sind. Gebündelt lautet das Urteil
> wahrscheinlich nur „die Zahlen stimmen ungefähr“, und der eine echte
> Fehler taucht nie auf.

Das Zitat ist die exakte Stelle des Textes, die die Aussage trifft:
eine Wendung, wenn die Aussage Teil eines Satzes ist, der ganze Satz,
wenn sie sein Kern ist. Es verankert die Aussage im Bericht und muss
genau einmal im Text vorkommen; verlängere es, bis das zutrifft.

**Prüfe über die Dichte, nicht durch erneutes Lesen.** Wer gerade
aussortiert hat, bestätigt beim Wiederlesen meist das Aussortieren.
Prüfe stattdessen die Zahlen: Gründliche Extraktion behauptender
Nachrichten- und Interviewprosa ergibt etwa eine Aussage pro 12 bis 15
Wörter. Ein Nachrichtentext mit 1.000 Wörtern ist ein Text mit 80
Aussagen, nicht mit 40. Ist die Dichte schlechter als eine Aussage pro
15 Wörter, geh die Absätze mit den wenigsten Aussagen noch einmal durch,
das Ausschussprotokoll in der Hand, und frag bei jedem übersprungenen
Satz: Steckt hier ein Mengenwort, eine Definition, eine Prämisse oder
ein Absolut? (Der Build setzt das durch: Über 20 Wörtern pro Aussage
verweigert er den Bericht, bis Durchgang 1 wieder geöffnet ist, oder,
bei einem wirklich dünnen Text, bis check.json im Feld `thin_text`
begründet, warum. Er markiert außerdem längere Absätze ohne verankerte
Aussage.)
