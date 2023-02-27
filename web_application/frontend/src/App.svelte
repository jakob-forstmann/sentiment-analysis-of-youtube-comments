<script lang="ts">
  export let name;

  import Navbar from "./components/Navbar.svelte";
  import Searchbar from "./components/Searchbar.svelte";
  import VideoComments from "./components/VideoComments.svelte";
  import Footer from "./components/Footer.svelte";
</script>

<Navbar {name} />
<main>
  <Searchbar />
  <VideoComments />
</main>
<Footer />

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    height: 80vh;
    width: 100%;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
