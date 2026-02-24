from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.models import Product, Category
from product_app.forms import ProductForm, CategoryForm
from user_app.models import User
# Create your views here.


def admin_pannel(request):
    products = Product.objects.all().order_by('-id')
    users = User.objects.all()
    category = Category.objects.all()
    total_products = products.count()
    category_form = CategoryForm()
    form = ProductForm()
    return render(request, 'admin_app/admin_panel.html',{
        'products': products,
        'total_products': total_products,
        'category': category,
        'form': form,
        'category_form': category_form,
        'users': users,

    })

