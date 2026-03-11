from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.forms import ProductForm, CategoryForm
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from order_app.models import Order
from product_app.models import Product, Category
from user_app.models import User


User = get_user_model()
# Create your views here.


def admin_pannel(request):
    products = Product.objects.all().order_by('-id')
    all_orders = Order.objects.prefetch_related('items').all().order_by('created_at')
    users = User.objects.all()
    categories = Category.objects.all()
    total_products = products.count()
    category_form = CategoryForm()
    form = ProductForm()
    low_stock_products = Product.objects.filter(stock__lte=5)

    order_counts = Order.objects.aggregate(
        pending_count = Count('id', filter=Q(shipment_status='PENDING')),
        preparing_count = Count('id', filter=Q(shipment_status='PREPARING')),
        shipped_count = Count('id', filter=Q(shipment_status='SHIPPED')),
        deliverd_count = Count('id', filter=Q(shipment_status='DELIVERED')),
        cancelled_count = Count('id', filter=Q(shipment_status='CANCELLED'))
    )

    context = {
        'products': products,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'categories': categories,
        'form': form,
        'category_form': category_form,
        'users': users,
        'all_orders': all_orders,
        'pending_orders': all_orders.filter(shipment_status='PENDING'),
        'preparing_orders': all_orders.filter(shipment_status='PREPARING'),
        'shipped_orders': all_orders.filter(shipment_status='SHIPPED'),
        'deliverd_orders': all_orders.filter(shipment_status='DELIVERED'),
        'cancelled_orders': all_orders.filter(shipment_status='CANCELLED'),
    }

    context.update(order_counts)

    return render(request, 'admin_app/admin_panel.html', context)



def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_app:admin_dashboard')


def user_permissions(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        # Update staff status based on checkbox
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
    return redirect('admin_app:admin_dashboard')