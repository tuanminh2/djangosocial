const likeAction = function (likeObj, likeCount) {
  svgIcon = $(likeObj).find(".likeSvg");

  if (svgIcon.attr("fill") == "grey") {
    svgIcon.attr("fill", "blue");
  } else {
    svgIcon.attr("fill", "grey");
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
$(document).on("click", ".commentShowBtn", function () {
  commentSection = $(this)
    .parent()
    .parent()
    .parent()
    .parent()

    .find(".commentSection");

  postId = $(this).parent().parent().parent().attr("id");
  //call comment
  if (commentSection.attr("data-show") == 0) {
    $.ajax({
      type: "get",
      url: `/post/${postId}/comments`,

      success: function (result) {
        refreshComments(commentSection, result);
        commentSection.attr("data-show", 1);
        commentSection.addClass("show");
      },
      error: function (err) {
        console.log(err);
      },
    });
  } else {
    commentSection.attr("data-show", 0);
    commentSection.removeClass("show");
  }
});

const refreshComments = function (commentObj, data) {
  commentContainer = $(commentObj).find(".commentContainer");
  commentList = [];
  let parser = new DOMParser();
  data.map((el) => {

    commentData = `<div id=${el.item.id} class="commentItem">

    <img
      src=${el.authImg}
      alt="avatar"
      class="avatarImg"
    />
  
    <div class="commentContent">
     
      <div class="commentContentHeader">`;
    commentData += el.optionHTML;
    commentData += `</div>
      <p class="commentContentName">${el.authUserName}</p>
      <input disabled class="commentContentText" value="${el.item.content}" />
      
     
    </div>
    </div> `;

    commentList.push(commentData);
  });
  commentContainer.html(commentList);
};

const addToComments = function (commentContainer, data) {
  commentContainer.append(`<div id=${data.item.id} class="commentItem">

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
            <span class="dropdown-item editCommentBtn" >Edit comment</span>
            <span class="dropdown-item deleteCommentBtn" >Delete comment</span>
          </div>
        </div>
      </div>
      <p class="commentContentName">${data.authUserName}</p>
      <input disabled class="commentContentText" value="${data.item.content}" />
     
     
    </div>
    </div> `);
};

$(document).on("click", ".editCommentBtn", function () {
  commentContent = $(this).parent().parent().parent().parent();
  commentInput = commentContent.find(".commentContentText");
  commentContent.append(
    "<div class='commentOpt'><button class='cancelUpdateCommentBtn uk-button uk-button-secondary'>CANCEL</button> <button class='updateCommentBtn uk-button uk-button-primary'>SAVE</button><div>"
  );

  commentInput.attr("disabled", false);
  commentInput.focus();
});

$(document).on("click", ".cancelUpdateCommentBtn", function () {
  commentContentText = $(this).parent().parent().find(".commentContentText");
  commentOpt = $(this).parent();

  commentContentText.attr("disabled", true);
  commentOpt.remove();
});
