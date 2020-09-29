from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Group(models.Model):
    name = models.CharField(max_length=128)

class Post(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    post_text = models.TextField(max_length=512)
    post_image = models.ImageField(default='default.jpg', upload_to='post_images')
