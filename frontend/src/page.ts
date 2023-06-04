export function getWelcomeText() {
    // Create a new Date object
    const currentDate: Date = new Date();

    // Get the current hour (0-23)
    const currentHour: number = currentDate.getHours();

    // Define the threshold values for each phase
    const morningThreshold: number = 6;     // 6 AM
    const noonThreshold: number = 12;       // 12 PM
    const afternoonThreshold: number = 13;  // 1 PM
    const eveningThreshold: number = 18;    // 6 PM
    const nightThreshold: number = 22;      // 10 PM

    // Compare the current hour to determine the phase of the day
    if (currentHour >= morningThreshold && currentHour < noonThreshold) {
        return 'Guten Morgen!';
    } else if (currentHour >= noonThreshold && currentHour < afternoonThreshold) {
        return 'Guten Mittag!';
    } else if (currentHour >= afternoonThreshold && currentHour < eveningThreshold) {
        return 'Guten Tag!';
    } else if (currentHour >= eveningThreshold && currentHour < nightThreshold) {
        return 'Guten Abend!';
    } else {
        return 'Guten Tag!';
    }
}

const airportFullNames: string[] = [
    "Amsterdam Airport Schiphol",
    "Berlin Brandenburg Airport",
    "Billund Airport",
    "Bremen Airport",
    "Bern Airport",
    "Brussels Airport",
    "EuroAirport Basel-Mulhouse-Freiburg",
    "Cologne Bonn Airport",
    "Brussels South Charleroi Airport",
    "Copenhagen Airport",
    "Dresden Airport",
    "Dortmund Airport",
    "Düsseldorf Airport",
    "Eindhoven Airport",
    "Erfurt-Weimar Airport",
    "Friedrichshafen Airport",
    "Karlsruhe/Baden-Baden Airport",
    "Memmingen Airport",
    "Münster Osnabrück International Airport",
    "Frankfurt Airport",
    "Graz Airport",
    "Geneva Airport",
    "Westerland Sylt Airport",
    "Hanover Airport",
    "Hamburg Airport",
    "Frankfurt-Hahn Airport",
    "Innsbruck Airport",
    "Klagenfurt Airport",
    "John Paul II International Airport Kraków-Balice",
    "Kassel Airport",
    "Lübeck Airport",
    "Leipzig/Halle Airport",
    "Linz Airport",
    "Luxembourg Airport",
    "Munich Airport",
    "Weeze Airport",
    "Nuremberg Airport",
    "Paderborn Lippstadt Airport",
    "Václav Havel Airport Prague",
    "Rostock-Laage Airport",
    "Rotterdam The Hague Airport",
    "Saarbrücken Airport",
    "Stuttgart Airport",
    "Strasbourg Airport",
    "Salzburg Airport",
    "Vienna International Airport",
    "Warsaw Chopin Airport",
    "Zurich Airport",
];


export function getAirportList(): string[] {
    return airportFullNames;
}

export function mapAirportNameToCode(name: string): string | undefined {
    const airportMap: { [key: string]: string } = {
        "Amsterdam Airport Schiphol": "AMS",
        "Berlin Brandenburg Airport": "BER",
        "Billund Airport": "BLL",
        "Bremen Airport": "BRE",
        "Bern Airport": "BRN",
        "Brussels Airport": "BRU",
        "EuroAirport Basel-Mulhouse-Freiburg": "BSL",
        "Cologne Bonn Airport": "CGN",
        "Brussels South Charleroi Airport": "CRL",
        "Copenhagen Airport": "CSO",
        "Dresden Airport": "DRS",
        "Dortmund Airport": "DTM",
        "Düsseldorf Airport": "DUS",
        "Eindhoven Airport": "EIN",
        "Erfurt-Weimar Airport": "ERF",
        "Friedrichshafen Airport": "FDH",
        "Karlsruhe/Baden-Baden Airport": "FKB",
        "Memmingen Airport": "FMM",
        "Münster Osnabrück International Airport": "FMO",
        "Frankfurt Airport": "FRA",
        "Graz Airport": "GRZ",
        "Geneva Airport": "GVA",
        "Westerland Sylt Airport": "GWT",
        "Hannover Airport": "HAJ",
        "Hamburg Airport": "HAM",
        "Frankfurt-Hahn Airport": "HHN",
        "Innsbruck Airport": "INN",
        "Klagenfurt Airport": "KLU",
        "John Paul II International Airport Kraków-Balice": "KRK",
        "Kassel Airport": "KSF",
        "Lübeck Airport": "LBC",
        "Leipzig/Halle Airport": "LEJ",
        "Linz Airport": "LNZ",
        "Luxembourg Airport": "LUX",
        "Munich Airport": "MUC",
        "Weeze Airport": "NRN",
        "Nuremberg Airport": "NUE",
        "Paderborn Lippstadt Airport": "PAD",
        "Václav Havel Airport Prague": "PRG",
        "Rostock-Laage Airport": "RLG",
        "Rotterdam The Hague Airport": "RTM",
        "Saarbrücken Airport": "SCN",
        "Stuttgart Airport": "STR",
        "Strasbourg Airport": "SXB",
        "Salzburg Airport": "SZG",
        "Vienna International Airport": "VIE",
        "Warsaw Chopin Airport": "WAW",
        "Zurich Airport": "ZRH",
    };

    return airportMap[name.trim()];
}