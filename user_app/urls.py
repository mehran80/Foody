from django.urls import path
from . import views

app_name = 'user_app'  

urlpatterns = [
   path('profile/',views.user_dashboard, name='user_profile'),
   path('login/',views.login_view, name='login'),
   path('logout/',views.logout_view, name='logout'),
   path('signup/', views.signup_view, name='signup'),
]
