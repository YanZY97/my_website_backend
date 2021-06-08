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
