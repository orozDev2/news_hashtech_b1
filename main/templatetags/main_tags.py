from django import template

from main.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_categories_by_name(name):
    return Category.objects.filter(name__icontains=name)


