# CHECK24-GenDev

Dieses Projekt ist Teil der CHECK24 GenDev Holiday Challenge.
Die App besteht aus einem SvelteKit Frontend, einem FastAPI Backend mit einer PostgreSQL Datenbank, sowie einem Redis Cache.

## About

### Datenbank

PostgreSQL Datenbank mit 2 genutzten Tabellen: `hotels` und `offers_1`.
Die Daten wurden mit dem gleichen Schema, wie des der CSV Datei in die Datenanbank geladen.
Ursprünglich wollte ich das Schema anpassen, es hat sich allerdings als komplizerter herausgestellt, als gedacht.

So hat im Moment die Datenbank fast gleiche Schema, wie das csv.
Um eine schnelle suche zu Ermöglichen habe eine Indexierung verwendet mittels B-Tree verwendet. Der konkrete Index lautet:
`"idx_offers_optimized_new_2" btree (outbounddepartureairport, countadults, countchildren, outbounddeparturedatetime, inboundarrivaldatetime, hotelid DESC)`

Des weiteren sieht die aktuelle Offers Table Folgendermaßen aus:

```
                                 Table "public.offers_1"
          Column           |            Type             | Collation | Nullable | Default
---------------------------+-----------------------------+-----------+----------+---------
 hotelid                   | integer                     |           |          |
 outbounddeparturedatetime | timestamp without time zone |           |          |
 inbounddeparturedatetime  | text                        |           |          |
 countadults               | integer                     |           |          |
 countchildren             | integer                     |           |          |
 price                     | integer                     |           |          |
 inbounddepartureairport   | text                        |           |          |
 outboundarrivalairport    | text                        |           |          |
 inboundarrivaldatetime    | timestamp without time zone |           |          |
 outbounddepartureairport  | text                        |           |          |
 inboundarrivalairport     | text                        |           |          |
 outboundarrivaldatetime   | text                        |           |          |
 mealtype                  | text                        |           |          |
 oceanview                 | boolean                     |           |          |
 roomtype                  | text                        |           |          |
Indexes:
    "idx_offers_optimized_new_2" btree (outbounddepartureairport, countadults, countchildren, outbounddeparturedatetime, inboundarrivaldatetime, hotelid DESC)
```

Als weitere optimierung habe ich `outbounddeparturedatetime` und `inbounddeparturedatetime` in einen timestamp umgewandelt um die Daten besser zu vergleichen zu können.

Im moment query die Daten sehr schnell (100ms - 800ms ist die Zeit der reinen SQL Abfrage), jedoch werden deshalb weniger Informationen auf der Startseite angzeigt.

### Backend

Das Backend ist in Python mit FastAPI geschrieben. Es kann sich unter URL `http://localhost:xxxx/docs` die doku der Endpointe angeschaut werden.

#### Cache

FastAPI nutzt einen Redis Cache um OpenAI Abfragen und Datenbank Abfragen zwischenzuspeichern. Dieser ist zu Demozwecken auf 1 Minute eingestellt. Mir ist auchgefallen, dass die Datenabank schon sehr gut selber cached, aber bei der OpenAI API ist es sehr hilfreich. Das wäre auch für ein Real-World Szenario sehr hilfreich, um bei der OpenAI API Kosten zu optimieren.

### Frontend

Das Frontend benutzt das Framework SvelteKit. SvelteKit basiert auf Svelte, bietet aber Server Side Rendering und Funktionen wie Routing out of the Box. Für das Styling benutze ich überwiegend TailwindCSS und die Componenten von Flowbite.
Beim Frontend war mir wichtig, dass die UI realtiv schön ist aber vor Allem, dass das Nutzerinterface klar verständlich ist.

### weitere Funktionen

#### OpenAI

- Ich bin am Anfang davon ausgegangen, dass es mehere Reisezeile gibt, deshalb habe ich mir eine Funtion überlegt, wie der Nutzer leichter nach Zielen suchen kann. In dem Suchfeld, kann er nicht nur Reiseziele wie Mallorca oder Paris suchen sondern auch nach Eigenschaften wie Strand etc. Beispielsweise kann nach "Ich möchte an den Strand" gesucht werden. Um die anderen Reiseziele zu Testen kann man Beispielsweise: "Großstadturlaub am Meer", "Ich möchte in eine historische Stadt" suchen.
  Aber finde die Funktion trozdem eine gute Idee, deshalb habe ich diese drin gelassen.

- Ich habe noch eine weitere Funktion mit OpenAI implementiert, diese generiert auf Basis des Reiseziels, Datums und der Anzahl der Personen einen Reiseempfehlung. Diesee wird zwischen den Offers angezeigt.
- Für die genaue Funktionsweise und die predefined Promts siehe controller.py

- _Note: Die OpenAI API ist relativ langsam, daher dauern diese Funktionen immer etwas._

#### Filter

- Bei allen Angeboten eines Hotels kann nach Preis, sowie Datum gefiltert werden.

### Optimierungen

Optimierungen der Geschwindigkeit:

- Datenbankindexierung
- Datanbankabfragen werden mithilfe von Redis gecached
- OpenAI Abfragen werden mithilfe von Redis gecached

weitere ptimierungen

- Docker

### Hinweise

- es wird aktuell nur ein Airport pro Suche unterstützt

### aktuelle Probleme:

- Die Datenbank enthält viele Duplikate, ich versuche das im Moment zu lösen, indem ich die Datenbank neu aufsetzte oder die Duplikate manuell entferne. Dadurch dauern die querys eventuell länger.
- Server hat kein HTTPS, deshalb kann das bereits deployte Frontend nicht auf das Backend zugreifen.

### Verbesserungen, welche ich mir überlegt habe

- Datenbank Schema anpassen
- weitere Filter-Möglichkeiten
