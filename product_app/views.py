from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .decorators import admin_required
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm
from .models import Product

def products_view(request):
        products = Product.objects.all()
        return render(request, 'product_app/products.html', {
            'products': products,
            'title': 'Products',
        })
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_app/product_detail.html', {
        'product': product,
        'title': product.name,
    })  



def add_category(request):
    
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
        else:
            messages.error(request, 'Failed to add category. Please check your inputs.')  

        
        url = reverse('admin_app:admin_dashboard') + '?tab=category'
        return redirect(url)  
       
    
    
    form = CategoryForm()
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
           url = reverse('admin_app:admin_dashboard') + '?tab=tab-products'
           return redirect(url)
       
    else:
        form = ProductForm()


    return render(request, 'admin_app/add_product.html', {
        'form': form,
        'title': 'Add Product',
    })

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)