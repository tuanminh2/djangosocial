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

//COMMENTS-------------
$(".commentPostStart").on("click", function () {
  commentContainer = $(this)
    .parent()
    .parent()
    .parent()
    .parent()

    .find(".commentContainer");

  postId = $(this).parent().parent().parent().attr("id");
  //call comment

  $.ajax({
    type: "get",
    url: `/post/${postId}/comments`,
    data: {
      csrfmiddlewaretoken: "{{ csrf_token }}",
    },
    success: function (result) {
      console.log(result.comments);

      showPostComments(commentContainer, result.comments);
    },
    error: function (err) {
      console.log(err);
    },
  });
});

const showPostComments = function (commentObj, data) {
  data.map((item) => {
    
  });
  commentObj.toggleClass("show");
};

//Post comment
$(document).on("click", ".postCommentBtn", function () {});

//COMMENT===============
