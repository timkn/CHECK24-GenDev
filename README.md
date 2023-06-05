# CHECK24-GenDev

Dieses Projekt ist Teil der CHECK24 GenDev Holiday Challenge.
Die App besteht aus einem SvelteKit Frontend, einem FastAPI Backend mit einer PostgreSQL Datenbank, sowie einem Redis Cache.

## About


### Datenbank
PostgreSQL Datenbank mit 2 Tabellen: ```hotels``` und ```offers```.
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
Um eine schnelle suche zu ermöglichen habe eine Indexierung verwendet.


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

### Backend

Das Backend kann mithilfe von Docker Compose gestartet werden. 
Hierbei ist zu beachten, dass eine Postgres Datenbank mitaufgestzt wird. 
In der jetzigen konfiguration wird diese Datenbank nicht verwendet, sondern eine, welche auf einem Server läuft und die Date enthält.

Alle credentials werden _im Moment_ in dem  ```docker-compose.yml``` File mitgeliefert.

_CORS ist im Moment so eingestellt, dass alle IPs erlaubt sind. Dies ist für die Entwicklung sehr hilfreich, sollte aber in einem Real-World Szenario angepasst werden._

Es sollte deshalb eigentlich keine CORS Probleme geben, ansonsten kontakieren Sie mich gerne.

Bitte kontakieren Sie mich gerne bei Fragen / Problemen 
```timknothe21@gmail.com```