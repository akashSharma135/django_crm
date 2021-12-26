from django.shortcuts import render, redirect

from accounts.decorators import admin_only, allowed_user, unauthenticated_user
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filters import OrderFilter
from django.contrib.auth.models import Group

@unauthenticated_user
def register_page(request):
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user = user
            )
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    return render(request=request, template_name="accounts/register.html", context={'form': form})

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.info(request, message='Username or password is incorrect!')

    return render(request=request, template_name="accounts/login.html", context={})

def logout_user(request):
    logout(request=request)
    return redirect(to='login')

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delieverd = orders.filter(status='Delievered').count()
    pending = orders.filter(status='Pending').count()
    return render(request=request, template_name='accounts/user.html', context={'orders': orders, 'total_orders': total_orders, 'delievered': delieverd, 'pending': pending})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request=request, template_name='accounts/products.html', context={'products': products})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(pk=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    return render(request=request, template_name='accounts/customer.html', context={'customer': customer, 'orders': orders, 'order_count': order_count, 'myfilter': myfilter})

@login_required(login_url='login')
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(parent_model=Customer, model=Order, fields=('product', 'status'), extra=5)
    
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request=request, template_name='accounts/order_form.html', context={'formset': formset})

@login_required(login_url='login')
def update_order(request, pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request=request, template_name='accounts/order_form.html', context={'form': form})

@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request=request, template_name='accounts/delete.html', context={'item': order})

