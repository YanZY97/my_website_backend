from django.urls import path

from . import views

urlpatterns = [
    path('like/', views.Like.as_view()),
]
