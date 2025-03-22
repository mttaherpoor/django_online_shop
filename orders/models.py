from django.db.models import QuerySet
from django.db import models
from django.conf import settings

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=700)

    order_note = models.CharField(max_length=700, blank=True)
    zarinpal_authority = models.CharField(max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(max_length=150, blank=True)
    zarinpal_data = models.TextField(blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True) 

    def __str__(self) -> str:
        return f'Order {self.id}'

    def get_total_price(self):
        items: QuerySet[OrderItem] = self.items.all()  
        return sum(item.price*item.quantity for item in items)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f'OrderItem {self.id} of order {self.order.id}'


