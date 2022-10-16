from django.db import models

from django.contrib.auth.models import User

# This is only needed for unittest to check if the cookie has been stolen


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.FileField(upload_to=user_directory_path)


class Mail(models.Model):
    content = models.TextField()


class Message(models.Model):
    source = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='target')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')


class Friends(models.Model):
    friend1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friend2')
    accepted = models.BooleanField()
