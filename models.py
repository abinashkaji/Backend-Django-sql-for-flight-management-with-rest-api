from django.db import models
from random import randint as rand
from django.utils.text import slugify 
from django.core.validators import MinValueValidator
from random import randint
import random
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User as Users



# # Create your models here.

class Product(models.Model):
    image=models.ImageField(upload_to='images/')
    name=models.CharField(max_length=30)
    price=models.FloatField(default=rand(100,100000),validators=[MinValueValidator(1)])
    stock=models.IntegerField(default=rand(1,50),validators=[MinValueValidator(1)])
    date=models.DateTimeField(default=datetime.now())
    slog=models.SlugField(unique=False, max_length=100,default=slugify(name))
    
    def save(self, *args, **kwargs):
        self.slog = slugify(str(self.name+str(self.date)+str(randint(1,5000))))
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name} '
    
    def get_absolute_url(self):
        return reverse("add", kwargs={"slug": self.slog})  # new


class Username(models.Model):
    name=models.CharField(max_length=40)
    address=models.CharField(max_length=40)
    email=models.EmailField(blank=True)
    password=models.CharField(max_length=30)
    def __str__(self) -> str:
        return f'{self.name} '


class Pro_Qty(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT, related_name="pro_product")
    qty=models.IntegerField(default=rand(1,5),validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f'{self.product.name}: {self.qty}'

class Cart(models.Model):
    user_id=models.ForeignKey(Users,on_delete=models.PROTECT,null=True,related_name="cart_user")
    items=models.ManyToManyField(Pro_Qty, related_name="cart_items")
    def __str__(self) -> str:
        return f'{self.user_id.username} '

class UserPurchase(models.Model):
    user=models.ForeignKey(Users,on_delete=models.PROTECT,null=True,related_name="purchase_user")
    cart=models.ForeignKey(Cart,on_delete=models.PROTECT,related_name="purchase_cart")
    payment=models.BooleanField(default=True)
    Total_amount=models.DecimalField(max_digits=6, decimal_places=2,default=0)
    
    def __str__(self) -> str:
        return f'{self.user.username} {self.Total_amount} '
    # def save(self, *args, **kwargs):
    #     self.Total_amount = 0
    #     if self.payment==True:
    #         self.Total_amount += self.cart__qty                                
    #     super(UserPurchase, self).save(*args, **kwargs)
class Category(models.Model):
    category=models.CharField(max_length=30)

class Product_category(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT,default="Others",related_name='category')
    category=models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.product.name} : {self.category} '

class ProductHistory(models.Model): 
    # for inventory transaction 
    user=models.ForeignKey(Users, on_delete=models.PROTECT,default=1,null=True,related_name="history_user")
    product=models.ForeignKey(Product, on_delete=models.PROTECT,blank=True,related_name="history_product")
    date=models.DateTimeField(default=datetime.now())
    qty=models.IntegerField(validators=[MinValueValidator(1)],default=1)
    
    # def __str__(self) -> str:
    #     return f'{self.user.username}: {self.product.name}: {self.qty} '

