<script>
    import Nav from "$lib/Nav.svelte";
    import Footer from "$lib/Footer.svelte";
    import "@fontsource/poppins";
</script>

<style lang="sass">
    *
      font-family: Poppins, sans-serif
</style>


<Nav/>

<slot />

<Footer/>
