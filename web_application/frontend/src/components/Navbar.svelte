<script>
  export let name;
</script>

<navbar class="navbar">
  <div class="logo"><h1>{name}</h1></div>
</navbar>

<style>
  .navbar {
    height: 10vh;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 0.1em black solid;
  }
</style>
