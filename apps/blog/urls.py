from django.urls import path

from . import views

urlpatterns = [
    path('postblog/', views.PostBlog.as_view()),
    path('getblog/', views.GetBlog.as_view())
]
