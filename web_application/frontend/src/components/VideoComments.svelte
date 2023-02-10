<script>
  import { onDestroy } from "svelte";
  import { allVideoComments } from "../stores/CommentStore";
  import CommentsCard from "./CommentsCard.svelte";

  let classifiedCommentsDetails = [];
  const calculatePercentage = (length, total) => Math.round((length * 100) / total);
  const unSubscribeAllVideoComments = allVideoComments.subscribe((comments) => {
    if (!comments.length) {
      return;
    }
    comments = JSON.parse(comments);

    const negative = comments.negative, positive = comments.positive, neutral = comments.neutral;
    const noOfNegative = comments.negative.length, noOfPositive = comments.positive.length, noOfNeutral = comments.neutral.length;
    const total = noOfNegative + noOfPositive + noOfNeutral;

    classifiedCommentsDetails = [
      {
        head: "Negative",
        percentage: calculatePercentage(noOfNegative, total),
        comments: negative,
      },
      {
        head: "Positive",
        percentage: calculatePercentage(noOfPositive, total),
        comments: positive,
      },
      {
        head: "Neutral",
        percentage: calculatePercentage(noOfNeutral, total),
        comments: neutral,
      },
    ];
  });

  onDestroy(unSubscribeAllVideoComments);
</script>

<div class="classification">
  {#each classifiedCommentsDetails as commentDetail}
    <CommentsCard
      head={commentDetail.head}
      comments={commentDetail.comments}
      percentage={commentDetail.percentage}
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
