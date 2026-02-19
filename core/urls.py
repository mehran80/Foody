from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('contact/', views.contact_us, name='contact_us'),
    path('login/',views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
