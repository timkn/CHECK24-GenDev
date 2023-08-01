<script>
    import "../app.postcss";
    import Nav from "$lib/Nav.svelte";
    import "@fontsource/poppins";
  import Footer from "$lib/Footer.svelte";
</script>

<Nav/>

<slot/>


<Footer />




<style l>
    * {
        font-family: Poppins, sans-serif;
    }
</style>
