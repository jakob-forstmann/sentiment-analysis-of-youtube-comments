<script>
  export let head;
  export let comments;
  export let percentage;
</script>

<div class={comments.length <= 0 ? "hidden" : ""}>
  <div class="analytics">
    <h3 class="head">{head}</h3>
    <h6 class="percentage">{percentage}%</h6>
  </div>

  <div class="comments">
    <ol>
      {#each comments as comment}
        <li class="comment">
          {comment}
        </li>
      {/each}
    </ol>
  </div>
</div>

<style>
  .hidden {
    display: none;
  }

  .comments {
    border: 1px solid #37525a; 
    background-color: #c6e3eb;
    margin: 0px 10px 0px 10px;
    min-width: 19vw;
    max-width: 19vw;
  }

  .comments ol {
    height: 50vh;
    overflow-y: scroll;
  }

  .comments ol li{
    border: 0.5px solid #37525a; 
    background-color: #c6e3eb;
  }
</style>
