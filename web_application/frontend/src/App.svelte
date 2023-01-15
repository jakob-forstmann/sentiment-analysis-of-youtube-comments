<script lang="ts">
  import Navbar from "./components/Navbar.svelte";
  import Searchbar from "./components/Searchbar.svelte";
  import VideoCard from "./components/VideoCard.svelte";
  import VideoComments from "./components/VideoComments.svelte";
  import Footer from "./components/Footer.svelte";
</script>

<Navbar />
<main>
  <Searchbar />
  <VideoCard />
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
