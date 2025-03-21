from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Order,OrderItem


class OrderItemInLine(admin.TabularInline): #admin.StackedInline
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', ]
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user', 'first_name','last_name','email','datetime_created', 'is_paid', ]
    inlines =[
        OrderItemInLine,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', ]

    