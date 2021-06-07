from django.db import models


# Create your models here.
class Messages(models.Model):
    author = models.TextField()
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Messages'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'messages'
