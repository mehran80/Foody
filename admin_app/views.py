from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
# Create your views here.


def admin_pannel(request):
    products = Product.objects.all().order_by('-id')
    category = Category.objects.all()
    total_products = products.count()
    return render(request, 'admin_app/admin_panel.html',{
        'products': products,
        'total_products': total_products,
        'category': category,

    })

