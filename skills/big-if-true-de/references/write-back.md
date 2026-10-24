# Befunde als Kommentare im Ausgangsdokument hinterlassen

Kam der geprüfte Text aus einem Google Doc oder einer Notion-Seite,
können die needs_review-Befunde als Kommentare dorthin zurück, jeder an
seiner Stelle, so wie eine Redakteurin kommentiert. Zwei Wege:

- **Google Doc + ein Browser.** Tastenkürzel im Docs-Editor. Zuerst
  Claude in Chrome: Es ist das eigene Chrome der Nutzerin, bei Google
  angemeldet, also öffnet sich das Dokument mit ihren Rechten und ihrem
  Namen an den Kommentaren. Der eingebaute Browser ist die Ausweichlösung;
  er hat keine Anmeldungen, also bitte die Nutzerin, sich dort zuerst
  anzumelden, und melde dich nie für sie an.
- **Notion-Seite + der Notion-Connector.** Ein Tool-Aufruf pro Kommentar,
  verankert über einen Anfang…Ende-Ausschnitt der Stelle. Kein Browser.

Das „Ja“ oder „mach“ der Nutzerin auf das Angebot ist die Freigabe;
Kommentare lassen sich zurücknehmen, also gibt es keine zweite
Bestätigung und keine Vorschau.

Ist keiner der Wege verfügbar oder das Dokument schreibgeschützt, sag es
in einer Zeile und hör auf. Versuch nie, dich anzumelden, Zugriff
anzufordern oder den Modus des Dokuments zu ändern.

## Die Kommentare vorbereiten

    python3 scripts/assemble.py export comments source.txt check.json comments.json

Jeder Eintrag enthält den Kommentar in zwei Formen: `text`, schlicht,
mit Bezeichnung und URL jeder Quelle in eigenen Zeilen (Google Docs
macht nackte URLs zu Links), und `markdown`, mit Inline-Links (Notion).
Außerdem `find`, ein kurzes wörtliches Stück der Stelle, mit geraden
statt typografischen Anführungszeichen, so lange verlängert, bis es im
geprüften Text genau einmal vorkommt, und `selection`, die ersten zehn
und letzten zehn Zeichen der Stelle, verbunden durch drei Punkte, die
Form, an der Notion verankert. Nimm diese, nie das ganze Zitat:
Zeichensetzung und Zeilenumbrüche im Dokument können vom geprüften Text
abweichen.

## Google Docs: der Ablauf, pro Kommentar

Öffne das Dokument einmal in Claude in Chrome (`navigate`), warte, bis
es geladen ist, drück Escape, um ein Link-Vorschaufenster zu schließen,
und klick einmal in den Fließtext, damit der Editor den Fokus hat. Dann
für jeden Eintrag, in einem `browser_batch`:

| Schritt | Mac | Windows / Linux | Was passiert |
|---|---|---|---|
| 1 | `cmd+f` | `ctrl+f` | öffnet die Suche von Docs |
| 2 | `find` eintippen | | der Treffer wird markiert; die Suche zeigt „1 von 1“ (englische Oberfläche: „1 of 1“) |
| 3 | `Escape` | | schließt die Suche, der Treffer bleibt **ausgewählt** |
| 4 | `cmd+alt+m` | `ctrl+alt+m` | öffnet einen Kommentar zur Auswahl |
| 5 | `text` eintippen | | Zeilenumbrüche sind in Ordnung; Enter postet nicht |
| 6 | `cmd+Return` | `ctrl+Enter` | postet den Kommentar |
| 7 | 2 s warten, `find` „Abbrechen“ (oder „Cancel“) | | ein solcher Button heißt: Der Kommentar ist noch ein ungespeicherter Entwurf |
| 8 | Screenshot | | zeigt, welche Stelle markiert war |

Nach den Schritten 1, 3, 4 und 5 je eine Sekunde warten; der Editor
braucht das.

**Ein Kommentar zählt erst, wenn er gespeichert ist.** Solange er ein
Entwurf ist, hat sein Feld noch ein Textfeld mit den Buttons
„Kommentieren“ und „Abbrechen“ (englisch: Comment, Cancel). Gespeichert
schließt sich das Feld, und der Kommentar zeigt den Namen der Autorin
und eine Uhrzeit. Findet Schritt 7 einen Abbrechen-Button, hat das
Kürzel nicht gepostet: Klick den Kommentieren-Button daneben, über
seine Referenz aus `find`, warte zwei Sekunden und prüf noch einmal.
Öffne den nächsten Kommentar nicht, solange ein Entwurf offen ist.
Entwurf und gespeicherter Kommentar sehen im Screenshot fast gleich
aus; der Screenshot bestätigt also nur, dass die richtige Stelle
markiert war, nie, dass der Kommentar gespeichert wurde.

Zeigte die Suche „0“ oder „1 von 2+“, drück Escape, öffne keinen
Kommentar und versuch es mit einem längeren Stück aus `quote`. Gibt es
die Stelle nicht mehr (das Dokument wurde seit dem Check bearbeitet),
überspring sie und sag es am Ende.

Nur Kommentare: Tippe nie in den Dokumenttext, nimm keine Vorschläge an,
löse und lösche nichts. Ein Kommentar pro Befund. Lass den Tab am Ende
auf dem Dokument offen.

## Notion: ein Aufruf pro Kommentar

Ruf für jeden Eintrag die Kommentarfunktion des Connectors auf, mit der
Seiten-ID, `selection_with_ellipsis` gleich der `selection` des Eintrags
und als Markdown das `quote` des Eintrags in Anführungszeichen in einer
eigenen ersten Zeile, danach das `markdown` des Eintrags. Die Zitatzeile
ist wichtig: Notion verankert einen Kommentar an dem Block, der die
Auswahl enthält, nicht an der Wendung. Zwei Befunde in einem Absatz
werden also zwei Kommentare am selben Block, und erst die zitierten
Worte zeigen, welcher welcher ist. Meldet der Aufruf, die Auswahl sei
mehrdeutig oder nicht gefunden, erweitere den Ausschnitt aus `quote` und
versuch es einmal erneut; scheitert es wieder, überspring den Befund und
sag es am Ende. Bearbeite nie die Blöcke der Seite.

## Prüfen und berichten

Prüfe im Dokument, nie anhand von Screenshots: Die Zahl, die du
meldest, ist die Zahl, die du zurückgelesen hast.

Google Docs: Ist der Drive-Connector verfügbar, lies das Dokument
einschließlich Kommentaren und bestätige, dass jeder Kommentar als
offener Thread an seiner Stelle steht. Sonst lade das Dokument neu,
damit du liest, was Google gespeichert hat, öffne den Kommentarverlauf
(`cmd+alt+shift+a` oder `ctrl+alt+shift+a`) und lies das Feld als
Seitentext. Ordne jeden geposteten Eintrag über seine ersten Worte einem
gespeicherten Kommentar zu. Poste fehlende nach und lies noch einmal.

Notion: Ruf die Seite einschließlich Diskussionen ab und bestätige, dass
jeder Kommentar an seinem Block sitzt.

Dann im Chat eine Zeile: wie viele Kommentare aus diesem Check das
Dokument jetzt enthält und welche Befunde übersprungen wurden und warum.
Keine Zusammenfassung der Befunde; die stehen im Dokument und im
Bericht.
