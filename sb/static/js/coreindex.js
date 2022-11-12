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
$(".commentShowBtn").on("click", function () {
  commentSection = $(this)
    .parent()
    .parent()
    .parent()
    .parent()

    .find(".commentSection");

  console.log("---------", commentSection);
  postId = $(this).parent().parent().parent().attr("id");
  //call comment

  $.ajax({
    type: "get",
    url: `/post/${postId}/comments`,

    success: function (result) {
      console.log(result);
      refreshComments(commentSection, result);
      commentSection.toggleClass("show");
    },
    error: function (err) {
      console.log(err);
    },
  });
});

const refreshComments = function (commentObj, data) {
  commentContainer = $(commentObj).find(".commentContainer");
  commentList = [];
  data.map((el) => {
    commentList.push(`<div class="commentItem">

    <img
      src=${el.authImg}
      alt="avatar"
      class="avatarImg"
    />
  
    <div class="commentContent">
     
      <div class="commentContentHeader">
      
        <div class="dropdown">
          <i
            role="button"
            class="fa fa-ellipsis-h"
            type="button"
            data-toggle="dropdown"
            aria-expanded="false"
          >
          </i>
    
          <div class="dropdown-menu">
            <a class="dropdown-item" href="#">Edit comment</a>
            <a class="dropdown-item" href="#">Delete comment</a>
          </div>
        </div>
      </div>
      <p class="commentContentName">${el.authUserName}</p>
      <p class="commentContentText">
      ${el.item.content}
      </p>
    </div>
    </div> `);
  });
  commentContainer.html(commentList);
};

const addToComments = function (commentContainer, data) {
  console.log("_______________OKOKOK", commentContainer);
  commentContainer.append(`<div class="commentItem">

    <img
      src=${data.authImg}
      alt="avatar"
      class="avatarImg"
    />
  
    <div class="commentContent">
     
      <div class="commentContentHeader">
      
        <div class="dropdown">
          <i
            role="button"
            class="fa fa-ellipsis-h"
            type="button"
            data-toggle="dropdown"
            aria-expanded="false"
          >
          </i>
    
          <div class="dropdown-menu">
            <a class="dropdown-item" href="#">Edit comment</a>
            <a class="dropdown-item" href="#">Delete comment</a>
          </div>
        </div>
      </div>
      <p class="commentContentName">${data.authUserName}</p>
      <p class="commentContentText">
      ${data.item.content}
      </p>
    </div>
    </div> `);
};
