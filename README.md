# CHECK24-GenDev

Dieses Projekt ist Teil der CHECK24 GenDev Holiday Challenge.
Die App besteht aus einem SvelteKit Frontend, einem FastAPI Backend mit einer PostgreSQL Datenbank.

## About


### Datenbank
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
Da ich davon zum Beispiel ausgegangen bin, dass sich die Flüge doppeln werden. 
Es hat sich aber als komolizert erachtet das ```offers.csv```in dieses Schema zu übertragen.

So hat im Moment die Datenbank Tabelle fast gleiche Schema, wie das csv.
Um eine schnelle suche zu ermöglichen habe einen Indexierung verwendet.


### Backend
Das Backend ist in Python mit FastAPI geschrieben. Es kann sich unter URL ```http://localhost:xxxx/docs``` die Endpointe angeschaut werden.
FastAPI ist realtiv einfach zu benutzen. 

### Frontend
Das Frontend ist in SvelteKit geschrieben. Für das Styling benutze ich überwiegend TailwindCSS und die Componenten von Flowbite.

### Funktionen
- #### OpenAI
    ich bin am Anfang davon ausgegangen, dass es mehere Reisezeile gibt, deshalb habe ich mir eine Funtion überlegt, wie der Nutzer leichter nach Zielen suchen kann. In dem Suchfeld, kann er nicht nur Reiseziele wie Mallorca oder Paris suchen sondern auch nach Eigenschaften wie Strand etc. Beispielsweise kann nach "Ich möchte an den Strand" gesucht werden. 
    Aber ich es trozdem eine gute Idee, deshalb habe ich sie drin gelassen.


### Honweise
- es wird nur ein Aiport pro Suche unterstützt

### aktuelle Probleme:
- Die Datenbank enthält viele Duplikate, ich versuche das im Moment zu lösen, indem ich die Datenbank neu aufsetzte oder die Duplikate manuell entferne. Dadurch dauern querys länger.
- Server hat kein HTTPS, deshalb kann das deployte Frontend nicht auf das Backend zugreifen.

### Verbesserungen, welche ich mir überlegt habe
- Datenbank Schema anpassen
- Redis Cache bei FastAPI implementieren


## How to run locally

### Frontend

um das Frontend zu starten folgenden anweisungen folgen:
https://github.com/timkn/CHECK24-GenDev/tree/main/frontend#developing.

Um zu valiederen, dass wie gewünscht funktioniert kann sich auch das Frontend auf: https://gendev.timknothe.com angesehen werden. Dort ist immer das aktuelle Frontend deployed, dieses hat aber keinen Zugriff auf das Backend, das Backend (noch) nicht über HTTPS verfügt.

### Backend

Das Backend kann mithilfe von Docker Compose gestartet werden. 
Hierbei ist zu beachten, dass eine Postgres Datenbank mitaufgestzt wird. 
In der jetzigen konfiguration wird diese Datenbank nicht verwendet, sondern eine, welche auf einem Server läuft und die Date enthält.

Alle credentials werden _im Moment_ in dem  ```docker-compose.yml``` File mitgeliefert.



Bitte kontakieren Sie mich gerne bei Fragen / Problemen 
```timknothe21@gmail.com```