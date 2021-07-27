from django.urls import path

from . import views

urlpatterns = [
    path('like/', views.Like.as_view()),
    path('visit/', views.Visit.as_view()),
    path('postannouncement/', views.PostAnnouncement.as_view()),
    path('getannouncement/', views.GetAnnouncement.as_view()),
    path('getannouncementcount/', views.GetAnnouncementCount.as_view()),
    path('uploadaction/', views.UploadAction.as_view()),
    path('echochat/', views.EchoChat.as_view()),
]
