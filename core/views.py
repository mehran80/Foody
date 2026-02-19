from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'core/index.html')

def login_view(request):
    return render(request,'core/login.html')

def signup_view(request):
    return render(request, 'core/signup.html')

def contact_us(request):
    return render(request, 'core/contact.html')