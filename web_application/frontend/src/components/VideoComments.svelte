<script>
  import CommentsCard from "./CommentsCard.svelte";
</script>

<div class="classification">
  <CommentsCard head="Negative" />
  <CommentsCard head="Neutral" />
  <CommentsCard head="Positive" />
</div>

<style>
  .classification {
    margin: 10px 0px 0px 0px;
    display: flex;
    justify-content: space-between;
    align-items: stretch;
  }
</style>
