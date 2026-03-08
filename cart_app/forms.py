from django.conf import settings
from django import forms
from user_app.models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code']