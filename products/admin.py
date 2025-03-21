from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product,Comment


class CommentInLine(admin.TabularInline): #admin.StackedInline
    model = Comment
    fields = ['auther', 'body', 'stars', 'active', ]
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'price', 'active', ]
    inlines =[
        CommentInLine,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'auther', 'body', 'stars', 'active', ]
    