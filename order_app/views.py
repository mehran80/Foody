from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
import stripe
from order_app.models import Order
from cart_app.cart import Cart


# Create your views here.
stripe.api_key = settings.STRIPE_PUBLIC_KEY

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    stripe_token = request.session.get['stripeToken']

    if not stripe_token:
        return redirect('cart:checkout')
    try:
    
        charge = stripe.Charge.create(

            amount= int(order.total_price * 100),
            currency= 'usd',
            description= f'Foody order #{order.id}',
            source=stripe_token
        )
        order.status = 'Paid'
        order.save()

        del request.session['stripe_token']

        return redirect('order_app:order_success', order_id = order.id)
    except stripe.error.CardError as e:
        context = {'error': e.user_message, 'order': order}
        return render(request , 'order_app:payment_failed.html', context)
    

def success_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    cart = Cart(request)
    cart.clear()

    context = {'order':order}

    return render(request, 'order_app/order_success.html', context)