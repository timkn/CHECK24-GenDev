<script lang="ts">
    import {Badge, Card, Mark, P, Rating, Timeline, TimelineItem} from "flowbite-svelte";

    export let data;

    function toGermanDate(dateString: string): string {
        const date = new Date(dateString);
        const formattedDate = date.toLocaleDateString('de-De', {
            month: '2-digit',
            day: '2-digit',
            year: 'numeric'
        }).replace(/\//g, '.');
        return formattedDate;
    }

    function toGermanTime(timeString: string): string {
        const date = new Date(timeString);
        const formattedTime = date.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
        return formattedTime;
    }


    function get_persons_text(countAdults, countChildren) {
        let text = "";
        if (countAdults === 1) {
            text += "1 Erwachsener";
        } else if (countAdults > 1) {
            text += `${countAdults} Erwachsene`;
        }

        if (countChildren === 1) {
            text += ", 1 Kind";
        } else if (countChildren > 1) {
            text += `, ${countChildren} Kinder`;
        }

        return text;
    }

    function get_mealtype_text(mealtype) {
        switch (mealtype) {
            case "NONE":
                return "Ohne Verpflegung"
            case "BREAKFAST":
                return "Frühstück"
            case "HALFBOARD":
                return "Halbpension"
            case "FULLBOARD":
                return "Vollpension"
            case "ALLINCLUSIVE":
                return "All Inclusive"
            default:
                return mealtype;
        }
    }

    function mapCodeToAirportName(code: string): string | undefined {
        const airportMap: { [key: string]: string } = {
            "AMS": "Amsterdam Airport Schiphol",
            "BER": "Berlin Brandenburg Airport",
            "BLL": "Billund Airport",
            "BRE": "Bremen Airport",
            "BRN": "Bern Airport",
            "BRU": "Brussels Airport",
            "BSL": "EuroAirport Basel-Mulhouse-Freiburg",
            "CGN": "Cologne Bonn Airport",
            "CRL": "Brussels South Charleroi Airport",
            "CSO": "Copenhagen Airport",
            "DRS": "Dresden Airport",
            "DTM": "Dortmund Airport",
            "DUS": "Düsseldorf Airport",
            "EIN": "Eindhoven Airport",
            "ERF": "Erfurt-Weimar Airport",
            "FDH": "Friedrichshafen Airport",
            "FKB": "Karlsruhe/Baden-Baden Airport",
            "FMM": "Memmingen Airport",
            "FMO": "Münster Osnabrück International Airport",
            "FRA": "Frankfurt Airport",
            "GRZ": "Graz Airport",
            "GVA": "Geneva Airport",
            "GWT": "Westerland Sylt Airport",
            "HAJ": "Hannover Airport",
            "HAM": "Hamburg Airport",
            "HHN": "Frankfurt-Hahn Airport",
            "INN": "Innsbruck Airport",
            "KLU": "Klagenfurt Airport",
            "KRK": "John Paul II International Airport Kraków-Balice",
            "KSF": "Kassel Airport",
            "LBC": "Lübeck Airport",
            "LEJ": "Leipzig/Halle Airport",
            "LNZ": "Linz Airport",
            "LUX": "Luxembourg Airport",
            "MUC": "Munich Airport",
            "NRN": "Weeze Airport",
            "NUE": "Nuremberg Airport",
            "PAD": "Paderborn Lippstadt Airport",
            "PRG": "Václav Havel Airport Prague",
            "RLG": "Rostock-Laage Airport",
            "RTM": "Rotterdam The Hague Airport",
            "SCN": "Saarbrücken Airport",
            "STR": "Stuttgart Airport",
            "SXB": "Strasbourg Airport",
            "SZG": "Salzburg Airport",
            "VIE": "Vienna International Airport",
            "WAW": "Warsaw Chopin Airport",
            "ZRH": "Zurich Airport",
            "PMI": "Palma de Mallorca Airport",
        };

        return airportMap[code];
    }

    function getRoomTypeText(roomstype:string) {
        switch (roomstype) {
            case "ACCORDINGDESCRIPTION":
                return "Laut Beschreibung"
            case "DOUBLE":
                return "Doppelzimmer"
            case "SINGLE":
                return "Einzelzimmer"
            case "SUITE":
                return "Suite"
            case "STUDIO":
                return "Studio"
            case "TRIPLE":
                return "Dreibettzimmer"
            case "APARTMENT":
                return "Apartment"
            default:
                return roomstype;
        }
    }





</script>
<Card>
    <div class="flex flex-row my-4 gap-16">
        <div>
            <p class="my-2">Zimmer:</p>
            <Badge large>{getRoomTypeText(data.roomtype)}</Badge>

            <p class="my-2">Verpfelgung:</p>
            <Badge large>{get_mealtype_text(data.mealtype)}</Badge>
        </div>

        <div>

            <Timeline order="vertical">
                <TimelineItem title={toGermanDate(data.outbounddeparturedatetime)}
                              date={toGermanTime(data.outbounddeparturedatetime)}>
                    <svelte:fragment slot="icon">
                    <span class="flex absolute -left-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900">
                       <svg class="h-8 w-8 text-red-500" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
                            stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path
                               stroke="none" d="M0 0h24v24H0z"/>  <path
                               d="M15 12h5a2 2 0 0 1 0 4h-15l-3 -6h3l2 2h3l-2 -7h3z"
                               transform="rotate(-15 12 12) translate(0 -1)"/>  <line x1="3" y1="21" x2="21" y2="21"/></svg>
                    </svelte:fragment>
                    <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">
                        {mapCodeToAirportName(data.outbounddepartureairport)}                    </p>
                </TimelineItem>
                <TimelineItem title={toGermanDate(data.outboundarrivaldatetime)} date={toGermanTime(data.outboundarrivaldatetime)}>
                    <svelte:fragment slot="icon">
                <span
                        class="flex absolute -left-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900">
                    <svg class="h-8 w-8 text-red-500" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
                         stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path
                            stroke="none" d="M0 0h24v24H0z"/>  <path
                            d="M15 12h5a2 2 0 0 1 0 4h-15l-3 -6h3l2 2h3l-2 -7h3z"
                            transform="rotate(15 12 12) translate(0 -1)"/>  <line x1="3" y1="21" x2="21" y2="21"/></svg>
                </span>
                    </svelte:fragment>
                    <p class="text-base font-normal text-gray-500 dark:text-gray-400">
                        {mapCodeToAirportName(data.outboundarrivalairport)}
                    </p>
                </TimelineItem>
            </Timeline>
            <Timeline order="vertical">
                <TimelineItem title={toGermanDate(data.inbounddeparturedatetime)}
                              date={toGermanTime(data.inbounddeparturedatetime)}>
                    <svelte:fragment slot="icon">
                    <span class="flex absolute -left-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900">
                   <svg class="h-8 w-8 text-red-500" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
                        stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path
                           stroke="none" d="M0 0h24v24H0z"/>  <path
                           d="M15 12h5a2 2 0 0 1 0 4h-15l-3 -6h3l2 2h3l-2 -7h3z"
                           transform="rotate(-15 12 12) translate(0 -1)"/>  <line x1="3" y1="21" x2="21" y2="21"/></svg>
                    </svelte:fragment>
                    <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">
                        {mapCodeToAirportName(data.inbounddepartureairport)}</p>
                </TimelineItem>
                <TimelineItem title={toGermanDate(data.inboundarrivaldatetime)} date={toGermanTime(data.inboundarrivaldatetime)}>
                    <svelte:fragment slot="icon">
                <span
                        class="flex absolute -left-3 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-8 ring-white dark:ring-gray-900 dark:bg-primary-900">
                    <svg class="h-8 w-8 text-red-500" width="24" height="24" viewBox="0 0 24 24" stroke-width="2"
                         stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path
                            stroke="none" d="M0 0h24v24H0z"/>  <path
                            d="M15 12h5a2 2 0 0 1 0 4h-15l-3 -6h3l2 2h3l-2 -7h3z"
                            transform="rotate(15 12 12) translate(0 -1)"/>  <line x1="3" y1="21" x2="21" y2="21"/></svg>
                </span>
                    </svelte:fragment>
                    <p class="text-base font-normal text-gray-500 dark:text-gray-400">
                        {mapCodeToAirportName(data.inboundarrivalairport)}
                    </p>
                </TimelineItem>
            </Timeline>
        </div>
    </div>
    <div class="flex justify-between items-center">
        <div class="flex items-baseline">
            <div class="flex items-baseline text-gray-900 dark:text-white">
                <span class="text-2xl font-extrabold tracking-tight">{data.price}</span>
                <span class="text-1xl font-semibold">€</span>
            </div>
            <P class="mx-2 mb-3" weight="light" color="text-gray-500 dark:text-gray-400">
                ({get_persons_text(data.countadults, data.countchildren)})</P>
        </div>
    </div>

</Card>



