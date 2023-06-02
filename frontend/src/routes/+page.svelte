<script lang="ts">

    import {
        Accordion,
        AccordionItem,
        Badge,
        ButtonGroup,
        Modal,
        Textarea,
        Alert,
        ToolbarButton,
        Input,
        Button,
        Spinner,
        Toast,
    } from 'flowbite-svelte';
    import MultiSelect from 'svelte-multiselect';
    import {DateInput} from 'date-picker-svelte';
    import OfferCard from '$lib/OfferCard.svelte';
    import {offset} from '@popperjs/core';
    import {onMount} from 'svelte';
    import OfferCardHotel from "$lib/OfferCardHotel.svelte";

    function calculateDaysBetweenDates(date1: Date, date2: Date) {
        const oneDay = 24 * 60 * 60 * 1000; // hours * minutes * seconds * milliseconds
        const diffInMs = Math.abs(date2.getTime() - date1.getTime());
        const diffInDays = Math.round(diffInMs / oneDay);
        return diffInDays;
    }


    function getTimeWelcome() {
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

    let loading_results = false
    let results_here = false

    let selected = []

    let date_from: Date = new Date()
    let date_to: Date = new Date()


    let defaultModal = false;

    let badges = [
        {name: 'Mallorca', color: 'blue', class: 'm-2'},
        {name: 'Paris', color: 'blue', class: 'm-2'},
        {name: 'Sydney', color: 'blue', class: 'm-2'},
    ]

    let search_text = "Ich möchte an den Strand und in die Sonne."

    let counter_children = 0
    let counter_adults = 2

    let destination = ""

    let noariport = false


    let ai_response: string = ""

    const URL = "http://localhost:8000/aisearch"

    async function ai_search(query: string) {
        const response = await fetch(`${URL}?query=${query}`);
        const json = await response.json();
        console.log(json);
        return json;
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

    function mapAirportNameToCode(name: string): string | undefined {
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

        // Convert the name to lowercase and remove leading/trailing whitespace
        const lowercaseName = name.toLowerCase().trim();

        // Iterate over the airport map entries and find the matching code
        for (const [airportName, airportCode] of Object.entries(airportMap)) {
            if (lowercaseName === airportName.toLowerCase()) {
                return airportCode;
            }
        }

        return undefined; // If no match found, return undefined
    }


    function getAiData() {
        ai_search(search_text).then((data) => {
            console.log(data.response);
            ai_response = data.response;
            searchInAiResponse();
        }).catch((error) => {
            console.log(error);
        });
    }


    function getBadges(text: string) {
        text = text.toLowerCase()

        badges = []

        if ("sydney".indexOf(text) !== -1 || text.indexOf("sydney") !== -1) {
            badges.push({name: 'Sydney', color: 'blue', class: 'm-2'});
        }
        if ("paris".indexOf(text) !== -1 || text.indexOf("paris") !== -1) {
            badges.push({name: 'Paris', color: 'blue', class: 'm-2'});
        }
        if ("mallorca".indexOf(text) !== -1 || text.indexOf("mallorca") !== -1) {
            badges.push({name: 'Mallorca', color: 'blue', class: 'm-2'});
        }

        console.log(badges)
    }

    function searchInSearchText() {
        getBadges(search_text)
    }

    function searchInAiResponse() {
        getBadges(ai_response)
        console.log(badges)
    }

    function handleDestination(value: string) {
        console.log(value)
        destination = value
        badges = []

        getBadges(destination)
    }


    let duration = 7;


    let offers = []

    let userData = {};


    const items = Array(4);
    const close_all = () => items.forEach((_, i) => items[i] = false)
    const open_all = () => items.forEach((_, i) => items[i] = true)


    let childsFail = false;
    let adultsFail = false;

    function handleSubmit() {
        close_all();
        noariport = false;
        childsFail = false;
        adultsFail = false;
        offers = []

        destination = "Mallorca"

        if (counter_children == null || counter_children < 0 || counter_children > 10|| isNaN(counter_children)) {
            childsFail = true;
            return
        }
        if (counter_adults == null || counter_adults < 0 || counter_adults > 10 || isNaN(counter_adults)) {
            adultsFail = true;
            return
        }


        if (selected.length == 0) {
            noariport = true;
            return
        }


        loading_results = true;
        results_here = false;


        let airport = mapAirportNameToCode(selected[0]);
        let dateFrom = date_from.toISOString().substring(0, 10);
        let dateTo = date_to.toISOString().substring(0, 10);
        let countAdults = counter_adults;
        let countChildren = counter_children;
        let host = "http://localhost:8000";

        userData = {
            airport: airport,
            dateFrom: dateFrom,
            dateTo: dateTo,
            duration: duration,
            countAdults: countAdults,
            countChildren: countChildren,
        }


        let url = `${host}/offers?airport=${airport}&date_from=${dateFrom}&date_to=${dateTo}&duration=${duration}&count_adults=${countAdults}&count_children=${countChildren}`;

        fetch(url)
                .then(response => response.json())
                .then(data => {
                            offers = data;
                            loading_results = false;
                            results_here = true;
                        }
                )
                .catch(error => console.error(error));

    }


    onMount(open_all);


    let limit = 30;


    const offerDataDummy = {
        hotelid: 520,
        outbounddeparturedatetime: '2023-03-04T10:00:00',
        inbounddeparturedatetime: '2023-03-11T10:00:00',
        countadults: 2,
        countchildren: 0,
        price: 500,
        inbounddepartureairport: 'JFK',
        outboundarrivalairport: 'FRA',
        inboundarrivaldatetime: '2023-03-11T18:00:00',
        outbounddepartureairport: 'FRA',
        inboundarrivalairport: 'JFK',
        outboundarrivaldatetime: '2023-03-04T18:00:00',
        mealtype: 'All Inclusive',
        oceanview: true,
        roomtype: 'Double',
        hotel: {
            id: 1,
            name: 'Hotel A',
            stars: 4
        }
    };

    const userDataDummy = {
        airport: "CSO",
        countAdults: 2,
        countChildren: 0,
        dateFrom: "2023-06-01",
        dateTo: "2023-06-20",
        duration: 7
    }
    


</script>


<div class="m-6">
    <p class="m-2 text-lg font-normal text-gray-500 text-center lg:text-xl dark:text-gray-400">{getTimeWelcome()}</p>
    <h1 class="m-2 text-4xl font-extrabold leading-none tracking-tight text-gray-00 text-center md:text-xl lg:text-3xl dark:text-white">
        Was sind Ihre nächsten <span
            class="underline underline-offset-3 decoration-4 decoration-blue-400 dark:decoration-blue-600">Urlaubspläne?</span>
    </h1>
</div>

<Accordion multiple class="m-8">
    <AccordionItem bind:open={items[0]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>1. Reiseziehl wählen</p>
            {#if (destination !== "") }
                <Badge large>{destination}</Badge>
            {/if}
        </span>
        <form>
            <label for="chat" class="sr-only">Your message</label>
            <Alert color="dark" class="px-3 py-2">
                <svelte:fragment slot="icon">
                    <Button on:click={() => (defaultModal = true)}>Erklärung</Button>
                    <Modal id="default-modal" title="Terms of Service" bind:open={defaultModal} autoclose>
                        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                            Mithife von AI werden dir Urluaborte vorgschlagen
                        </p>
                        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                            Bitte gebe keine privaten Daten ein.
                        </p>
                        <svelte:fragment slot="footer">
                            <Button on:click={() => console.log('Handle "success"')}>Okay</Button>
                        </svelte:fragment>
                    </Modal>
                    <Textarea bind:value={search_text} on:input={searchInSearchText} id="chat" class="mx-4" rows="1"
                              placeholder="Suche nach einem Reiseziel oder Frage die AI..."/>
                    <ToolbarButton on:click={getAiData} type="submit" color="blue"
                                   class="rounded-full text-blue-600 dark:text-blue-500">
                        <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1.5"
                                stroke="currentColor"
                                class="w-6 h-6"
                        >
                            <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"/>
                        </svg>
                        <span class="sr-only">Send message</span>
                    </ToolbarButton>
                </svelte:fragment>
            </Alert>
            <p on:change={searchInAiResponse} class="m-4">{ai_response}</p>
        </form>
        <div class="flex flex-row justify-center gap-4">
            {#each badges as badge}
                <Button outline on:click={() => handleDestination(badge.name)}>
                    {badge.name}
                    <svg aria-hidden="true" class="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                         xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                              clip-rule="evenodd"></path>
                    </svg>
                </Button>
            {:else}
                <p>keine Reiseziele gefunden.</p>
            {/each}
        </div>
    </AccordionItem>
    <AccordionItem bind:open={items[1]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>2. Abflugort wählen</p>
            {#each selected as airport}
            <Badge large>{airport}</Badge>
            {/each}
        </span>
        <MultiSelect bind:selected options={airportFullNames}/>
    </AccordionItem>
    <AccordionItem bind:open={items[2]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>3. Zeitraum wählen</p>
            <Badge large><p>{date_from.toISOString().substring(0, 10)}
                - {date_to.toISOString().substring(0, 10)}</p></Badge>
        </span>
        <div class="flex flex-row justify-around">
            <div class="flex flex-row justify-center items-baseline gap-4">
                <p>vom</p>
                <DateInput bind:value={date_from} format="yyyy-MM-dd" placeholder="Select a date"/>
                <p>bis</p>
                <DateInput bind:value={date_to} format="yyyy-MM-dd" placeholder="Select a date"/>
                <p>Dauer:</p>
                <Input type="text" bind:value={duration} required/>
            </div>

        </div>
    </AccordionItem>
    <AccordionItem bind:open={items[3]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>4. weitere Informationen</p>
            <Badge large>Erwachsene: {counter_adults}</Badge> <Badge large> Kinder: {counter_children}</Badge>
        </span>
        <div class="flex flex-row justify-center items-baseline gap-4">
            <p>Erwachsene</p>
            <ButtonGroup>
                <Button outline color="red" on:click={() => counter_adults > 0 ? counter_adults-- : counter_adults}>-
                </Button>
                <Input type="text" id="first_name" bind:value={counter_adults} required/>
                <Button outline color="green" on:click={() => counter_adults < 20? counter_adults++: counter_adults}>+
                </Button>
            </ButtonGroup>
            <p>Kinder</p>
            <ButtonGroup>
                <Button outline color="red"
                        on:click={() => counter_children > 0 ? counter_children-- : counter_children}>-
                </Button>
                <Input type="text" id="first_name" bind:value={counter_children} required/>
                <Button outline color="green"
                        on:click={() => counter_children < 20 ? counter_children++: counter_children}>+
                </Button>
            </ButtonGroup>
        </div>
    </AccordionItem>
</Accordion>


<div class="flex justify-center">

    <Button on:click={handleSubmit}>
        {#if loading_results}
            <Spinner class="mr-3" size="4" color="white"/>
            Loading ...
        {:else}
            Los geht's
        {/if}
    </Button>
</div>

<ul class="flex flex-row flex-wrap gap-4 justify-start m-4 justify-items-stretch">
    {#each offers.slice(0, limit) as offer}
        <OfferCardHotel userData={userData} data={offer}/>
    {/each}
</ul>

{#if offers.length !== 0}
    <div class="flex justify-center m-4">
        <Button on:click={() => limit+=30}>
            mehr laden
            <svg aria-hidden="true" class="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                 xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd"
                      d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                      clip-rule="evenodd"></path>
            </svg>
        </Button>
    </div>
{/if}

{#if offers.length === 0 && results_here}
    <Alert class="m-8" color="red">
        <span class="font-medium">Keine Angebote gefunden.</span> Bitte wähle andere Reisedaten.
    </Alert>
{/if}


{#if noariport}
    <Alert class="m-8" color="red">
        <span class="font-medium">Kein Flughafen ausgewählt.</span> Bitte wähle einen Flughafen aus.
    </Alert>
{/if}

{#if childsFail}
    <Alert class="m-8" color="red">
        <span class="font-medium">Bitte gib einen gültigen Wert für Anazhal Kinder ein.</span> Bitte gebe eine Zahl ein.
    </Alert>
{/if}


{#if adultsFail}
    <Alert class="m-8" color="red">
        <span class="font-medium">Bitte gib einen gültigen Wert für die Anazhal der Erwachsenen ein.</span> Bitte gebe eine Zahl ein.
    </Alert>
{/if}




