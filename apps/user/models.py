from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, mobile, birthday, website, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        user = self.model(username=username, email=email, mobile=mobile, birthday=birthday, website=website, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, mobile, birthday, website, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, mobile, birthday, website, **kwargs)

    def create_superuser(self, username, password, email, mobile, birthday, website, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, mobile, birthday, website, **kwargs)


class User(AbstractUser):
    mobile = models.CharField(max_length=15)
    birthday = models.CharField(max_length=50)
    website = models.CharField(max_length=200)

    objects = UserManager()

    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = verbose_name
