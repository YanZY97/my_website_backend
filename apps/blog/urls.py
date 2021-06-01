from django.urls import path

from . import views

urlpatterns = [
    path('postblog/', views.PostBlog.as_view()),
    path('getblog/', views.GetBlog.as_view()),
    path('getblogcount/', views.GetBlogCount.as_view()),
    path('getarticle/', views.GetArticle.as_view()),
    path('add_comment/', views.AddComment.as_view()),
    path('getcomments/', views.GetComments.as_view()),
    path('likecomments/', views.LikeComments.as_view()),
    path('dislikecomments/', views.DislikeComments.as_view()),
    path('likearticle/', views.LikeArticle.as_view()),
    path('dislikearticle/', views.DislikeArticle.as_view()),
]
