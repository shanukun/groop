from django.urls import path

from .views import (
    PostDeleteView,
    PostUpdateView,
    like_unlike_post,
    CreateComment,
    DeleteComment,
    post_comment_create_and_list_view,
)

app_name = "posts"

urlpatterns = [
    path("", post_comment_create_and_list_view, name="main-post-view"),
    path("liked/", like_unlike_post, name="like-post-view"),
    path("<pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("api/comment/", CreateComment.as_view(), name="create-comment-view"),
    path("api/comment/delete/", DeleteComment.as_view(), name="delete-comment-view"),
]
