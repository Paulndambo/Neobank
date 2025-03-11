from django.db import models
from apps.core.models import AbstractBaseModel
# Create your models here.
class ServiceProvider(AbstractBaseModel):
  user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="service_provider")
  name = models.CharField(max_length=255)
  description = models.TextField()