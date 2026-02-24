from django.urls import path
from .import views

urlpatterns = [
    path('admin/',views.admin_pannel,name='admin_panel'),
]
