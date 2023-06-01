<script>
    import {Card, Timeline, TimelineItem} from "flowbite-svelte";
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

    <script>
        import { Timeline, TimelineItem, Button } from 'flowbite-svelte';
    </script>

    <Timeline>
        <TimelineItem title="{data.outbounddepartureairport}" date="{data.outbounddeparturedatetime}">

        </TimelineItem>
        <TimelineItem title="{data.outboundarrivalairport}" date="{data.outboundarrivaldatetime}">
      
        </TimelineItem>
    </Timeline>
    <Timeline>
        <TimelineItem title="{data.inbounddepartureairport}" date="{data.inbounddeparturedatetime}">

        </TimelineItem>
        <TimelineItem title="{data.inboundarrivalairport}" date="{data.inboundarrivaldatetime}">

        </TimelineItem>
    </Timeline>


</Card>