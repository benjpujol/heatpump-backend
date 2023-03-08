
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Settings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos', blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    company_address = models.CharField(max_length=100, blank=True)
    company_city = models.CharField(max_length=100, blank=True)
    company_state = models.CharField(max_length=100, blank=True)
    company_zip = models.CharField(max_length=100, blank=True)
    company_phone = models.CharField(max_length=100, blank=True)
    company_email = models.CharField(max_length=100, blank=True)
    company_website = models.CharField(max_length=100, blank=True)
    company_identifier = models.CharField(max_length=100, blank=True)
