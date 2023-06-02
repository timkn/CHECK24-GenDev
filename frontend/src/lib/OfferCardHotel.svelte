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
        TableHeadCell, TableHead, Table, Heading
    } from "flowbite-svelte";
    import OfferSmall from "./OfferSmall.svelte";
    import {onMount} from 'svelte';

    export let userData;
    export let data;

    let clickOutsideModal = false;
    let offers = [];
    let loading_results = false;
    let results_here = false;
    let host = "http://localhost:8000";

    function get_offers() {
        loading_results = true;
        results_here = false;

        console.log(userData);
        console.log(data);


        let url = `${host}/hotel/${data.id}/offers?airport=${userData.airport}&date_from=${userData.dateFrom}&date_to=${userData.dateTo}&duration=${userData.duration}&count_adults=${userData.countAdults}&count_children=${userData.countChildren}`;

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

    function toGermanDate(dateString) {
        const date = new Date(dateString);
        const formattedDate = date.toLocaleDateString('de-De', {
            month: '2-digit',
            day: '2-digit',
            year: 'numeric'
        }).replace(/\//g, '.');
        return formattedDate;
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

    function getRoomTypeText(roomstype) {
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

<Modal title="Alle Angebote" bind:open={clickOutsideModal} size="xl" autoclose outsideclose>
    <div class="flex flex-row justify-between items-baseline">
        <Heading tag="h2" class='mb-4 mx-4'>
            <Mark>{data.name}</Mark>
        </Heading>
        <Rating class="mx-4" id="example-1" total={5} size={40} rating={data.stars}/>
    </div>
    <div class="flex flex-row flex-wrap gap-4 justify-center">
        {#each offers as offer}
            <OfferSmall data={offer}></OfferSmall>
        {/each}
    </div>


</Modal>