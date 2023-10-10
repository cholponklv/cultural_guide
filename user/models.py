from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


class MyCustomUserManger(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be exist')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff', True) is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    ADMIN = 'admin'
    COMPANY = 'company'

    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (COMPANY, 'company')
    ]
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES,default='user')
    photo = models.ImageField(upload_to='profile', default='profile/ava.png')
    phone_number = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    is_email_confirmed = models.BooleanField(default=False)
    email_confirmation_code = models.CharField(
        max_length=6, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    doc = models.CharField(max_length=100,blank=True,null=True)
    chat_id = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=16, null=True, blank=True)
    objects = MyCustomUserManger()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_company(self):
        return self.role == self.COMPANY


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    events = models.ForeignKey('events.Events', on_delete=models.CASCADE,default=None,blank=True,null=True)

        




