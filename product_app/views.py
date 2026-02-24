from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_required
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product



# Create your views here.
def products_view(request):
    return render(request, 'product_app/view_products.html')

def product_detail(request):
    return render(request,'product_app/product_detail.html')

@admin_required
def add_category(request):
    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return redirect('admin_panel')
       
    else:
        form = ProductForm()


    return render(request, 'admin_app/add_category.html', {
        'form': form,
        'title': 'Add Category',
    })

@admin_required
def add_product(request):
    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return redirect('admin_panel')
       
    else:
        form = ProductForm()


    return render(request, 'admin_app/add_product.html', {
        'form': form,
        'title': 'Add Product',
    })

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)