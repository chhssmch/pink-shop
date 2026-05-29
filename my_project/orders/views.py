from django.shortcuts import render
from .models import Order 

def order_list(request):
    orders = Order.objects.all().prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})