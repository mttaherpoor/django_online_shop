import requests
import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.conf import settings

from orders.models import Order

def payment_process(request:HttpRequest):
    # Get order id from session
    order_id = request.session.get('order_id')
    
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = "https://payment.zarinpal.com/pg/v4/payment/request.json"

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data ={
        'merchant_id':settings.ZARINPAL_MERCHANT_ID,
        'amount':rial_total_price,
        'description':f'#{order.id}:{order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback'))
        
    }
     
    
    res = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' in data or len(data['errors']):
        return HttpResponse('Error from zarinpal')
    else :
        return redirect(f'https://payment.zarinpal.com/pg/StartPay/{authority}')
    
def payment_callback_view(request:HttpRequest):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
        "accept": "application/json",
        "content-type": "application/json",
        }

        request_data ={
            'merchant_id':settings.ZARINPAL_MERCHANT_ID,
            'amount':rial_total_price,
            'authority':payment_authority,
        }
        res = requests.post(
            url='https://payment.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
        )

        if  'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors'] == 0)):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')
            
            elif payment_code == 101:
                return HttpResponse(' پرداخت شما با موفقیت انجام شد.البته این تراکنش قبلا ثبت شده است.')

            else:
                error_code = res.json()['errors']['code']
                error_message =res.json()['errors']['message']
                return HttpResponse(f'{error_code}{error_message} تراکتش ناموفق بود.')
    else:
        return HttpResponse(' تراکتش ناموفق بود!.')

def payment_process_sandbox(request:HttpRequest):
    # Get order id from session
    order_id = request.session.get('order_id')
    
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data ={
        'MerchantID':'b8c1b14c-788d-4045-96b7-f424fec24013',
        'Amount':rial_total_price,
        'Description':f'#{order.id}:{order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('payment:payment_callback'))
        
    }
    
    res = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    print(res)
    data = res.json()
    print(data)
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' in data or len(data['errors']):
        return HttpResponse('Error from zarinpal')
    else :
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
  
def payment_callback_view_sandbox(request:HttpRequest):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept":"appliction/json",
            "content_type" : "appliction/json",
        }

        request_data ={
            'MerchantID':'abcABCabcABCabcABCabcABCabcABCabcABC',
            'Amount':rial_total_price,
            'Authority':payment_authority,
        }
        res = requests.post(
            url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
            json=request_data,
            headers=request_header
        )

        if 'errors' not in res.json():
            data = res.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['RedID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')
            
            elif payment_code == 101:
                return HttpResponse(' پرداخت شما با موفقیت انجام شد.البته این تراکنش قبلا ثبت شده است.')

            else:
                error_code = res.json()['errors']['code']
                error_message =res.json()['errors']['message']
                return HttpResponse(f'{error_code}{error_message} تراکتش ناموفق بود.')
    else:
        return HttpResponse(' تراکتش ناموفق بود!.')
