from django.db import models

from django.contrib.auth.models import User

# This is only needed for unittest to check if the cookie has been stolen


class Mail(models.Model):
    content = models.TextField()


class Message(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

class Friends(models.Model):
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend2')
    accepted = models.BooleanField()
	