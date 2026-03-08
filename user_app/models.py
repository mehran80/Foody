from django.db import models
from django.conf import settings
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
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_label = models.CharField(max_length=50, default='Home')

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    phone =  PhoneNumberField(blank=True, null=False)
    address = models.TextField(blank=True, null=False,default="123 Street, New York, USA2")
    city = models.CharField(max_length=100, null=False)
    postal_code = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False,default="default_email@example.com")

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return F"{self.address_label} - {self.address}"



