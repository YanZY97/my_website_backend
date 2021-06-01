from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view()),              # 登录
    path('adminlogin/', views.MyAdminTokenObtainPairView.as_view()),    # 管理员登录
    path('send_captcha/', views.SendCaptcha.as_view()),                 # 获取验证码
    path('register/', views.Register.as_view()),                        # 注册
    path('refresh/', TokenRefreshView.as_view()),                       # 刷新用户token
    path('uploadavatar/', views.UploadAvatar.as_view()),                # 上传头像
    path('permission_check/', views.PermissionCheck.as_view()),         # 验证管理员身份
    path('evalcaptcha/', views.EvalCaptcha.as_view()),                  # 验证验证码
    path('resetpassword/', views.ResetPassword.as_view()),              # 重置密码
    path('getuserdetail/', views.GetUserDetail.as_view()),              # 获取用户详细信息
    path('resetemail/', views.ResetEmail.as_view()),                    # 重置邮箱
    path('resetsignature/', views.ResetSignature.as_view()),            # 重置个人简介
    path('resetmobile/', views.ResetMobile.as_view()),                  # 重置手机
    path('resetbirthday/', views.ResetBirthday.as_view()),              # 重置生日
    path('resetwebsite/', views.ResetWebsite.as_view()),                # 重置个人主页
    path('getwebaccess/', views.GetWebAccess.as_view()),                # 获取认证网站的用户列表
]
