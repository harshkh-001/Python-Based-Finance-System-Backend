from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    
    class Role(models.TextChoices):
        VIEWER = 'Viewer', 'viewer'
        ANALYST = 'Analyst', 'analyst'
        ADMIN = 'Admin', 'admin'
         
    role = models.CharField(
        max_length=10,
        choices=Role.choices
    )