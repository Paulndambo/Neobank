from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models import AbstractBaseModel
# Create your models here.
class User(AbstractUser, AbstractBaseModel):
  gender = models.CharField(max_length=255, blank=True, null=True)
  birthday = models.DateField(blank=True, null=True)
  phone = models.CharField(max_length=255, blank=True, null=True)
  address = models.CharField(max_length=255, blank=True, null=True)
  avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
  role = models.CharField(max_length=255, blank=True, null=True)