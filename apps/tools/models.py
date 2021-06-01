from django.db import models


# Create your models here.
class Likes(models.Model):
    user = models.CharField(max_length=100)

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
    author = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'announcement'
        verbose_name = 'Announcement'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Announcement'

