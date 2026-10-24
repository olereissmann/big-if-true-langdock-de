# Route: Webseiten, Social-Media-Posts, Bilder und Archive

Aussagen darüber, was eine Seite, ein Post, ein Bild oder ein Video
gezeigt hat, und ob es das noch zeigt oder je gezeigt hat. Hier verdient
sich der Browser seinen Platz: Der Beleg ist eine bestimmte gerenderte
Seite, oft hinter einer Anmeldung oder einer Skriptwand, und der Abruf
sieht sie nicht.

## War diese Seite so?

- `python3 scripts/evidence.py wayback URL --at JJJJMMTT` liefert den
  nächstgelegenen Schnappschuss im Internet Archive. Vergleich ihn mit
  der Live-Seite bei Aussagen wie „das Unternehmen hat stillschweigend
  geändert …“ oder „der Post wurde inzwischen gelöscht“. archive.today
  (archive.ph) ist das andere große Archiv; durchsuch es im Browser.
- `evidence.py wayback-save URL` sichert die Live-Seite jetzt, damit die
  geprüfte Fassung zitierbar bleibt, wenn sie sich ändert.

## Gab es diesen Post, und was stand darin?

- X/Twitter: Öffne die URL des Posts im Browser; ein gelöschter Post
  zeigt eine Fehlerseite, die selbst ein Beleg ist. Such den genauen
  Wortlaut in der Wayback Machine und auf archive.ph: Virale Posts sind
  meist archiviert.
- Bluesky, Threads, Mastodon: öffentlich, der Abruf klappt meist; sonst
  der Browser.
- Facebook, Instagram, TikTok, LinkedIn: der Browser, und meist die
  eigene Anmeldung der Nutzerin. Vermerke, dass es ihre Ansicht ist.
- Öffentliche Telegram-Kanäle: t.me/s/KANAL wird ohne Anmeldung
  angezeigt.
- Truth Social: trumpstruth.org für Trump; andere Konten über den Browser.
- Screenshots von Posts, die als Beleg kursieren, beweisen allein
  nichts; finde den Post oder sein Archiv.

## Bilder und Video

- Die umgekehrte Bildersuche läuft nur im Browser: Google Lens
  (lens.google.com), TinEye (tineye.com), Bing Visual Search, Yandex.
  Nimm zwei. Ziel ist das früheste Auftauchen und der ursprüngliche
  Zusammenhang.
- Prüfe die Datei selbst, wenn sie vorliegt: EXIF (`exiftool`, falls
  installiert), sichtbare Daten, Wetter, Schatten, Schilder,
  Nummernschilder im Abgleich mit dem behaupteten Ort und der Zeit.
- Für Video: die Browsererweiterung InVID/WeVerify, falls die Nutzerin
  sie hat; sonst Screenshots von Schlüsselbildern in die umgekehrte
  Bildersuche.

## Hat das schon jemand geprüft?

- Durchsuch den Fact Check Explorer von Google,
  toolbox.google.com/factcheck/explorer, im Browser. Er sammelt
  ClaimReview-Einträge von IFCN-Unterzeichnern und anderen
  Faktencheckern weltweit, in vielen Sprachen; für den deutschsprachigen
  Raum finden sich dort unter anderem dpa-Faktencheck, CORRECTIV.Faktencheck,
  AFP Faktencheck und BR24 #Faktenfuchs.
- Ein früherer Faktencheck ist eine starke Spur und eine Quelle; lies
  seine Belege und zitiere den Primärbeleg, den er gefunden hat, nicht
  nur den Faktencheck.

## Fallen

- Wayback-Zeitstempel sind UTC; rechne um, bevor du „vor“ oder „nach“
  sagst.
- Eine archivierte Seite kann eine Cache- oder abgemeldete Ansicht sein;
  die Live-Seite, die die Autorin sah, kann anders gewesen sein.
- Die Cache-Kopien der Suchmaschinen gibt es nicht mehr; die Archive
  sind der Beleg.
