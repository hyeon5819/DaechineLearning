# step 1 : 유저모델 구현하기 (유저에게 필요한 정보를 가져오기)

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email = self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # User Email (Required)
    email = models.EmailField("email", max_length=256, unique=True)
    # User Username
    username = models.CharField("username", max_length=20, blank=True, null=True)
    # User Password (Required)
    password = models.CharField("Password", max_length=256)
    
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    
    objects = UserManager()  # Necessary when creating custom user
    
    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label): 
        return True
    
    @property
    def is_staff(self): 
        return self.is_admin