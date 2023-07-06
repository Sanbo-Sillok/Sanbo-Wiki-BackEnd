from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Member(AbstractUser):
    name = models.CharField(verbose_name="이름", null=True, max_length=5)