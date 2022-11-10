// href="/like-post?post_id={{item.postContent.id}}"
$(".likePost").on("click", function () {
  let that = this;
  postId = $(this).parent().parent().parent().attr("id");
  $.ajax({
    type: "post",
    url: "/like-post",
    data: {
      post_id: postId,
    },
    success: function (result) {
      likeAction(that, result.likeCount);
    },
    error: function (err) {
      console.log(err);
    },
  });
});

const likeAction = function (likeObj, likeCount) {
  svgIcon = $(likeObj).find(".likeSvg");
  isAuthLiked = svgIcon.attr("data-active");
  if (isAuthLiked == 1) {
    svgIcon.attr("fill", "grey");
    svgIcon.attr("data-active", 0);
  } else {
    svgIcon.attr("fill", "blue");
    svgIcon.attr("data-active", 1);
  }
  curretnLikeCountSpan = $(likeObj).find(".likeCountSpan");
  if (likeCount >= 1) {
    if (!curretnLikeCountSpan.text()) {
      $(likeObj).append(
        `<p class="likeCountP" >Like by <span class="likeCountSpan">${likeCount}</span> person</p>`
      );
    } else {
      curretnLikeCountSpan.text(likeCount);
    }
  } else {
    $(likeObj).find(".likeCountP").remove();
  }
};

