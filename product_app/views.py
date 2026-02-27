import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .decorators import admin_required
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm
from .models import Product, Category
from django.views.decorators.http import require_http_methods   


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


# @admin_required
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

# @admin_required
@require_http_methods(["DELETE"])     
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({'status': 'success', 'message': 'Category deleted successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def edit_category(request, category_id):
    
    if request.method == 'POST':
        try:
            category = get_object_or_404(Category, id=category_id)
            
            data = json.loads(request.body)
            new_name = data.get('name')
            if new_name:
                category.name = new_name
                category.save()
                return JsonResponse({'status': 'success', 'message': 'Category updated successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name is required.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
        


# @admin_required
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
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            response = {
                'status': 'success',
                'message': 'Product updated successfully.',
            }

            if product.images:
                response['image_url'] = product.images.url
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@require_http_methods(["DELETE"])
#@admin_required
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'status': 'success', 'message': 'Product deleted successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})