from django.shortcuts import render
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect,get_object_or_404
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .generate_bill import GenerateBill
from .utils import shopowner_required


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='ShopOwners').exists():
            return redirect('shopowner_dashboard')  
        else:
            return redirect('customer_dashboard') 
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()

            if form.cleaned_data['is_shop_owner']: 
                shop_owner_group = Group.objects.get(name='ShopOwners')
                user.groups.add(shop_owner_group) 
            else:
                customer_group = Group.objects.get(name='Customers')
                user.groups.add(customer_group)  

            login(request, user) 

            if user.groups.filter(name='ShopOwners').exists():
                return redirect('shopowner_dashboard')  
            else:
                return redirect('customer_dashboard') 
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def dologin(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='ShopOwners').exists():
            return redirect('shopowner_dashboard')  
        else:
            return redirect('customer_dashboard') 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='ShopOwners').exists():
                return redirect('shopowner_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    form = SignUpForm(request.POST)
    return render(request, 'signup.html', {'form': form})

@login_required
def customer_dashboard(request):
    items = Item.objects.all()
    return render(request, 'customer_dashboard.html', {'items': items})

@shopowner_required
def shopowner_dashboard(request):
    items = Item.objects.all()
    return render(request, 'shopowner_dashboard.html', {'items': items})

@shopowner_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopowner_dashboard')
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form, 'type': 'Create'})

@shopowner_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('shopowner_dashboard')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form, 'type': 'Edit', 'item': item})

@shopowner_required
def create_discount(request):
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shopowner_dashboard')
    else:
        form = DiscountForm()
    return render(request, 'discount_form.html', {'form': form, 'type': 'Create'})

@shopowner_required
def edit_discount(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            return redirect('shopowner_dashboard')
    else:
        form = DiscountForm(instance=discount)
    return render(request, 'discount_form.html', {'form': form, 'type': 'Edit', 'discount': discount})

def user_logout(request):
    logout(request)  
    return redirect('login') 


def generate_bill(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cart_items = data.get('items', [])

            print("Received Cart Items:",cart_items)
            
            bill = GenerateBill(cart_items)
            total, item_wise_prices = bill.total_price()
            print("total price is :" , total)
            print("item_wise_prices price is :" , item_wise_prices)

            return JsonResponse({
                'status': 'success',
                'message': 'Bill generated successfully.',
                'items': item_wise_prices,
                'total': total 
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)