<script>
    import {Card} from "flowbite-svelte";

    let offer = {
        "outbounddeparturedatetime": "2021-08-01T06:00:00",
        "inbounddeparturedatetime": "2021-08-01T06:00:00",
        "inboundarrivaldatetime": "2021-08-01T08:00:00",
        "outboundarrivaldatetime": "2021-08-01T08:00:00",

        "inbounddepartureairport": "PMI",
        "outbounddepartureairport": "FRA",
        "inboundarrivalairport": "FRA",
        "outboundarrivalairport": "PMI",

        "countadults": 2,
        "countchildren": 1,
        "price": 100,
        "mealtype": "allinclusive",
        "oceanview": true,
        "roomtype": "double",

        "hotelname": "Hyatt",
        "hotelstars": 4,
    }


    export let data;


</script>
<Card>
    <p>{data.outbounddepartureairport} -  {data.outboundarrivalairport}, {data.inbounddepartureairport}
        - {data.inboundarrivalairport}</p>
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
</Card>