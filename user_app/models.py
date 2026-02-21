from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, blank=True, null=True, unique=True)
    phone_number =  PhoneNumberField(blank=True, null=True,)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username
