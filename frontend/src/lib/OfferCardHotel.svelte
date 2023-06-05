<script>
    import {
        Card,
        Rating,
        Button,
        Modal,
        Badge,
        P,
        Mark,
        TableBodyCell,
        TableBodyRow,
        TableBody,
        TableHeadCell, TableHead, Table, Heading, Spinner, Radio
    } from "flowbite-svelte";
    import OfferSmall from "./OfferSmall.svelte";
    import {onMount} from 'svelte';

    export let userData;
    export let data;

    let clickOutsideModal = false;
    let offers = [];
    let loading_results = true;
    let results_here = false;
    let host = "http://localhost:8000";

    function get_offers() {
        loading_results = true;
        results_here = false;

        let url = `${host}/hotel/${data.id}/offers?airport=${userData.airport}&date_from=${userData.dateFrom}&date_to=${userData.dateTo}&duration=${userData.duration}&count_adults=${userData.countAdults}&count_children=${userData.countChildren}`;

        fetch(url)
                .then(response => response.json())
                .then(data => {
                            offers = data;
                            sort_by_price_low();
                            loading_results = false;
                            results_here = true;
                        }
                )
                .catch(error => console.error(error));

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

    function sort_by_price_low() {
        offers = offers.sort((a, b) => (a.price > b.price) ? 1 : -1)
    }

    function sort_by_price_high() {
        offers = offers.sort((a, b) => (a.price < b.price) ? 1 : -1)
    }

    function sort_by_date_low() {
        offers = offers.sort((a, b) => new Date(a.outbounddeparturedatetime) - new Date(b.outbounddeparturedatetime));
    }

    function sort_by_date_high() {
        offers = offers.sort((a, b) => new Date(b.outbounddeparturedatetime) - new Date(a.outbounddeparturedatetime));
    }



</script>
<Card on:click={() => {
    get_offers()
    clickOutsideModal = true
    }}
      class="cursor-pointer" size="lg" padding='xl'>
    <div class="flex flex-row justify-between items-baseline">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white mr-4">{data.name}</h5>
        <Rating id="example-1" total={5} size={20} rating={data.stars}/>
    </div>
    <div class="flex justify-between items-center">
        <div class="flex items-baseline">
            <div class="flex items-baseline text-gray-900 dark:text-white">
                <span class="text-2xl font-extrabold tracking-tight">{data.price}</span>
                <span class="text-1xl font-semibold">€</span>
            </div>
            <P class="mx-2 mb-3" weight="light" color="text-gray-500 dark:text-gray-400">
                ({get_persons_text(userData.countAdults, userData.countChildren)})</P>
        </div>

        <Button on:click={() => {
      clickOutsideModal = true
      get_offers()
      }}>mehr Angebote
        </Button>
    </div>
</Card>

<Modal title="Alle Angebote" bind:open={clickOutsideModal} size="xl">
    <div class="flex flex-row justify-between items-baseline">
        <Heading tag="h2" class='mb-4 mx-4'>
            <Mark>{data.name}</Mark>
        </Heading>
        <Rating class="mx-4" id="example-1" total={5} size={40} rating={data.stars}/>
    </div>

    <ul class="items-center w-full rounded-lg border border-gray-200 sm:flex dark:bg-gray-800 dark:border-gray-600 divide-x divide-gray-200 dark:divide-gray-600">
        <li class="w-full"><Radio on:click={sort_by_price_high} name="hor-list" class="p-3">Preis (höchster zu erst)</Radio></li>
        <li class="w-full"><Radio on:click={sort_by_date_low} name="hor-list" class="p-3">Datum (frühstmöglich)</Radio></li>
        <li class="w-full"><Radio on:click={sort_by_date_high} name="hor-list" class="p-3">Datum (am spätesten)</Radio></li>
        <li class="w-full"><Radio on:click={sort_by_price_low} name="hor-list" class="p-3">Preis (niedrigster zu erst)</Radio></li>
    </ul>




    <div class="flex flex-row flex-wrap gap-4 justify-center">
        {#if loading_results}
            <Spinner />
        {/if}
        {#each offers as offer}
            <OfferSmall data={offer}></OfferSmall>
        {/each}
    </div>


</Modal>