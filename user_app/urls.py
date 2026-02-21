from django.urls import path
from . import views

app_name = 'user_app'  

urlpatterns = [
   path('user_dashboard/',views.user_dashboard, name='user_dashboard'),
   path('login/',views.login_view, name='login'),
   path('logout/',views.logout_view, name='logout'),
   path('signup/', views.signup_view, name='signup'),
]
