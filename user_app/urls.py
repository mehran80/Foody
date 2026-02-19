from django.urls import path
from . import views

urlpatterns = [
   path('profile/',views.user_dashboard, name='user_profile')
]
