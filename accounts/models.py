from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core import validators
import os
from uuid import uuid4
# from ..app.models import Sport

#moved from app
class Sport(models.Model):
    # user = models.ManyToManyField(User, related_name='favorite_sports')
    name = models.CharField(max_length=100, null=False, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

def path_and_rename(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'book#{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField('username', unique=True, max_length=50, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    # first_name = models.CharField('first_name', max_length=50, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    # last_name = models.CharField('last_name', max_length=50, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    photo = models.ImageField(upload_to=path_and_rename, blank=True)
    birthday = models.DateField('birthday', null=True)
    benchpress = models.IntegerField('benchpress', null=True)
    sport = models.ManyToManyField(Sport, related_name='users')
    goal = models.TextField('goal', max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username