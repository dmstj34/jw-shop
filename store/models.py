from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Customer(models.Model):
  user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200)
  def __str__(self):
    return self.name

class Product(models.Model):
  name = models.CharField(max_length=200)
  decription = models.CharField(max_length=200, null=True,default='')
  price = models.IntegerField(default=0)
  digital = models.BooleanField(default=False, null=True, blank=True)
  image = models.ImageField(null=True, blank=True)
  
  def __str__(self):
    return self.name
  @property
  def imageURL(self):
    try:
      url = self.image.url
    except:#사진없으면
      url = '/images/이미지없음.png'
    return url

  
class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True )
  dated_ordered =models.DateTimeField(auto_now_add=True) #에러수정
  complete = models.BooleanField(default=False, null=True, blank=True)
  transation_id = models.CharField(max_length=200, null=True)
  def __str__(self):
    return str(self.id)
  @property
  def shipping(self):
    shipping = False
    orderitems = self.orderitem_set.all()
    for i in orderitems:
      if i.product.digital == False:
        shipping = True
    return shipping
  @property
  def get_cart_total(self): #장바구니 총 가격
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total  
  def get_cart_items(self): #장바구니 총 가격
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total


class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)
  dated_added = models.DateTimeField(auto_now_add=True)

  @property
  def get_total(self): #해당 아이템 개수에대한 총 가격
    total = self.product.price * self.quantity
    return total


class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  address = models.CharField(max_length=200, null=True)
  city = models.CharField(max_length=200, null=True)
  state = models.CharField(max_length=200, null=True)
  zipcode = models.CharField(max_length=200, null=True)
  dated_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.address+'/'+self.city+'/'+self.state+'/'+self.zipcode


@receiver(post_save, sender=User) #시그널 회원가입 저장
def create_or_update_customer(sender, instance, created, **kwargs):
  if created:
    Customer.objects.create(user=instance, name=instance.username, email=instance.email)
  instance.customer.save()



#댓글
class Comment(models.Model):
  product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE )
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  modify_date = models.DateTimeField(null=True, blank=True)
  approved_comment = models.BooleanField(default=True) #댓글승인
  def __str__(self):
    return self.text