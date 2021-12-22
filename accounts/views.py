from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request=request, template_name='accounts/dashboard.html')

def products(request):
    return render(request=request, template_name='accounts/products.html')

def customer(request):
    return render(request=request, template_name='accounts/customer.html')
