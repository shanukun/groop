from django.urls import path

from .views import (
    FollowSendReq,
    ProfileDetailView,
    accept_req,
    my_profile_view,
    reject_req,
    search_profile_view,
    unfollow_leader,
)

app_name = "profiles"

urlpatterns = [
    path("user/", my_profile_view, name="my-profile-view"),
    path("user/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("search_profile/", search_profile_view, name="search-profile-view"),
    path("follow_send_req/", FollowSendReq.as_view(), name="follow-send-req"),
    path("unfollow/", unfollow_leader, name="unfollow-leader"),
    path("reqs/acctept/", accept_req, name="accept-req"),
    path("reqs/reject/", reject_req, name="reject-req"),
]
