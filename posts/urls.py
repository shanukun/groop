from django.urls import path

from .views import (
    CreateComment,
    CreatePost,
    DeleteComment,
    DeletePost,
    LikeUnlikePost,
    PostDetailView,
    notification_view,
    post_comment_create_and_list_view,
)

app_name = "posts"

urlpatterns = [
    path("", post_comment_create_and_list_view, name="main-post-view"),
    path("notifications", notification_view, name="notification-view"),
    path("<pk>", PostDetailView.as_view(), name="post-detail-view"),
    path("api/comment/", CreateComment.as_view(), name="create-comment-view"),
    path("api/create/", CreatePost.as_view(), name="create-post-view"),
    path("api/post/delete/", DeletePost.as_view(), name="delete-post-view"),
    path("api/comment/delete/", DeleteComment.as_view(), name="delete-comment-view"),
    path("api/liked/", LikeUnlikePost.as_view(), name="like-post-view"),
]
