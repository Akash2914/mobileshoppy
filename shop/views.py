import json

from django.shortcuts import render,redirect
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.shortcuts import HttpResponse
# Create your views here.
def home(request):
    products = Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{'products':products})

def payment_page(request):
    return render(request,'shop/payment.html')


def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect('/fav_view_page')


def fav_view_page(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, 'shop/fav.html', {'fav': fav})
    else:
        return redirect('/')

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'product added to favorite'}, status=200)
        else:
            return JsonResponse({'status':'Login to fav'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)




def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'cart':cart})
    else:
        return redirect('/')


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'product added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'product stock not available'},status=200)
        else:
            return JsonResponse({'status':'Login to addcart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,pasword=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'logged in successfully')
                return redirect('/')
            else:
                messages.error(request,'invalid username or password')
                return redirect('/login')
        return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'logged-out successfully')
        return redirect('/')



def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can LogIn Now...!")
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})


def collections(request):
    category=Catagory.objects.filter(status=0)
    return render(request, 'shop/collections.html',{"category":category})
def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'shop/products/index.html',{'products':products,'category__name':name})
    else:
        messages.warning(request,'no such catagory found')
        return redirect('collections')
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,'no such product found')
            return redirect('collections')
    else:
        messages.error(request,"no such catagory found")
        return redirect('collections')
