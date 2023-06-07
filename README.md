# CHECK24-GenDev

Dieses Projekt ist Teil der CHECK24 GenDev Holiday Challenge.
Die App besteht aus einem SvelteKit Frontend, einem FastAPI Backend mit einer PostgreSQL Datenbank, sowie einem Redis Cache.

## About


### Datenbank
PostgreSQL Datenbank mit 2 genutzten Tabellen: ```hotels``` und ```offers_1```.
Die Daten wurden mit dem gleichen Schema, wie des der CSV Datei in die Datenanbank geladen.
Ursprünglich wollte ich das Schema anpassen, es hat sich allerdings als komplizerter herausgestellt, als gedacht.

Das Schema was ich mir überlegt hatte, war folgendes:
```

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stars = Column(Integer)
    rooms = relationship("Room", back_populates="hotel")


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    departure_airport = Column(String)
    arrival_airport = Column(String)
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
    offers = relationship("Booking", back_populates="flight")


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    flight_id = Column(Integer, ForeignKey('flights.id'))
    count_adults = Column(Integer)
    count_children = Column(Integer)
    price = Column(Float)
    meal_type = Column(Enum("BREAKFAST", "ALLINCLUSIVE", "HALFBOARD", "NONE", name="meal_type_enum"), nullable=False)
    hotel = relationship("Hotel", back_populates="offers")
    flight = relationship("Flight", back_populates="offers")


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    type = Column(Enum("APARTMENT", "DOUBLE", "STUDIO", "FAMILY", "SUITE", "SINGLE", "ACCORDINGDESCRIPTION", name="room_type_enum"))
    ocean_view = Column(Boolean)
    offers = relationship("Booking", back_populates="room")
```
Da ich davon ausgegangen bin, dass sich z.B. die Flüge doppeln werden. 
Es hat sich aber als komplizert erachtet das ```offers.csv```in dieses Schema zu übertragen.

So hat im Moment die Datenbank fast gleiche Schema, wie das csv.
Um eine schnelle suche zu Ermöglichen habe eine Indexierung verwendet mittels B-Tree verwendet. Der konkrete Index lautet:
```"idx_offers_optimized_new_2" btree (outbounddepartureairport, countadults, countchildren, outbounddeparturedatetime, inboundarrivaldatetime, hotelid DESC)```

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
Als weitere optimierung habe ich ```outbounddeparturedatetime``` und ```inbounddeparturedatetime``` in einen timestamp umgewandelt um die Daten besser zu vergleichen zu können.


Im moment query die Daten sehr schnell (100ms - 800ms ist die Zeit der reinen SQL Abfrage), jedoch werden deshalb weniger Informationen auf der Startseite angzeigt.

### Backend
Das Backend ist in Python mit FastAPI geschrieben. Es kann sich unter URL ```http://localhost:xxxx/docs``` die doku der Endpointe angeschaut werden.

#### Cache
FastAPI nutzt einen Redis Cache um OpenAI Abfragen und Datenbank Abfragen zwischenzuspeichern. Dieser ist zu Demozwecken auf 1 Minute eingestellt. Mir ist auchgefallen, dass die Datenabank schon sehr gut selber cached, aber bei der OpenAI API ist es sehr hilfreich. Das wäre auch für ein Real-World Szenario sehr hilfreich, um bei der OpenAI API Kosten zu optimieren.

### Frontend
Das Frontend ist in SvelteKit geschrieben. Für das Styling benutze ich überwiegend TailwindCSS und die Componenten von Flowbite. 
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


## How to run locally

### Frontend

um das Frontend zu starten folgenden anweisungen folgen:
https://github.com/timkn/CHECK24-GenDev/tree/main/frontend#developing.
eventell muss https://kit.svelte.dev installiert werden.
Um zu valiederen, dass wie gewünscht funktioniert kann sich auch das Frontend auf: https://gendev.timknothe.com angesehen werden. Dort ist immer das aktuelle Frontend deployed, dieses hat aber keinen Zugriff auf das Backend, das Backend (noch) nicht über HTTPS verfügt.

Konkret müssen folgende Schritte durchgeführt werden:

1. In den Ordner frontend navigieren.
2. ```npm install``` ausführen
3. ````npm run dev```` ausführen
nun sollte das Frontend gestartet sein.

### Backend

Das Backend kann mithilfe von Docker Compose gestartet werden. 
Hierbei ist zu beachten, dass eine Postgres Datenbank mitaufgestzt wird. 
In der jetzigen konfiguration wird diese Datenbank nicht verwendet, sondern eine, welche auf einem Server läuft und die Date enthält.

Alle credentials für die Datenbank, sowie OpenAI werden _im Moment_ in dem  ```docker-compose.yml``` File mitgeliefert. Bitte beachten: Damit die Daten & Konfiguration bereits in der Datenabnk sind wird nicht die lokal von Docker erstellte PostgreSQL Datenbank verwendet sondern diese, welche auf einem Oracle Cloud Server läuft. Auf dem Oracle Cloud Server selber wird in leicht abgeänderter From genau dieses ```docker-compose.yml``` file ausgeführt. Die Credentials für die Datenbank können entweder im ``docker-compose.yml`` file nachgeschaut werden (Es sind jetzt die gleichen wie für die lokale DB) oder sind folgende:

username: `````postgres`````

password: `````hfieufh8f39f9fb3uzfg839fh3f3`````

datenbank-name: ```gendev```

host: `````144.24.175.18`````

port: `````5432`````

```postgresql://postgres:hfieufh8f39f9fb3uzfg839fh3f3@144.24.175.18:5432/gendev```

_CORS ist im Moment so eingestellt, dass alle IPs erlaubt sind. Dies ist für die Entwicklung sehr hilfreich, sollte aber in einem Real-World Szenario angepasst werden._

Es sollte deshalb eigentlich keine CORS Probleme geben, ansonsten kontakieren Sie mich gerne.


Konkret müssen folgende Schritte durchgeführt werden:

(Docker muss installiert sein)

1. In den Ordner backend navigieren.
2. ```docker compose build``` ausführen
3. ````docker compose up```` ausführen
nun sollte das Backend gestartet sein.



Bitte kontakieren Sie mich gerne bei Fragen / Problemen 
```timknothe21@gmail.com```