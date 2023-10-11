from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Comment, Post
from profiles.serializers import FollowUnfollowReqSerializer

from .models import Profile, Relationship


def get_user_info_for_view(profile):
    context = {}

    # rel_r = Relationship.objects.filter(follower=profile)
    following = Profile.objects.get_leaders(profile)
    followers = Profile.objects.get_followers(profile)
    follower_cnt = followers.count()

    context["profile"] = profile
    context["follower_cnt"] = follower_cnt
    context["posts"] = Post.objects.get_author_posts(profile)
    context["followers"] = followers
    context["following"] = following
    context["comments"] = Comment.objects.filter(author=profile)

    return context


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    context = get_user_info_for_view(profile)
    return render(request, "profiles/user_profile.html", context)


@login_required
def accept_req(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == "send":
            rel.status = "accepted"
            rel.save()
    return redirect("profiles:notifications")


@login_required
def reject_req(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect("profiles:notifications")


@login_required
def search_profile_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_follow(user)

    context = {"qs": qs}

    return render(request, "profiles/search_profile.html", context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = kwargs.get("object")
        context = get_user_info_for_view(profile)
        return context


class FollowSendReq(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        follow = FollowUnfollowReqSerializer(data=request.data)
        follower = Profile.objects.get(user=request.user)

        if follow.is_valid():
            follow_req = follow.save()
            leader = Profile.objects.get(pk=follow_req.leader_id)
            if Relationship.objects.follow_unfollow(follower, leader):
                return Response({"msg": "Follow request sent."})
            else:
                return Response({"msg": "Unfollowed."})
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
def unfollow_leader(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver))
            | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("profiles:my-profile-view")
