from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.products_view, name='products'),
    path('product_detail/', views.product_detail , name='product_detail'),
]
