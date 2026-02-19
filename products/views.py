from django.shortcuts import render

# Create your views here.
def products_view(request):
    return render(request, 'products/view_products.html')

def product_detail(request):
    return render(request,'products/product_detail.html')