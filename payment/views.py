import requests
import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings

from orders.models import Order

def payment_process(request:HttpRequest):
    # Get order id from session
    order_id = request.session.get('order_id')
    
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = order.get_total_price() * 10

    zarinpal_request_url = "https://api.zarinpal.com/pg/v4/paymnet/request.json"

    request_header = {
        "accept":"appliction/json",
        "content_type" : "appliction/json",
    }

    request_data ={
        'merchant_id':settings.ZARINPAL_MERCHANT_ID,
        'amount':rial_total_price,
        'description':f'{order.id}:{order.user.first_name} {order.user.last_name}',
        'callback_url':'https://google.com',
    }
    
    res = requests.post(zarinpal_request_url, data=json.dump(request_data), headers=request_header)

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' in data or len(data['errors']):
        return HttpResponse('Error from zarinpal')
    else :
        return redirect(f'https://api.zarinpal.com/pg/StartPay/{authority}')