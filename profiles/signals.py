from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Comment, Like, Notification

from .models import Profile


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Like)
def like_save_create_notify(sender, instance, created, **kwargs):
    if instance.user == instance.post.author:
        return
    if instance.value == "Like":
        Notification.objects.create(
            user=instance.post.author,
            actor=instance.user,
            post=instance.post,
            action="like",
        )
    else:
        Notification.objects.get(
            user=instance.post.author,
            actor=instance.user,
            post=instance.post,
        ).delete()


@receiver(post_save, sender=Comment)
def comment_save_create_notify(sender, instance, created, **kwargs):
    if instance.author == instance.post.author:
        return
    Notification.objects.create(
        user=instance.post.author,
        actor=instance.author,
        post=instance.post,
        action="comment",
    )
