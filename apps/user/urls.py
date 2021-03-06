from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view()),      # 登录
    path('send_captcha/', views.SendCaptcha.as_view()),         # 获取验证码
    path('register/', views.Register.as_view()),                # 注册
    path('refresh/', TokenRefreshView.as_view()),               # 刷新用户token
    path('upload_avatar/', views.UploadAvatar.as_view()),       # 上传头像
]
