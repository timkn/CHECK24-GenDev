<script lang="ts">

    import Card from "$lib/Card.svelte";

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

    const ui_libs = [`München`, `Köln`, `Berlin`, `Hamburg`]

    let selected = []

    let defaultModal = false;


    import {Badge, ButtonGroup, Datepicker, FloatingLabelInput, Modal} from 'flowbite-svelte';

    import {Button} from 'flowbite-svelte';


    import {Textarea, Alert, ToolbarButton, Label, Input} from 'flowbite-svelte';

    import {Search} from 'flowbite-svelte';

    function handleVoiceBtn() {
        alert('You clicked voice button');
    }


</script>


<style>
    * {
        font-family: Poppins, sans-serif;
    }

</style>

<p>{getTimeWelcome()} What's your next plans?</p>

<code>selected = {JSON.stringify(selected)}</code>


<Card class="search-card">
    <form>
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            1. Wähle dein Reiseziel
        </h5>
        <script>
            import {Button, Modal} from 'flowbite-svelte';

            let defaultModal = false;
        </script>
        <label for="chat" class="sr-only">Your message</label>
        <Alert color="dark" class="px-3 py-2">
            <svelte:fragment slot="icon">

                <Button on:click={() => (defaultModal = true)}>erklärung</Button>
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
                <Textarea id="chat" class="mx-4" rows="1" placeholder="Your message..."/>
                <ToolbarButton type="submit" color="blue" class="rounded-full text-blue-600 dark:text-blue-500">
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
        <Badge>Mallorca</Badge>
        <Badge>Bali</Badge>
        <Badge>Madrid</Badge>
    </form>
</Card>

<Card>
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        2. Wähle deine Flughäfen
    </h5>
    <MultiSelect bind:selected options={ui_libs}/>
</Card>

<Card>
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        3. deine Reisedaten
    </h5>
    <Datepicker range/>
</Card>


<Card>
    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        4. weitere Informationen
    </h5>
    <p>Adults</p>
    <ButtonGroup>
        <Button outline color="red">-</Button>
        <Input type="text" id="first_name" value="2" required/>
        <Button outline color="green">+</Button>
    </ButtonGroup>

    <p>Children (14yo)</p>
    <ButtonGroup>
        <Button outline color="red">-</Button>
        <Input type="text" id="first_name" value="0" required/>
        <Button outline color="green">+</Button>
    </ButtonGroup>

</Card>

<Button class="m-8">Search</Button>



