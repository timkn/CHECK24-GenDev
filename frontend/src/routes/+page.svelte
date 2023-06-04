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
        Card, FloatingLabelInput,
    } from 'flowbite-svelte';


    import MultiSelect from 'svelte-multiselect';
    import {DateInput} from 'date-picker-svelte';
    import {onMount} from 'svelte';
    import OfferCardHotel from "$lib/OfferCardHotel.svelte";

    import {getWelcomeText, mapAirportNameToCode} from "../page";
    import {getAirportList} from "../page.js";


    let host = "http://localhost:8000";

    let loading_results = false
    let results_here = false
    let selected = ["Munich Airport"]
    let date_from: Date = new Date()
    let date_to: Date = new Date()
    date_to.setDate(date_to.getDate() + 8);
    let counter_children = 0
    let counter_adults = 2


    let destination = ""
    let noariport = false
    let ai_response: string = ""


    let defaultModal = false;

    let search_text = "Ich möchte an den Strand und in die Sonne."


    let badges = [
        {name: 'Mallorca', color: 'blue', class: 'm-2'},
        {name: 'Paris', color: 'blue', class: 'm-2'},
        {name: 'Sydney', color: 'blue', class: 'm-2'},
        {name: 'New York', color: 'blue', class: 'm-2'},
    ]




    const URL = "http://localhost:8000/gpt_destination_search"

    async function ai_search(query: string) {
        const response = await fetch(`${URL}?user_promt=${query}`);
        const json = await response.json();
        console.log(json);
        return json;
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
        if ("ney york".indexOf(text) !== -1 || text.indexOf("new york") !== -1) {
            badges.push({name: 'New York', color: 'blue', class: 'm-2'});
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


    let showDestinationDescriptionCard = false;
    let destinationDescriptionCard = {
        "destination": "",
        "description": "",
    }

    function handleDestinationDescriptionCard(destination:string, dateFrom:string, dateTo:string, countAdults:number, countChildren:number) {


        let url = `${host}/gpt_destination_description?destination=${destination}&outbounddeparturedatetime=${dateFrom}&inboundarrivaldatetime=${dateTo}&duration=${duration}&count_adults=${countAdults}&count_children=${countChildren}`;

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
        noariport = false;
        childsFail = false;
        adultsFail = false;
        showDestinationDescriptionCard = false;
        destinationDescriptionCard.description = "";
        destinationDescriptionCard.destination = "";

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

        console.log(airport)

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
                            handleDestinationDescriptionCard(destination, dateFrom, dateTo, countAdults, countChildren);
                        }
                )
                .catch(error => console.error(error));

    }


    onMount(open_all);


    let limit = 30;


</script>


<div class="m-6">
    <p class="m-2 text-lg font-normal text-gray-500 text-center lg:text-xl dark:text-gray-400">{getWelcomeText()}</p>
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
            <label class="sr-only">Your message</label>
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
        <MultiSelect bind:selected options={getAirportList()}/>
    </AccordionItem>
    <AccordionItem bind:open={items[2]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>3. Zeitraum wählen</p>
            <Badge large><p>{date_from.toISOString().substring(0, 10)}
                - {date_to.toISOString().substring(0, 10)}</p></Badge>
        </span>
        <div class="flex flex-row justify-around">
            <div class="flex flex-row justify-center items-center gap-4">
                <p>Zeitspanne von</p>
                <DateInput bind:value={date_from} format="dd.MM.yyyy" placeholder="Select a date"/>
                <p>bis</p>
                <DateInput bind:value={date_to} format="dd.MM.yyyy" placeholder="Select a date"/>
                <p>Dauer:</p>
                <ButtonGroup>
                    <Button>7 Tage</Button>
                    <Button>10 Tage</Button>
                    <Button>14 Tage</Button>
                </ButtonGroup>
                <FloatingLabelInput bind:value={duration} style="outlined" id="floating_outlined" name="floating_outlined" type="number" label="Dauer in Tagen" />
            </div>

        </div>
    </AccordionItem>
    <AccordionItem bind:open={items[3]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>4. abschließende Informationen</p>
            <Badge large>Erwachsene: {counter_adults}</Badge> <Badge large> Kinder: {counter_children}</Badge>
        </span>
        <div class="flex flex-row justify-center items-baseline gap-4">
            <p>Erwachsene</p>
            <ButtonGroup>
                <Button outline color="red" on:click={() => counter_adults > 0 ? counter_adults-- : counter_adults}>-
                </Button>
                <Input type="number" id="first_name" bind:value={counter_adults} required/>
                <Button outline color="green" on:click={() => counter_adults < 20? counter_adults++: counter_adults}>+
                </Button>
            </ButtonGroup>
            <p>Kinder</p>
            <ButtonGroup>
                <Button outline color="red"
                        on:click={() => counter_children > 0 ? counter_children-- : counter_children}>-
                </Button>
                <Input type="number" id="first_name" bind:value={counter_children} required/>
                <Button outline color="green"
                        on:click={() => counter_children < 20 ? counter_children++: counter_children}>+
                </Button>
            </ButtonGroup>
        </div>
        <div class="flex justify-center m-4">
            <Button on:click={handleSubmit}>
                {#if loading_results}
                    <Spinner class="mr-3" size="4" color="white"/>
                    Loading ...
                {:else}
                    Suche Angebote
                {/if}
            </Button>
        </div>
    </AccordionItem>
</Accordion>





<ul class="grid grid-cols-3 gap-4 m-8">
    {#each offers.slice(0, limit) as offer, index}
        {#if offers.length >= 3? index === 3: index === 0}
                <div class="p-6 bg-white border border-gray-200 rounded-lg shadow col-span-3 justify-self-stretch ">
                    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{destinationDescriptionCard.destination}</h5>
                        {#if destinationDescriptionCard.description}
                            <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
                                {destinationDescriptionCard.description}
                            </p>
                        {:else}
                            <div class="flex justify-center gap-4 items-center">
                            <Spinner />
                            <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
                                Beschreibung für Mallorca wird geladen...                            </p>
                            </div>
                        {/if}
                </div>
        {/if}
        <OfferCardHotel userData={userData} data={offer}/>
    {/each}
</ul>

{#if offers.length !== 0 && results_here && offers.length > limit}
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




