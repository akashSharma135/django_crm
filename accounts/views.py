from django.shortcuts import render
from .models import *

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delieverd = orders.filter(status='Delievered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delievered': delieverd,
        'pending': pending
    }

    return render(request=request, template_name='accounts/dashboard.html', context=context)

def products(request):
    products = Product.objects.all()
    return render(request=request, template_name='accounts/products.html', context={'products': products})

def customer(request, pk):
    customer = Customer.objects.get(pk=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    return render(request=request, template_name='accounts/customer.html', context={'customer': customer, 'orders': orders, 'order_count': order_count})
