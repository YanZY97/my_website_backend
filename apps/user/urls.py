from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [

    path('login/', views.MyTokenObtainPairView.as_view()),                  # 登录
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # 刷新用户token
]
