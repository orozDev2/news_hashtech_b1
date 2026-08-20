from django.contrib import admin
from main.models import News, Category, Tag, NewsLinks

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsLinks)

# Register your models here.
