from django.urls import path
from . import views

urlpatterns = [
    path('success/<int:order_id>', views.success_order, name='success_order'),
    path('payment/<int:order_id>', views.payment_process, name='payment_failed')
]
