<script>
    import { Card, Rating, Button, Modal } from "flowbite-svelte";
    import OfferSmall from "./OfferSmall.svelte";
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

    let clickOutsideModal = false;


</script>
<Card on:click={() => clickOutsideModal = true}>
  <div class="flex flex-row justify-between items-baseline">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{offer.hotelname}</h5>
    <Rating id="example-1" total={5} size={20} rating={offer.hotelstars} />
  </div>
    <p>{offer.outbounddepartureairport} -  {offer.outboundarrivalairport}, {offer.inbounddepartureairport} - {offer.inboundarrivalairport}</p>
    <p>
      {offer.countadults} Erwachsene -
      {offer.countchildren} Kind(er) 
    </p>
    <p>
      {offer.outbounddeparturedatetime} - {offer.outboundarrivaldatetime}
      {offer.inbounddeparturedatetime} - {offer.inboundarrivaldatetime}
    </p>
    <div class="flex flex-row justify-between items-baseline">
      <div>
        <p class="text-1xl font-bold">{offer.mealtype}</p>
      </div>
      <div class="flex items-baseline text-gray-900 dark:text-white">
        <span class="text-2xl font-extrabold tracking-tight">{offer.price}</span>
        <span class="text-1xl font-semibold">€</span>
    </div>
    </div>
    <Button on:click={() => clickOutsideModal = true}>more</Button>

    
</Card>

<Modal title="{offer.hotelname}" bind:open={clickOutsideModal} size="xl" autoclose outsideclose>
  <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
    Alle Angebote von dem Hotel:
  <OfferSmall></OfferSmall>

</Modal>