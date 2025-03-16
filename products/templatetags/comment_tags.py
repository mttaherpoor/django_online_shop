from django import template
from django.db.models import QuerySet

from models import Comment

register = template.Library()

@register.filter
def only_active_comments(comments: QuerySet[Comment]) -> QuerySet[Comment]:
    return comments.filter(active=True) #comments.exclude(active=False)
 