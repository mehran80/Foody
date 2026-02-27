from django.urls import path
from .import views
app_name = 'product_app'

urlpatterns = [
    path('products/',views.products_view, name='products'),
    path('product_detail/<int:product_id>/', views.product_detail , name='product_detail'),
    path('add_product/', views.add_product, name='add_products'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    
    path('add_category/', views.add_category, name='add_categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
]