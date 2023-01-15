<script>
</script>

<div class="video-card">
  <div class="card-left">
    <div class="card-thumbnail">
      <span class="no-likes">5 Likes</span>
      <span class="no-comments">10 Comments</span>
      <span class="no-views">100 Views</span>
    </div>
  </div>
  <div class="card-right">
    <h1 class="card-title">Title of the Video</h1>
    <p class="card-description">
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptates
      eligendi velit, doloribus ut ducimus laborum, et vitae iusto nobis omnis a
      impedit repudiandae laudantium voluptate vero eos nostrum quas illum? Ipsa
      deleniti totam dolor vel, laboriosam ex natus! Odit inventore mollitia
      corporis doloribus quaerat, vel totam illum labore repellendus similique
      porro perferendis non dolores! Exercitationem dolorem facilis quis officia
      facere?
    </p>
  </div>
</div>

<style>
  .video-card {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    max-width: 500px;
    max-height: 6em;
    background-color: lightcyan;
  }

  .card-left {
    display: flex;
    align-items: center;
    justify-content: stretch;
  }

  .card-thumbnail {
    height: 6em;
    width: 6em;
    display: flex;
    justify-content: flex-end;
    flex-direction: column;
    align-items: flex-start;
    background-color: rgb(135, 206, 250);
  }

  .card-thumbnail span {
    font-weight: 200;
    font-size: 12px;
    text-decoration: underline;
  }

  .card-right {
    height: 6em;
  }

  .card-title {
    font-weight: 300;
    font-size: 1.5em;
    height: 30%;
    background-color: rgba(135, 206, 250, 0.3);
  }

  .card-description {
    font-weight: 200;
    font-size: 0.8em;
    height: 70%;
    overflow-y: scroll;
  }
</style>
