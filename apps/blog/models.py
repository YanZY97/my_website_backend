from django.db import models


# Create your models here.
class Blogs(models.Model):
    author = models.TextField()
    title = models.TextField()
    cls = models.TextField()
    tags = models.TextField()
    content = models.TextField()
    abstract = models.TextField()
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
    author = models.TextField()
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
