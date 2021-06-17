from django.db import models
from apps.user.models import User


class Messages(models.Model):
    user = models.IntegerField()
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Messages'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'messages'


class MessagePictures(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    url = models.TextField()

    class Meta:
        db_table = 'message_pictures'
        verbose_name = 'MessagePictures'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'message_pictures'
