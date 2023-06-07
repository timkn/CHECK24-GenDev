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
        Spinner
    } from 'flowbite-svelte';


    import MultiSelect from 'svelte-multiselect';
    import {DateInput} from 'date-picker-svelte';
    import {onMount} from 'svelte';
    import OfferCardHotel from "$lib/OfferCardHotel.svelte";

    import {getBadges, getWelcomeText, mapAirportNameToCode} from "../page";
    import {getAirportList, toGermanDate} from "../page.js";

    let HOST = "http://localhost:8000";
    let loadingOffers = false
    let isInitailOffers = true;
    let selectedAirports = ["Munich Airport"]
    let dateFrom: Date = new Date()
    let dateTo: Date = new Date()
    let counterChildren = 0
    let counterAdults = 2
    let destination = ""
    let noAirport = false
    let aiSearchDestinationText: string = ""
    let explainationAIModal = false;
    let searchDestinationText = "Ich möchte an den Strand und in die Sonne."
    let loadingDestinationSearch = false;
    let duration = 7;
    let offers = []
    let userData = {};
    let limit = 30;

    dateTo.setDate(dateTo.getDate() + 8);



    const fromCards = Array(4);
    const close_all = () => fromCards.forEach((_, i) => fromCards[i] = false)
    const open_all = () => fromCards.forEach((_, i) => fromCards[i] = true)


    let childsFail = false;
    let adultsFail = false;


    let showDestinationDescriptionCard = false;
    let destinationDescriptionCard = {
        "destination": "",
        "description": "",
    }


    let badges = [
        {name: 'Mallorca', color: 'blue', class: 'm-2'},
        {name: 'Paris', color: 'blue', class: 'm-2'},
        {name: 'Sydney', color: 'blue', class: 'm-2'},
        {name: 'New York', color: 'blue', class: 'm-2'},
    ]


    function destinationSearch() {
        loadingDestinationSearch = true;
        fetch(`${HOST}/gpt_destination_search?user_promt=${searchDestinationText}`)
                .then(response => response.json())
                .then(data => {
                            aiSearchDestinationText = data.response;
                            updateBadges(aiSearchDestinationText);
                            loadingDestinationSearch = false;
                        }
                )
                .catch(error => console.error(error));
    }


    function updateBadges(text: string) {
        badges = getBadges(text)
    }



    function handleDestination(value: string) {
        console.log(value)
        destination = value
        badges = getBadges(destination)
    }


    function handleDestinationDescriptionCard(destination: string, dateFrom: string, dateTo: string, countAdults: number, countChildren: number) {


    let url = `${HOST}/gpt_destination_description?destination=${destination}&outbounddeparturedatetime=${dateFrom}&inboundarrivaldatetime=${dateTo}&duration=${duration}&count_adults=${countAdults}&count_children=${countChildren}`;
    destinationDescriptionCard.description = "";
    destinationDescriptionCard.destination = "";
    fetch(url)
            .then(response => response.json())
            .then(data => {
                        destinationDescriptionCard.destination = destination;
                        destinationDescriptionCard.description = data.response;
                        showDestinationDescriptionCard = true;
                    }
            )
            .catch(error => console.error(error));

    }

    function handleSubmit() {
        close_all();
        noAirport = false;
        childsFail = false;
        adultsFail = false;
        showDestinationDescriptionCard = false;
        limit = 30;


        offers = []

        destination = "Mallorca"

        if (counterChildren == null || counterChildren < 0 || counterChildren > 10 || isNaN(counterChildren)) {
            childsFail = true;
            open_all();
            return
        }
        if (counterAdults == null || counterAdults < 0 || counterAdults > 10 || isNaN(counterAdults)) {
            adultsFail = true;
            open_all();
            return
        }

        if (selectedAirports.length == 0) {
            noAirport = true;
            open_all();
            return
        }


        loadingOffers = true;


        let paramAirport = mapAirportNameToCode(selectedAirports[0]);
        let paramDateFrom = dateFrom.toISOString().substring(0, 10);
        let paramDateTo = dateTo.toISOString().substring(0, 10);
        let paramCountAdults = counterAdults;
        let paramCountChildren = counterChildren;
        let paramDuration = duration;
        let paparamDestination = destination;


        userData = {
            airport: paramAirport,
            dateFrom: paramDateFrom,
            dateTo: paramDateTo,
            duration: paramDuration,
            countAdults: paramCountAdults,
            countChildren: paramCountChildren,
        }


        let url = `${HOST}/offers?airport=${paramAirport}&date_from=${paramDateFrom}&date_to=${paramDateTo}&duration=${paramDuration}&count_adults=${paramCountAdults}&count_children=${paramCountChildren}`;

        fetch(url)
                .then(response => response.json())
                .then(data => {
                            offers = data;
                            loadingOffers = false;
                            isInitailOffers = false;
                            handleDestinationDescriptionCard(paparamDestination, paramDateFrom, paramDateTo, paramCountAdults, paramCountChildren);
                        }
                )
                .catch(error => console.error(error));
    }

    onMount(open_all);
