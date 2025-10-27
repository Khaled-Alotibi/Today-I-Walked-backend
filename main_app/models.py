from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="posts/")
    steps = models.IntegerField()
    caption = models.TextField(blank=True, default="Today i Walked.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.useranem} - {self.created_at}"
