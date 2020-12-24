from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.user.models import User


class CustomBackend(ModelBackend):
    """自定义登录验证"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义登录信息"""
    def validate(self, attrs):
        try:
            data = super(MyTokenObtainPairSerializer, self).validate(attrs)
            refresh = self.get_token(self.user)
            data['message'] = '登录成功'
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['username'] = self.user.username
            data['permission'] = self.user.is_superuser

            return data
        except Exception as e:
            print(e)
            return {
                'message': '用户名或密码错误'
            }


class MyTokenObtainPairView(TokenObtainPairView):
    """登录"""
    serializer_class = MyTokenObtainPairSerializer


class Register(APIView):
    """注册"""
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        birthday = request.POST.get('birthday')
        website = request.POST.get('website')

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=mobile) | Q(email=email))
        except User.DoesNotExist:
            user = None

        if user:
            return HttpResponse('用户已存在', status=403)

        user = User.objects.create_user(username, password, email, mobile, birthday, website)
        user.is_active = 0
        user.save()
        return HttpResponse('注册成功')
