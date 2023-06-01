<script>
    import { Card, Rating, Button, Modal } from "flowbite-svelte";
    import OfferSmall from "./OfferSmall.svelte";
    import { onMount } from 'svelte';
    let offer = {
        "outbounddeparturedatetime" : "2021-08-01T06:00:00",
        "inbounddeparturedatetime" : "2021-08-01T06:00:00",
        "inboundarrivaldatetime" : "2021-08-01T08:00:00",
        "outboundarrivaldatetime" : "2021-08-01T08:00:00",

        "inbounddepartureairport" : "PMI",
        "outbounddepartureairport" : "FRA",
        "inboundarrivalairport" : "FRA",
        "outboundarrivalairport" : "PMI",

        "countadults" : 2,
        "countchildren" : 1,
        "price" : 100,
        "mealtype" : "allinclusive",
        "oceanview" : true,
        "roomtype" :"double",

        "hotelname" : "Hyatt",
        "hotelstars" : 4,
    }

    export let userData;
    export let data;

    console.log(data);

    let clickOutsideModal = false;

    let offers = [];
    let loading_results = false;
    let results_here = false;
    let host = "http://localhost:8000";

    function get_offers() {
      loading_results = true;
      results_here = false;
    

      let url = `${host}/hotel/${data.hotelid}/offers?airport=${userData.airport}&date_from=${userData.dateFrom}&date_to=${userData.dateTo}&duration=${userData.duration}&count_adults=${userData.countAdults}&count_children=${userData.countChildren}`;

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
      
    

</script>
<Card on:click={() => clickOutsideModal = true}>
  <div class="flex flex-row justify-between items-baseline">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{data.hotel.name}</h5>
    <Rating id="example-1" total={5} size={20} rating={data.hotel.stars} />
  </div>
    <p>{data.outbounddepartureairport} -  {data.outboundarrivalairport}, {data.inbounddepartureairport} - {data.inboundarrivalairport}</p>
    <p>
      {data.countadults} Erwachsene -
      {data.countchildren} Kind(er) 
    </p>
    <p>
      {data.outbounddeparturedatetime} - {data.outboundarrivaldatetime}
      {data.inbounddeparturedatetime} - {data.inboundarrivaldatetime}
    </p>
    <div class="flex flex-row justify-between items-baseline">
      <div>
        <p class="text-1xl font-bold">{data.mealtype}</p>
      </div>
      <div class="flex items-baseline text-gray-900 dark:text-white">
        <span class="text-2xl font-extrabold tracking-tight">{data.price}</span>
        <span class="text-1xl font-semibold">€</span>
    </div>
    </div>
    <Button on:click={() => {
      clickOutsideModal = true
      get_offers()
      }}>more</Button>

    
</Card>

<Modal title="{data.hotel.name}" bind:open={clickOutsideModal} size="xl" autoclose outsideclose>
  <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
    Alle Angebote von dem Hotel:
<div class="flex flex-row flex-wrap gap-4">
  {#each offers as offer}
  <OfferSmall data={offer}></OfferSmall>
{/each}
</div>
   

</Modal>