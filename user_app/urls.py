from django.urls import path
from . import views

app_name = 'user_app'  

urlpatterns = [
   path('user_dashboard/',views.user_dashboard, name='user_dashboard'),
   path('login/',views.login_view, name='login'),
   path('logout/',views.logout_view, name='logout'),
   path('signup/', views.signup_view, name='signup'),
    path('delete-user/<int:id>/',views.delete_user, name='delete_user'),
    path('user_permission/<int:id>',views.user_permissions, name='update_user_permissions'),
]
