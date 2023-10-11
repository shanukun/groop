from django.urls import path

from .views import (
    FollowSendReq,
    ProfileDetailView,
    ProfileListView,
    accept_invatation,
    invites_received_view,
    my_profile_view,
    reject_invatation,
    remove_from_friends,
    send_invatation,
)

app_name = "profiles"

urlpatterns = [
    path("", ProfileListView.as_view(), name="all-profiles-view"),
    path("myprofile/", my_profile_view, name="my-profile-view"),
    path("send-invite/", send_invatation, name="send-invite"),
    path("remove-friend/", remove_from_friends, name="remove-friend"),
    path("<slug>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("my-invites/acctept/", accept_invatation, name="accept-invite"),
    path("my-invites/reject/", reject_invatation, name="reject-invite"),
    path("search_profile/", search_profile_view, name="search-profile-view"),
    path("follow_send_req/", FollowSendReq.as_view(), name="follow-send-req"),
]
