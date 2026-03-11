from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('admin/',views.admin_pannel,name='admin_dashboard'),
    path('delete-user/<int:id>/',views.delete_user, name='delete_user'),
    path('user_permission/<int:id>',views.user_permissions, name='update_user_permissions'),
]
