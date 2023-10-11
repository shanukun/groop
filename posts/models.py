from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import BooleanField, ExpressionWrapper, Q

from profiles.models import Profile, Relationship


class PostManager(models.Manager):
    def get_my_posts(self, profile):
        following = Relationship.objects.filter(follower=profile).values("leader")

        likes = Like.objects.filter(user=profile).filter(value="Like").values("post")
        posts = Post.objects.filter(
            Q(author__in=following) | Q(author=profile)
        ).annotate(
            likes=ExpressionWrapper(
                Q(pk__in=likes),
                output_field=BooleanField(),
            )
        )
        return posts

    def get_author_posts(self, profile):
        likes = Like.objects.filter(user=profile).filter(value="Like").values("post")

        post = Post.objects.annotate(
            likes=ExpressionWrapper(
                Q(pk__in=likes),
                output_field=BooleanField(),
            )
        ).filter(author=profile)
        return post

    def get_post(self, post_id, user):
        likes = (
            Like.objects.filter(user__user=user)
            .filter(value="Like")
            .filter(post__id=post_id)
            .values("post")
        )

        post = Post.objects.annotate(
            likes=ExpressionWrapper(
                Q(pk__in=likes),
                output_field=BooleanField(),
            )
        ).get(pk=post_id)
        return post


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(
        upload_to="media/",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
        blank=True,
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    objects = PostManager()

    def __str__(self):
        return str(self.content[:20])

    @property
    def num_likes(self):
        # return Like.objects.filter(post=self).filter(value="Like").count()
        return self.like_set.filter(value__exact="Like").count()

    @property
    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ("-created",)


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ("Like", "Like"),
    ("Unlike", "Unlike"),
)


class LikeManager(models.Manager):
    def like_unlike_post(self, post_id, profile):
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        addition = 1
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
                addition = -1
            else:
                like.value = "Like"
        else:
            like.value = "Like"
        like.save()
        return addition


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = LikeManager()

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


NOTIFICATION_TYPE = (("like", "like"), ("comment", "comment"))


class Notification(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="target_user"
    )
    actor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    action = models.CharField(max_length=7, choices=NOTIFICATION_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.actor} - {self.action} - {self.post}"
