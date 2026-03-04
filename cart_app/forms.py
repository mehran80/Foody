from django.conf import settings
from django import forms
from order_app.models import Order


class CheckoutForm(forms.Form):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code']