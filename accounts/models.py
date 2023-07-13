from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Member(AbstractUser):
    email = None
    first_name = None
    last_name = None