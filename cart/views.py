from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpRequest

from  .cart import Cart
from products.models import Product
from .forms import AddToCartForm

def cart_detail_view(request:HttpRequest):
    cart = Cart(request)

    return render(request, 'cart/cart_detail.html', {
        'cart':cart,
    })

def add_to_cart_view(request:HttpRequest, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity  = cleaned_data["quantity"]
        cart.add(product, quantity)

    return redirect('cart:cart_detail')
