from django.urls import path

from .views import (
    ProfileDetailView,
    ProfileListView,
    accept_invatation,
    invite_profiles_list_view,
    invites_received_view,
    my_profile_view,
    profiles_list_view,
    reject_invatation,
    remove_from_friends,
    send_invatation,
)

app_name = "profiles"

urlpatterns = [
    path("", ProfileListView.as_view(), name="all-profiles-view"),
    path("myprofile/", my_profile_view, name="my-profile-view"),
    path("my-invites/", invites_received_view, name="my-invites-view"),
    path("to-invite/", invite_profiles_list_view, name="invite-profiles-view"),
    path("send-invite/", send_invatation, name="send-invite"),
    path("remove-friend/", remove_from_friends, name="remove-friend"),
    path("<slug>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("my-invites/acctept/", accept_invatation, name="accept-invite"),
    path("my-invites/reject/", reject_invatation, name="reject-invite"),
]
