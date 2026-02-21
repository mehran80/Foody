from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from django.urls import reverse
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

    customer_orders = [ # Placeholder data
        {'id': 101, 'date': '2023-11-10', 'total': 45.50, 'status': 'Pending'},
        {'id': 100, 'date': '2023-11-05', 'total': 78.00, 'status': 'Completed'},
        {'id': 99, 'date': '2023-10-30', 'total': 22.10, 'status': 'Cancelled'},
    ]
    active_tab = request.GET.get('tab', 'wishlist')
    context = {
        'form':form,
        'customer_orders': customer_orders,
        'active_tab': active_tab
        }
    return render(request,'user_app/user_dashboard.html',context)

