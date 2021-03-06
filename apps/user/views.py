import time
import base64
import os

import cv2
import numpy as np

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from apps.user.models import User
import my_website_backend.settings as settings
from utils.mail_helper import send_captcha_code


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
            raise e


class MyTokenObtainPairView(TokenObtainPairView):
    """登录"""
    serializer_class = MyTokenObtainPairSerializer


class SendCaptcha(APIView):
    """发送验证码"""
    def post(self, request):
        email = request.data.get('email')
        # 校验邮箱格式
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse('邮箱格式不正确', status=403)

        # 校验邮箱是否存在
        try:
            user = User.objects.get(Q(email=email))
        except User.DoesNotExist:
            user = None
        if user:
            return HttpResponse('用户已存在', status=403)

        send_time = request.session.get('send_time')
        if send_time and time.time() < send_time + settings.MAIL_INTERVAL:
            return HttpResponse(f'{settings.MAIL_INTERVAL}秒内不能重复发送', status=403)
        else:
            captcha_code = send_captcha_code(
                settings.MAIL_SMTP_SERVER,
                settings.MAIL_FROM_ADDR,
                settings.MAIL_PASSWORD,
                email
            )

            request.session['mail'] = email
            request.session['captcha'] = captcha_code
            request.session['send_time'] = time.time()
            return HttpResponse('发送成功，请查看邮箱')


class Register(APIView):
    """注册"""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        mobile = request.data.get('mobile')
        birthday = str(request.data.get('birthday')).split('T')[0]
        website = request.data.get('website')
        captcha = request.data.get('captcha')
        avatar_b64 = request.data.get('avatar').split(',')[1]

        avatar_data = base64.b64decode(avatar_b64)
        avatar_array = np.fromstring(avatar_data, np.uint8)
        avatar = cv2.imdecode(avatar_array, cv2.COLOR_RGB2BGR)
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media', 'avatars', username)):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media', 'avatars', username))
        avatar_url = os.path.join('media', 'avatars', username, 'avatar.png')
        cv2.imwrite(os.path.join(settings.BASE_DIR, avatar_url), avatar)
        # cv2.imshow('1', avatar)
        # cv2.waitKey()

        # 校验邮箱格式
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse('邮箱格式不正确', status=403)

        # 校验用户名/邮箱是否已存在
        try:
            user = User.objects.get(Q(username=username) | Q(email=email))
        except User.DoesNotExist:
            user = None
        if user:
            return HttpResponse('用户已存在', status=403)

        email_saved = request.session.get('mail')
        if email_saved and email_saved == email:
            send_time = request.session.get('send_time')
            if send_time and time.time() <= send_time + settings.MAIL_EXPIRE:
                captcha_saved = request.session.get('captcha')
                if captcha_saved == captcha:
                    pass
                else:
                    return HttpResponse('验证码错误', status=403)
            else:
                return HttpResponse('验证码已过期，请重新获取', status=403)
        else:
            return HttpResponse('该邮箱还没获取验证码', status=403)

        user = User.objects.create_user(username, password, email, mobile, birthday, website, avatar_url)
        user.is_active = 1
        user.save()
        return HttpResponse('注册成功')


class UploadAvatar(APIView):
    """上传头像"""
    def post(self, request):
        print(request)
        return HttpResponse('1')
