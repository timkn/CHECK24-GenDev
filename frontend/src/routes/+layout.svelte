<script>
    import "../app.postcss";
    import Nav from "$lib/Nav.svelte";
    import Footer from "$lib/Footer.svelte";
    import "@fontsource/poppins";
</script>

<Nav/>

<slot/>

<Footer/>

<style l>
    * {
        font-family: Poppins, sans-serif;
    }
</style>
