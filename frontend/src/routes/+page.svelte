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
    } from 'flowbite-svelte';
    import MultiSelect from 'svelte-multiselect';
    import { DateInput } from 'date-picker-svelte';
    import OfferCard from '$lib/OfferCard.svelte';
    import { offset } from '@popperjs/core';
    import { onMount } from 'svelte';

    function calculateDaysBetweenDates(date1:Date, date2:Date) {
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
            console.log('Guten Morgen!');
            return 'Guten Morgen!';
        } else if (currentHour >= noonThreshold && currentHour < afternoonThreshold) {
            console.log('Guten Mittag!');
            return 'Guten Mittag!';
        } else if (currentHour >= afternoonThreshold && currentHour < eveningThreshold) {
            console.log('Good Tag!');
            return 'Guten Tag!';
        } else if (currentHour >= eveningThreshold && currentHour < nightThreshold) {
            console.log('Good Abend!');
            return 'Guten Abend!';
        } else {
            console.log('Good Tag!');
            return 'Guten Tag!';
        }


    }


    const airports = [`München`, `Köln`, `Berlin`, `Hamburg`]

    let selected = []

    let date_from:Date = new Date()
    let date_to:Date = new Date()


    let defaultModal = false;

    let badges = [
        {name: 'Mallorca', color: 'blue', class: 'm-2'},
        {name: 'Paris', color: 'blue', class: 'm-2'},
        {name: 'Kreta', color: 'blue', class: 'm-2'},
        {name: 'Sydney', color: 'blue', class: 'm-2'},
    ]

    let search_text = "Ich möchte an den Strand und in die Sonne."

    let counter_children = 0
    let counter_adults = 2

    let destination = ""



    let ai_response:string = ""

    const URL = "http://144.24.175.18:8000/aisearch"
    async function ai_search(query: string) {
        const response = await fetch(`${URL}?query=${query}`);
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
    
        if ("kreta".indexOf(text) !== -1    || text.indexOf("kreta") !== -1) {
            badges.push({name: 'Kreta', color: 'blue', class: 'm-2'});
        }
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

    function handleDestination(value:string) {
        console.log(value)
        destination = value
        badges = []

        getBadges(destination)
    }



    let duration = 0;



    const items = Array(4);
    const close_all= () => items.forEach((_,i)=> items[i] = false)
    const open_all = () => items.forEach((_,i)=> items[i] = true)

        function handleSubmit() {
            close_all();

            let airport = "PMI";
        let dateFrom = "2021-08-01";
        let dateTo = "2021-08-08";
        let duration = 7;
        let countAdults = 2;
        let countChildren = 1;
        let host = "http://localhost:8000";

        let url = `${host}/offers?airport=${airport}&date_from=${dateFrom}&date_to=${dateTo}&duration=${duration}&count_adults=${countAdults}&count_children=${countChildren}`;

        fetch(url)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    }




    onMount(open_all);

    






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
                    <Textarea bind:value={search_text} on:input={searchInSearchText} id="chat" class="mx-4" rows="1" placeholder="Suche nach einem Reiseziel oder Frage die AI..."/>
                    <ToolbarButton on:click={getAiData} type="submit" color="blue" class="rounded-full text-blue-600 dark:text-blue-500">
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
                {badge.name} <svg aria-hidden="true" class="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
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
        <MultiSelect bind:selected options={airports}/>
    </AccordionItem>
    <AccordionItem bind:open={items[2]}>
        <span slot="header" class="flex flex-row gap-4">
            <p>3. Zeitraum wählen</p>
            <Badge large><p>{date_from.getDay()}.{date_from.getMonth()}.{date_from.getFullYear()} - {date_to.getDay()}.{date_to.getMonth()}.{date_to.getFullYear()}</p></Badge>
        </span>
        <div class="flex flex-row justify-around">
            <div class="flex flex-row justify-center items-baseline gap-4">
                <p>vom</p>
                <DateInput bind:value={date_from} placeholder="Select a date"/>
                <p>bis</p>
                <DateInput bind:value={date_to} placeholder="Select a date"/>
                <p>Dauer:</p>
                <Input type="text"  bind:value={duration} required/>
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
                <Button outline color="red" on:click={() => counter_adults > 0 ? counter_adults-- : counter_adults}>-</Button>
                <Input type="text" id="first_name" bind:value={counter_adults} required/>
                <Button outline color="green" on:click={() => counter_adults < 20? counter_adults++: counter_adults}>+</Button>
            </ButtonGroup>
            <p>Kinder</p>
            <ButtonGroup>
                <Button outline color="red" on:click={() => counter_children > 0 ? counter_children-- : counter_children}>-</Button>
                <Input type="text" id="first_name" bind:value={counter_children} required/>
                <Button outline color="green" on:click={() => counter_children < 20 ? counter_children++: counter_children}>+</Button>
            </ButtonGroup>
        </div>
    </AccordionItem>
</Accordion>



<button on:click={handleSubmit}   type="button"
        class="m-8 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Los geht's
    <svg aria-hidden="true" class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20"
         xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd"
              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
              clip-rule="evenodd"></path>
    </svg>
</button>


<code>selected = {JSON.stringify(selected)}</code>



<OfferCard></OfferCard>