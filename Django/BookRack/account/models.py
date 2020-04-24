# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)
# # Create your models here.
# class User(AbstractBaseUser,PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=25, unique=True)
#     first_name = models.CharField(max_length=40)
#     last_name = models.CharField(max_length=140)
#     date_joined = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     interest=models.CharField(max_length=150)
    
#     USERNAME_FIELD = "username" 