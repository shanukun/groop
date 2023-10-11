from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import (
    CommentActionSerializer,
    CommentSerializer,
    PostActionSerializer,
    PostSerializer,
)
from profiles.models import Profile

from .models import Comment, Like, Notification, Post


@login_required
def post_comment_create_and_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.get_my_posts(profile)

    context = {
        "qs": qs,
        "profile": profile,
    }

    return render(request, "posts/main.html", context)


class CreatePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        print(request.data)
        post_serializer = PostSerializer(data=request.data)
        profile = Profile.objects.get(user=request.user)

        if post_serializer.is_valid():
            post = post_serializer.save()
            post = Post.objects.create(
                content=post.body, image=post.image, author=profile
            )
            return Response({"post_id": post.id})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        comment_serializer = CommentSerializer(data=request.data)
        profile = Profile.objects.get(user=request.user)

        if comment_serializer.is_valid():
            comment = comment_serializer.save()
            post = Post.objects.get(pk=comment.post_id)
            Comment.objects.create(author=profile, post=post, body=comment.body)

            return Response({"post_id": comment.post_id})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeUnlikePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        print(request.data)
        like_serializer = PostActionSerializer(data=request.data)
        profile = Profile.objects.get(user=request.user)

        if like_serializer.is_valid():
            like = like_serializer.save()
            addition = Like.objects.like_unlike_post(like.post_id, profile)
            return Response({"add": addition})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeletePost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        print(request.data)
        post_serializer = PostActionSerializer(data=request.data)
        profile = Profile.objects.get(user=request.user)

        if post_serializer.is_valid():
            post = post_serializer.save()
            addition = Post.objects.get(id=post.post_id).delete()
            return Response({"add": addition})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        print(request.data)
        comment_serializer = CommentActionSerializer(data=request.data)
        profile = Profile.objects.get(user=request.user)

        if comment_serializer.is_valid():
            comment = comment_serializer.save()
            addition = Comment.objects.get(id=comment.comment_id).delete()
            return Response({"add": addition})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_view.html"

    def get_object(self, *args, **kwargs):
        return Post.objects.get_post(self.kwargs.get("pk"), self.request.user)

    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        post = kwargs.get("object")
        context["post"] = post
        context["profile"] = profile
        context["comments"] = Comment.objects.filter(post__id=post.id)
        return context

