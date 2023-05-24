<script lang="ts">

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
            console.log('Good morning!');
            return 'Good morning!';
        } else if (currentHour >= noonThreshold && currentHour < afternoonThreshold) {
            console.log('Good noon!');
            return 'Good noon!';
        } else if (currentHour >= afternoonThreshold && currentHour < eveningThreshold) {
            console.log('Good afternoon!');
            return 'Good afternoon!';
        } else if (currentHour >= eveningThreshold && currentHour < nightThreshold) {
            console.log('Good evening!');
            return 'Good evening!';
        } else {
            console.log('Good night!');
            return 'Good night!';
        }


    }

    import MultiSelect from 'svelte-multiselect'

    const ui_libs = [`München`, `React`, `Vue`, `Angular`, `...`]

    let selected = []

    import { Card } from 'flowbite-svelte'
    let defaultModal = false;




</script>


<style>
    * {
        font-family: Poppins, sans-serif;
    }

</style>

<p>{getTimeWelcome()} What's your next plans?</p>

<code>selected = {JSON.stringify(selected)}</code>

<h2>Von wo möchtest du Fliegen?</h2>
<MultiSelect bind:selected options={ui_libs}/>


<Card href="/cards">
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        Noteworthy technology acquisitions 2021
    </h5>
    <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
        Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.
    </p>
</Card>