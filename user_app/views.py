from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from django.urls import reverse
from order_app.models import Order
from user_app.models import User


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                username = user.username
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        else:
            messages.error(request,"invalid email or password")
    else:
        form = AuthenticationForm()
    return render(request,'user_app/login.html', {'form':form})



def logout_view(request):
    logout(request)
    messages.info(request, "You have been Logout")
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.split('@')[0]
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_app/signup.html', {'form':form})


@login_required
def user_dashboard(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!') 
            url = reverse('user_app:user_dashboard') + '?tab=profile'
            return redirect(url)
    else:
        form = UserUpdateForm(instance=user)

    customer_orders = Order.objects.filter(user=request.user)
    active_tab = request.GET.get('tab', 'wishlist')
    context = {
        'form':form,
        'customer_orders': customer_orders,
        'active_tab': active_tab
        }
    return render(request,'user_app/user_dashboard.html',context)


def user_permissions(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        # Update staff status based on checkbox
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
    return redirect('admin_app:admin_dashboard')


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_app:admin_dashboard')

