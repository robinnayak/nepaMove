from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,Group,Permission,PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,username, email, password,phone_number, is_driver,**extra_fields):
        if not email:
            raise ValueError(' Email is required ')
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email,
            phone_number=phone_number,
            is_driver = is_driver,
            # profile_image = profile_image,
            
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        print("extra kwargs",extra_fields)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have a superuser=True')
        
        user = self.model(
            username=username,
            email = email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255,unique=True)
    email = models.CharField(max_length=255, unique = True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15,blank=True)
    profile_image = models.ImageField(upload_to='user_profiles/',blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text='The groups this user belongs to A user will get all permissions granted to each at their groups.',
        related_query_name="user_group"
          )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user',
        related_query_name="user_permissions",
    )
    is_driver=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects =CustomUserManager()

    USERNAME_FIELD ='username'
    REQUIRED_FIELDS = ['email','password']

    def __str__(self) -> str:
        return self.username

