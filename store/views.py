from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json, datetime
from . cookie import *


####상점
def store(request):
  Data = cart_data(request) # cookie.py > def cookie_cart
  cartItems = Data['cartItems']
  
  products = Product.objects.all()

  context={'products': products, 'cartItems': cartItems}
  return render(request, 'store/상점.html', context) #앱의 템플릿폴더를 자동인식하기때문에 경로이럼.

####장바구니
def cart(request):
  Data = cart_data(request) # cookie.py > def cookie_cart
  cartItems = Data['cartItems']
  order = Data['order']
  items = Data['items']

  context = {'items': items, 'order':order, 'cartItems': cartItems }
  return render(request, 'store/장바구니.html', context)

####결제
def checkout(request):
  Data = cart_data(request) # cookie.py > def cookie_cart
  cartItems = Data['cartItems']
  order = Data['order']
  items = Data['items']

  context = {'items': items, 'order':order, 'cartItems': cartItems}
  return render(request, 'store/결제.html', context)


def updatedItme(request):
  data = json.loads(request.body) #제이슨타입의 데이터 가져오기 (바디에있는)
  productID = data['productID']
  action = data['action']

  customer = request.user.customer
  product = Product.objects.get(id=productID)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
  if action == 'add':
    orderItem.quantity += 1
  elif action == 'sub':
    orderItem.quantity -= 1
  
  orderItem.save()
  if orderItem.quantity <= 0:
    orderItem.delete()

  return JsonResponse('Item added zz', safe=False)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt #csrf 에러 방지


def processOrder(request):
  transation_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)

  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
  else: #미사용자의 결제
    customer, order = client_order(request, data)

  total = int(data['user_form']['total'])
  order.transation_id = transation_id

  if total == order.get_cart_total:
      order.complete = True
  order.save()
  if order.shipping == True:
      ShippingAddress.objects.create(
          customer = customer,
          order = order,
          address = data['shipping']['address'],
          city = data['shipping']['city'],
          state = data['shipping']['state'],
          zipcode = data['shipping']['zipcode'],
  )     

  return JsonResponse('Payment Completed!', safe =False) 
