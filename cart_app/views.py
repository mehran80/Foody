import json
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from product_app.models import Product
from order_app.models import Order, OrderItem
from user_app.models import ShippingAddress
from .cart import Cart
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def cart_view(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'total_price': cart.get_total_price()
    }
    return render(request, 'cart_app/cart_view.html', context)

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    cart_quantity = len(cart)
    return JsonResponse({'cart_quantity': cart_quantity})

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart_view')


def cart_update_ajax(request):
    cart = Cart(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        action = data.get('action')
        product = Product.objects.get(id=product_id)
        current_quantity = cart.cart.get(product_id, {}).get('quantity', 0)

        if action == 'increment':
            current_quantity += 1
            cart.add(product=product, quantity=current_quantity, update_quantity=True)
        elif action == 'decrement' and current_quantity > 1:
            current_quantity -= 1
            cart.add(product=product, quantity=current_quantity, update_quantity=True)
        elif action == 'remove':
            cart.remove(product)
            current_quantity = 0


        cart.add(product=product, quantity=current_quantity, update_quantity=True)

        cart_length = len(cart)
        total_price = float(cart.cart.get(product_id, {}).get('price', 0)) * current_quantity
        cart_total_price = cart.get_total_price()
        return JsonResponse({
            'success': True,
            'cart_quantity': current_quantity,
            'total_price': total_price,
            'cart_total_price': cart_total_price,
            'cart_length': cart_length
        })
@login_required
def checkout(request):
    cart = Cart(request)
    user = request.user
    saved_address = ShippingAddress.objects.filter(user=user)
    if request.method == 'POST':
        if 'selected_address_id' in request.POST:
            address_id = request.POST.get('selected_address_id')
            chosen_address = ShippingAddress.objects.get(id=address_id, user=user)

            order = create_order_from_address(user, chosen_address, cart)
            request.session['order_id'] = order.id
            return redirect('payment_process')
        
        else:
            form = CheckoutForm(request.POST)
            if form.is_valid():
                new_address = form.save(commit=False)
                new_address.user = user

                if request.POST.get('save_address_for_later'):
                    new_address.save()

                order = create_order_from_address(user, new_address, cart)
                return redirect('payment_process',order_id = order.id)

    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.profile.email if hasattr(request.user, 'profile') else '',
                'phone_number': request.user.profile.phone_number if hasattr(request.user, 'profile') else '',
                'address': request.user.profile.address if hasattr(request.user, 'profile') else ''
            }
        form = CheckoutForm(initial=initial_data)
    context = {
        'cart': cart,
        'total_price': cart.get_total_price(),
        'form': form
    }
    return render(request, 'cart_app/checkout.html', context)


def create_order_from_address(user, address_obj, cart):
    order = Order.objects.create(
        user=user,
        first_name=address_obj.first_name,
        last_name=address_obj.last_name,
        phone=address_obj.phone,
        address=address_obj.address_line_1,
        city=address_obj.city,
        postal_code=address_obj.postal_code,
        total_paid=cart.get_total_price()
        total_price=cart.get_total_price(),
        address=form.cleaned_data['address']
    )

    for item in cart.cart.items():
        product = Product.objects.get(id=item['product_id'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=item['price']
        )

    cart.clear()
    return order