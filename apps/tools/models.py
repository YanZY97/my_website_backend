from django.db import models


# Create your models here.
class Likes(models.Model):
    count = models.IntegerField(default=0, verbose_name='Likes')

    class Meta:
        db_table = 'likes'
        verbose_name = 'Likes'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'likes:%d' % self.count
