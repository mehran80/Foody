from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('success/<int:order_id>', views.success_order, name='success_order'),
    path('payment/<int:order_id>', views.payment_process, name='payment_failed'),
    path("update_order_status/<int:id>", views.update_order_status, name="update_order_status"),
]
