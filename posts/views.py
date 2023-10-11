from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import (
    CommentActionSerializer,
    CommentSerializer,
)
from profiles.models import Profile

from .models import Like, Post



@login_required
def post_comment_create_and_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.filter(Q(author__friends__profile=profile) | Q(author=profile))
    profile = Profile.objects.get(user=request.user)

    # initials
    p_form = PostModelForm()
    post_added = False

    if "submit_p_form" in request.POST:
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True


    context = {
        "qs": qs,
        "profile": profile,
        "p_form": p_form,
        "post_added": post_added,
    }

    return render(request, "posts/main.html", context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        # created or fetched
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        # if fetched - there is an existent value to it
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value = "Like"

            post_obj.save()
            like.save()
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



class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
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
    model = Post
    template_name = "posts/update.html"
    success_url = reverse_lazy("posts:main-post-view")

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(
                None, "You need to be the author of the post in order to update it"
            )
            return super().form_invalid(form)
