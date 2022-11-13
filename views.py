from django.shortcuts import render
from .models import Product,Cart,ProductHistory,UserPurchase,Product_category,Category
from django.contrib.auth.models import User as Users
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
from django.contrib.auth import logout,authenticate,login
# Create your views here.


# def update(request): update column
#     products=Product.objects.all()
#     for product in products:
#         product.date=datetime.now()
#         product.save()
#     return render(request,'index.html')
class Form(forms.Form):
    color=forms.ChoiceField(choices=[('bk','black'),('wt','white'),('rd','red'), ('or','other')],required=False,label="Select color")
    quantity=forms.IntegerField(min_value=1)
    price=forms.DecimalField()

class UserForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput(), max_length=30 )

def index(request):
    categories=Product_category.objects.all().values_list('category').distinct()
    
    categories=[i[0] for i in categories]
    products=sorted(Product.objects.all(),  key=lambda x: random.random()) #order_by('?')
    #print(request.GET["category"])
    try: 
        cart=len(eval(request.COOKIES["cart"]))
    except:
        cart=0
    print(cart)
    return render(request,'index.html',{"product":products,"items":cart,"category":list(categories)})

def details(request,id):
    # individual product with details
    product=Product.objects.get(id=id)
    return render(request,'details.html',{"product":product,"form":Form()})

def add(request,id):
    #Adding in cart in Cookies 
    response = HttpResponseRedirect(reverse('shop:cart')) 
    try:
        content= eval(request.COOKIES["cart"])
    except:
        content={}
    
    content[id]=[request.POST['quantity'],request.POST['price']]
    response.set_cookie('cart',content) 
    return response
def cart_item(request): 
    cart=eval(request.COOKIES["cart"]) # data extraction from cookies
    product_id=[int(id) for id, item in cart.items()] 
    product_price=[float(item[1]) for id, item in cart.items()]
    product_quantity=[int(item[0]) for id, item in cart.items()]
    

    product_at_cart=Product.objects.filter(id__in=product_id)
    #price=list(product_at_cart.price)
    mylist=zip(product_at_cart,product_quantity)
    print(product_price,product_id,product_quantity)
    return render(request,'cart.html',{"cart":mylist})
    #"t":list(cart.values()),"cart":product_at_cart

def purchase(request):
    cart=eval(request.COOKIES["cart"])

    product_at_cart=Product.objects.filter(id__in=list(cart.keys()))
    for i in product_at_cart:
        print(i.stock, cart[i.id],'\n')
        if int(cart[i.id][0])>i.stock:
            return HttpResponseRedirect(reverse('details',args=(i.id,))) #change cart item values    

    if request.user.is_authenticated:
        user=Users.objects.get(username=request.user)
        for i in product_at_cart:
            i.stock=i.stock-int(cart[i.id][0])
            i.save()
            p=ProductHistory.objects.create(user=user,product=i,qty=cart[i.id][0])
            p.save()
            # print(p.date,p.qty)

        try:
                response = HttpResponseRedirect(reverse('cart'))
                response.set_cookie('cart',{})
                return response 
        except:
                print("unsuccessful")
        return render(request,'index.html',{'context':"success"})
    else:
        return HttpResponseRedirect(reverse('user:login1'))

def cancel(request):
    if request.user.is_authenticated:
        try:
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('cart',{})
            return response
        except:
            return render(request,'index.html',{'context':"Unsuccess"})
    return HttpResponseRedirect(reverse('user:login1'))

def history(request):
    if request.user.is_authenticated:
        user=Users.objects.get(username=request.user)
        p=ProductHistory.objects.filter(user_id=user).all()

        return render(request,'history.html',{'p':p})

def logout1(request,id):
    if request.is_authenticated:
        logout(request)
        form=UserForm()    
    else:
        form=UserForm()
        if request.method=="POST":
            form=UserForm(request.POST)
            if form.is_valid():
                user=form["username"]
                password=form["password"]                
                user=authenticate(request,username=user,password=password)
                if user:
                    login(request,user)
                return HttpResponseRedirect(reverse('index'))
            
    return render(request,'login.html',{"form":form})
