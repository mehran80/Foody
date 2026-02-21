from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'core/index.html')



def contact_us(request):
    return render(request, 'core/contact.html')