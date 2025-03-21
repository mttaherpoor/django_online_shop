from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_ckeditor_5.fields import CKEditor5Field

class Product(models.Model):
    title = models.CharField(verbose_name=_('Product title'), max_length=100)
    description = CKEditor5Field(_('Product description'), config_name='extends')
    short_description = models.TextField(_('Product short description'), blank=True)
    price = models.PositiveIntegerField(_('price'), default=0)
    active = models.BooleanField(_('active'), default=0)
    image = models.ImageField(verbose_name=_('Product_image'), upload_to='product/product_cover', blank=True)

    datetime_created = models.DateTimeField(verbose_name=_('Date Time of Created'), default=timezone.datetime,)
    datetime_modified = models.DateTimeField(auto_now=True) 

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
       return reverse('product_detail', args=[self.pk])


class ActiveCommentManger(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(ActiveCommentManger, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS =[
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),

    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    auther = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name=_('comment_text'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS)

    
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True) 

    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_comments_manager = ActiveCommentManger()

    def get_absolute_url(self):
       return reverse('product_detail', args=[self.product.id])
    