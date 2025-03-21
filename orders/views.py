from django.http import HttpRequest
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product

@login_required
def order_create_view(request:HttpRequest):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('You can not proceed to checkout page because your cart is empty.'))
        return redirect('product_list')

    if request.method =='POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj:Order = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product :Product = item['product_obj']
                OrderItem.objects.create(
                    order = order_obj,
                    product = product,
                    quantity = item['quantity'],
                    price = product.price,
                )
            cart.clear()

            
            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.first_name
            request.user.save()

            request.session['order_id'] = order_obj.id 
            return redirect('payment:payment_process') 
            messages.success(request, _('Your order has successfully placed.'))

    return render(request, 'orders/order_create.html',{
        'form':OrderForm(),
    })