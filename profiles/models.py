from django.contrib.auth.models import User
from django.db import models
from django.db.models import BooleanField, ExpressionWrapper, Q, Subquery
from django.shortcuts import reverse


class ProfileManager(models.Manager):
    def get_all_profiles_to_follow(self, user):
        my_profile = Profile.objects.get(user=user)
        following = Relationship.objects.filter(follower=my_profile)
        profiles = Profile.objects.exclude(
            Q(id__in=Subquery(following.values("leader"))) | Q(user=user)
        )

        return profiles

    def get_followers(self, profile):
        # profile = Profile.objects.get(user=user)
        followers = Relationship.objects.filter(leader=profile).values("follower")
        leaders = Relationship.objects.filter(follower=profile).values("leader")

        followers_profile = Profile.objects.annotate(
            follows=ExpressionWrapper(
                Q(pk__in=leaders),
                output_field=BooleanField(),
            )
        ).filter(id__in=followers)
        return followers_profile

    def get_leaders(self, profile):
        leaders = Relationship.objects.filter(follower=profile).values("leader")

        followers_profile = Profile.objects.annotate(
            follows=ExpressionWrapper(
                Q(pk__in=leaders),
                output_field=BooleanField(),
            )
        ).filter(id__in=leaders)
        return followers_profile

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me.user)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default="media/avatars/avatar.webp", upload_to="media/avatars/")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # is_private = models.BooleanField(default=False)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view")

    @property
    def follower_cnt(self):
        return Relationship.objects.filter(leader=self).count()


# (value for database, what we see in admin page)
STATUS_CHOICES = (("send", "send"), ("accepted", "accepted"))


class RelationshipManager(models.Manager):
    def follow_unfollow(self, follower, leader):
        created = False
        try:
            Relationship.objects.get(follower=follower, leader=leader).delete()
        except:
            Relationship.objects.create(
                follower=follower, leader=leader, status="accepted"
            )
            created = True
        return created

    def req_received(self, leader):
        qs = Relationship.objects.filter(leader=leader, status="send")
        return qs


class Relationship(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower"
    )
    leader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="leader")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.follower}-{self.leader}-{self.status}"
