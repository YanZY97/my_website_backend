from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, mobile, birthday, website, avatar, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        if not mobile:
            mobile = ''
        if not birthday:
            birthday = ''
        if not website:
            website = ''
        if not avatar:
            avatar = ''
        else:
            avatar = '/api/' + avatar
        user = self.model(username=username,
                          email=email,
                          mobile=mobile,
                          birthday=birthday,
                          website=website,
                          avatar=avatar,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, mobile, birthday, website, avatar, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, mobile, birthday, website, avatar, **kwargs)

    def create_superuser(self, username, password, email, mobile=None, birthday=None, website=None, avatar=None, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, mobile, birthday, website, avatar, **kwargs)


class User(AbstractUser):
    mobile = models.CharField(max_length=15)
    birthday = models.CharField(max_length=50)
    website = models.CharField(max_length=200)
    avatar = models.CharField(max_length=100)
    website_accessable = models.BooleanField(default=False)
    signature = models.CharField(max_length=500)
    website_img = models.CharField(max_length=1000)

    objects = UserManager()

    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = verbose_name
