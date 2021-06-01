from django.contrib import admin

from . import models

admin.site.register(models.Blogs)
admin.site.register(models.Comments)


