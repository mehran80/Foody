from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('admin/',views.admin_pannel,name='admin_dashboard'),
]
