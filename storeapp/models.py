from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=250, null=True)

    def __str__(self):
       return self.user.email

class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    product_type =models.ForeignKey(ProductType, on_delete=models.CASCADE, max_length=50,null=True, blank=True)
    price = models.FloatField()
    product_brifing = models.TextField(max_length=50,null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url =self.image.url
        except:
            url =""
        return url



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ["-transaction_id"]



    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.product)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=200, null=False)
    status = models.BooleanField(default=False, null=True, blank=False)
    address = models.CharField(max_length=250,  null=True)
    pickup_location = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    total = models.CharField(max_length=250, null=True)




    def __str__(self):
        return self.city

    @property
    def get_orderitem(self):
        orderitems = self.orderitem_set.all()
        return orderitems





