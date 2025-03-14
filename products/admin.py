from django.contrib import admin

from .models import Product,Comment


class CommentInLine(admin.TabularInline): #admin.StackedInline
    model = Comment
    fields = ['auther', 'body', 'stars', 'active', ]
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'active', ]
    inlines =[
        CommentInLine,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'auther', 'body', 'stars', 'active', ]
    