<script>
  import { onDestroy } from "svelte";
  import { allVideoComments } from "../stores/CommentStore";
  import CommentsCard from "./CommentsCard.svelte";

  let videoComments = [];
  let commentsClasses = [];

  const unSubscribeAllVideoComments = allVideoComments.subscribe((comments) => {
    videoComments = comments;
    const lengthOfComments = videoComments.length;
    const negative = lengthOfComments * 0.2;
    const positive = negative + lengthOfComments * 0.5;
    const neutral = positive + lengthOfComments * 0.3;

    commentsClasses = [
      {
        head: "Negative",
        percentage: "20",
        comments: videoComments.slice(0, negative),
      },
      {
        head: "Positive",
        percentage: "50",
        comments: videoComments.slice(negative, positive),
      },
      {
        head: "Neutral",
        percentage: "30",
        comments: videoComments.slice(positive, neutral),
      },
    ];

    console.log("Second: ", videoComments[videoComments.length - 1]);
    console.log("First: ", videoComments[0]);
  });

  onDestroy(unSubscribeAllVideoComments);
</script>

<div class="classification">
  {#each commentsClasses as commentsClass}
    <CommentsCard
      head={commentsClass.head}
      comments={commentsClass.comments}
      percentage={commentsClass.percentage}
    />
  {/each}
</div>

<style>
  .classification {
    margin: 10px 0px 0px 0px;
    display: flex;
    justify-content: space-between;
    align-items: stretch;
  }
</style>
