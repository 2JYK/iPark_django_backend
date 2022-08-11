from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("사용자 계정을 만들어주세요")
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Region(models.Model):
    region_name = models.CharField("지역", max_length=50)

    def __str__(self):
        return self.region_name


class User(AbstractBaseUser):
    bookmarks = models.ManyToManyField("park.Park", verbose_name="즐겨찾기", related_name="users", through="park.BookMark")
    username = models.CharField("사용자 계정", max_length=30, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField("사용자 이름", max_length=20)
    email = models.EmailField("이메일", max_length=100, unique=True)
    phone = models.CharField("핸드폰 번호", max_length=20)
    region = models.ForeignKey(Region, verbose_name="지역", on_delete=models.SET_NULL, null=True)
    join_date = models.DateTimeField("가입일자", auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label): 
        return True

    @property
    def is_staff(self):
        return self.is_admin