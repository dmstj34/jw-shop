import json
from . models import *

def cookie_cart(request):
  try:
    cart = json.loads(request.COOKIES['cart'])
  except: #쿠키없어서 못가져오는경우
    cart = {}

  items = []
  order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
  cartItems = order['get_cart_items']

  for i in cart:
    try:
      cartItems += cart[i]['quantity']
      product = Product.objects.get(id=i)
      total = (product.price * cart[i]['quantity'])
      order['get_cart_total'] += total
      order['get_cart_items'] += cart[i]['quantity']
      item = {
        'product': {'id': product.id, 'name': product.name, 'price':product.price, 'imageURL':product.imageURL},
        'quantity': cart[i]['quantity'],
        'get_total': total
      }
      items.append(item)
      if product.digital == False:
        order['shipping'] = True
    
    except: #장바구니에 디지털제품삭제한경우 에러 방지
      pass
  return {'items':items, 'order':order, 'cartItems':cartItems}

def cart_data(request):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False) #주문가져오기
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    CookieData = cookie_cart(request) # cookie.py > def cookie_cart
    cartItems = CookieData['cartItems']
    order = CookieData['order']
    items = CookieData['items']
  return {'items':items, 'order':order, 'cartItems':cartItems}
