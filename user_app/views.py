from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm

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
            return redirect('user_app:user_profile')
    else:
        form = UserUpdateForm(instance=user)
        context = {'form':form}
    return render(request,'user_app/user_dashboard.html',context)

