from django import template
from django.db.models import Count

from main.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all().annotate(news_count=Count('news'))


@register.simple_tag()
def get_categories_by_name(name):
    return Category.objects.filter(name__icontains=name).annotate(news_count=Count('news'))


