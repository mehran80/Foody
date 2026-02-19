from django.shortcuts import render

# Create your views here.
def admin_pannel(request):
    return render(request, 'admin_app/admin_panel.html')