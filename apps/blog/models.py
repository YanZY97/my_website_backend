from django.db import models


# Create your models here.
class Blogs(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    cls = models.CharField(max_length=50)
    tags = models.TextField()
    content = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blogs'
        verbose_name = 'Blogs'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'blogs'


class Comments(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey("Blogs", on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'
        verbose_name = 'Comments'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'comments'
