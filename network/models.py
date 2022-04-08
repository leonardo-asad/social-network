from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")

    def __str__(self):
        return f"Username: {self.username}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField()
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Author: {self.author.username}. Likes: {self.likes}"
