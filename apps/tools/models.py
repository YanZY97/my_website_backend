from django.db import models


# Create your models here.
from apps.user.models import User


class Likes(models.Model):
    user = models.TextField()

    class Meta:
        db_table = 'likes'
        verbose_name = 'Likes'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'likes'


class Visits(models.Model):

    class Meta:
        db_table = 'visits'
        verbose_name = 'Visits'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'visits'


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'announcement'
        verbose_name = 'Announcement'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Announcement'

