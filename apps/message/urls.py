from django.urls import path

from . import views

urlpatterns = [
    path('postmessage/', views.PostMessage.as_view()),
    path('getmessage/', views.GetMessage.as_view()),
    path('getmessagecount/', views.GetMessageCount.as_view()),
]
