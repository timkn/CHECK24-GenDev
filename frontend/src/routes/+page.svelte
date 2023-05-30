<svelte:head>

</svelte:head>


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
        Datepicker,
    } from 'flowbite-svelte';
    import MultiSelect from 'svelte-multiselect'


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


    const ui_libs = [`München`, `Köln`, `Berlin`, `Hamburg`]

    let selected = []

    let defaultModal = false;
</script>


<div class="m-6">
    <p class="m-2 text-lg font-normal text-gray-500 text-center lg:text-xl dark:text-gray-400">{getTimeWelcome()}</p>
    <h1 class="m-2 text-4xl font-extrabold leading-none tracking-tight text-gray-00 text-center md:text-xl lg:text-3xl dark:text-white">
        Was sind Ihre nächsten <span
            class="underline underline-offset-3 decoration-4 decoration-blue-400 dark:decoration-blue-600">Urlaubspläne?</span>
    </h1>
</div>

<Accordion multiple class="m-8">
    <AccordionItem open>
        <span slot="header"> Wähle Sie ihr Reiseziel</span>
        <form>
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
    </AccordionItem>
    <AccordionItem open>
    <span slot="header" class="text-base flex gap-2">
        <p>1.</p>
      <span> My Header 1</span>
        <p>Hey</p>
    </span>
        <code>selected = {JSON.stringify(selected)}</code>
        <MultiSelect bind:selected options={ui_libs}/>
    </AccordionItem>
    <AccordionItem open>
        <span slot="header">Wähle deine Flughäfen</span>
        <Datepicker range/>
    </AccordionItem>
    <AccordionItem open>
        <span slot="header">Weitere Inbfromationen</span>
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
    </AccordionItem>
</Accordion>

<button type="button"
        class="m-8 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Los geht's
    <svg aria-hidden="true" class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20"
         xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd"
              d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
              clip-rule="evenodd"></path>
    </svg>
</button>
