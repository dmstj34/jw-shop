from __future__ import unicode_literals
from django.shortcuts import render


####상점
def store(request):
  
  context={}
  return render(request, 'store/상점.html', context) #앱의 템플릿폴더를 자동인식하기때문에 경로이럼.

####장바구니
def cart(request):
  
  context={}
  return render(request, 'store/장바구니.html', context)

####결제
def checkout(request):
  
  context={}
  return render(request, 'store/결제.html', context)