</script>


<div class="m-6">
    <p class="m-2 text-lg font-normal text-gray-500 text-center lg:text-xl dark:text-gray-400">{getWelcomeText()}</p>
    <h1 class="m-2 text-4xl font-extrabold leading-none tracking-tight text-gray-00 text-center md:text-xl lg:text-3xl dark:text-white">
        Was sind Ihre nächsten <span
            class="underline underline-offset-3 decoration-4 decoration-blue-400 dark:decoration-blue-600">Urlaubspläne?</span>
    </h1>
</div>

<Accordion multiple class="m-8">
    <AccordionItem bind:open={fromCards[0]}>
        <span slot="header" class="flex flex-row gap-4 flex-wrap">
            <p>1. Reiseziehl wählen</p>
            {#if (destination !== "") }
                <Badge large>{destination}</Badge>
            {/if}
        </span>
        <form>
            <Alert color="dark" class="px-3 py-2 flex-wrap">
                <svelte:fragment slot="icon">
                    <Button on:click={() => (explainationAIModal = true)}>Erklärung</Button>
                    <Modal id="default-modal" title="Terms of Service" bind:open={explainationAIModal} autoclose>
                        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                            Mithilfe von Künstlicher Intelligenz werden Ihen Urlaubsorte vorgeschlagen.
                            Probieren Sie zum Beispiel "Ich möchte in eine eine echte Großstadt, aber auch ans Meer" oder "Ich möchte auf eine Insel" oder "Ich möchte in eine historische Weltmetropole".
                        </p>
                        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                            Bitte geben Sie keine privaten Daten ein.
                        </p>
                        <svelte:fragment slot="footer">
                            <Button on:click={() => console.log('Handle "success"')}>Okay</Button>
                        </svelte:fragment>
                    </Modal>
                    <Textarea bind:value={searchDestinationText} on:input={() => updateBadges(searchDestinationText)} id="chat" class="mx-4" rows="1"
                              placeholder="Suche nach einem Reiseziel oder Frage die AI..."/>
                    <ToolbarButton on:click={destinationSearch} type="submit" color="blue"
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
            {#if loadingDestinationSearch}
                <div class="flex justify-center m-4">
                    <Spinner />
                </div>
                {:else}
            <p class="m-4">{aiSearchDestinationText}</p>
            {/if}
        </form>
        <div class="flex flex-row justify-center gap-4 flex-wrap">
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
    <AccordionItem bind:open={fromCards[1]}>
        <span slot="header" class="flex flex-row gap-4 flex-wrap">
            <p>2. Abflugort wählen</p>
            {#each selectedAirports as airport}
            <Badge large>{airport}</Badge>
            {/each}
        </span>
        <MultiSelect bind:value={selectedAirports} options={getAirportList()}/>
    </AccordionItem>
    <AccordionItem bind:open={fromCards[2]}>
        <span slot="header" class="flex flex-row gap-4 flex-wrap">
            <p>3. Zeitraum wählen</p>
            <Badge large><p>{toGermanDate(dateFrom)} -> {toGermanDate(dateTo)}</p></Badge>
        </span>
        <div class="flex flex-row justify-around">
            <div class="flex flex-row justify-center items-center gap-4 flex-wrap">
                <p>Zeitspanne von</p>
                <DateInput bind:value={dateFrom} format="dd.MM.yyyy" placeholder="Select a date"/>
                <p>bis</p>
                <DateInput bind:value={dateTo} format="dd.MM.yyyy" placeholder="Select a date"/>
                <p>Dauer (Tage):</p>
                <ButtonGroup>
                    <Button on:click={() => duration = 7}>7</Button>
                    <Button on:click={() => duration = 10}>10</Button>
                    <Button on:click={() => duration = 14}>14</Button>
                    <Input bind:value={duration} type="number" id="first_name" placeholder="Dauer in Tagen" required  />

                </ButtonGroup>
            </div>

        </div>
    </AccordionItem>
    <AccordionItem bind:open={fromCards[3]}>
        <span slot="header" class="flex flex-row gap-4 flex-wrap">
            <p>4. abschließende Informationen</p>
            <Badge large>Erwachsene: {counterAdults}</Badge> <Badge large> Kinder: {counterChildren}</Badge>
        </span>
        <div class="flex flex-row justify-center items-baseline gap-4 flex-wrap">
            <p>Erwachsene</p>
            <ButtonGroup>
                <Button outline color="red" on:click={() => counterAdults > 0 ? counterAdults-- : counterAdults}>-
                </Button>
                <Input type="number" id="first_name" bind:value={counterAdults} required/>
                <Button outline color="green" on:click={() => counterAdults < 20? counterAdults++: counterAdults}>+
                </Button>
            </ButtonGroup>
            <p>Kinder</p>
            <ButtonGroup>
                <Button outline color="red"
                        on:click={() => counterChildren > 0 ? counterChildren-- : counterChildren}>-
                </Button>
                <Input type="number" id="first_name" bind:value={counterChildren} required/>
                <Button outline color="green"
                        on:click={() => counterChildren < 20 ? counterChildren++: counterChildren}>+
                </Button>
            </ButtonGroup>
        </div>
        <div class="flex justify-center m-4">
            <Button on:click={handleSubmit}>
                {#if loadingOffers}
                    <Spinner class="mr-3" size="4" color="white"/>
                    Loading ...
                {:else}
                    Suche Angebote
                {/if}
            </Button>
        </div>
    </AccordionItem>
</Accordion>




<ul class="grid grid-cols-2 gap-4 m-8">
    {#each offers.slice(0, limit) as offer, index}
        {#if offers.length > 3 ? index === 2 : index === 0}
            <div class="p-6 bg-white border border-gray-200 rounded-lg shadow col-span-2 justify-self-stretch">
                <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{destinationDescriptionCard.destination}</h5>
                {#if destinationDescriptionCard.description}
                    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
                        {destinationDescriptionCard.description}
                    </p>
                {:else}
                    <div class="flex justify-center gap-4 items-center">
                        <Spinner/>
                        <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
                            Beschreibung für Mallorca wird geladen... </p>
                    </div>
                {/if}
            </div>
        {/if}
        <OfferCardHotel userData={userData} data={offer}/>
    {/each}
</ul>

{#if offers.length !== 0 && !loadingOffers && offers.length > limit}
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

{#if offers.length === 0 && !loadingOffers && !isInitailOffers}
    <Alert class="m-8" color="red">
        <span class="font-medium">Keine Angebote gefunden.</span> Bitte wähle andere Reisedaten.
    </Alert>
{/if}


{#if noAirport}
    <Alert class="m-8" color="red">
        <span class="font-medium">Kein Flughafen ausgewählt.</span> Bitte wähle einen Flughafen aus.
    </Alert>
{/if}

{#if childsFail}
    <Alert class="m-8" color="red">
        <span class="font-medium">Bitte gib einen gültigen Wert für Anzahl Kinder ein.</span> Bitte gebe eine Zahl ein / max 20.
    </Alert>
{/if}


{#if adultsFail}
    <Alert class="m-8" color="red">
        <span class="font-medium">Bitte gib einen gültigen Wert für die Anzahl der Erwachsenen ein.</span> Bitte gebe
        eine Zahl ein / max 20.
    </Alert>
{/if}




