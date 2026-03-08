import json
from django.urls import reverse
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from product_app.models import Product
from order_app.models import Order, OrderItem
from user_app.models import ShippingAddress
from .cart import Cart
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)

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
    return redirect('cart:cart_view')


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
    saved_addresses = ShippingAddress.objects.filter(user=user)
    form = CheckoutForm(request.POST or None)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        selected_address_id = request.POST.get('selected_address_id')
        if selected_address_id and selected_address_id != 'new':
            try:
                address_id = int(selected_address_id)
                chosen_address = get_object_or_404(ShippingAddress,id=address_id)
                order = create_order_from_address(user, chosen_address, cart ,payment_method)
                request.session['order_id'] = order.id

                if payment_method != 'COD':
                    request.session['stripeToken'] = request.POST.get('stripToken')
                    return redirect('payment_process', order_id=order.id)
                else:
                    return redirect('success_order',order_id=order.id)
                
            except (ValueError, TypeError, Http404):
                print("Invalid Address ID selected")

        elif selected_address_id == 'new' or not selected_address_id:

            if form.is_valid():
                new_address = form.save(commit=False)
                new_address.user = user

                if request.POST.get('saved_address_for_later'):
                    new_address.save()

                order = create_order_from_address(user, new_address, cart, payment_method)

                if payment_method != 'COD':
                    request.session['stripeToken']= request.POST.get('stripeToken')
                    return redirect('payment_process', order_id = order.id)
                
                else:
                    return redirect('success_order', order_id = order.id)
                
            else:
                message = 'Please Fill the form Correctly'

        context={
            'form': form,
            'cart': cart,
            'saved_address': saved_addresses,
            'total_price': cart.get_total_price(),
            'message': message if 'message' in locals() else "Form submission failed.",
        }

        return render(request, 'cart_app/checkout.html', context)
    
    else:

        initial_data = {}
        if request.user.is_authenticated:

            profile = getattr(request.user, 'profile', None)
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': profile.email if profile else request.user.email,
                'phone_number': profile.phone_number if profile else request.user.phone_number,
                'address': profile.address if profile else request.user.address
            }

        form = CheckoutForm(initial=initial_data)
        
    context = {
        'cart': cart,
        'total_price': cart.get_total_price(),
        'form': form,
        'saved_address': saved_addresses
    }
    
    return render(request, 'cart_app/checkout.html', context)


def create_order_from_address(user, address_obj, cart, payment_method):
    order = Order.objects.create(
        user=user,
        first_name=address_obj.first_name,
        last_name=address_obj.last_name,
        phone=address_obj.phone,
        address=address_obj.address,
        city=address_obj.city,
        postal_code=address_obj.postal_code,
        total_paid=cart.get_total_price(),
        total_price=cart.get_total_price(),
        payment_method = payment_method
    )

    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=item['price']
        )

    cart.clear()
    return order