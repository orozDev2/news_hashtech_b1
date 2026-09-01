from django.contrib import admin
from main.models import News, Category, Tag, NewsLinks
from django.utils.safestring import mark_safe


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'date', 'author', 'get_image')
    list_display_links = ('id', 'title')
    readonly_fields = ('get_full_image', 'date', 'update_date')
    list_filter = ('category', 'tags', 'date', 'update_date')
    search_fields = ('title', 'content', 'author')
    filter_horizontal = ('tags',)

    @admin.display(description='изображение')
    def get_image(self, obj: News):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150px">')
        return '-'

    @admin.display(description='изображение')
    def get_full_image(self, obj: News):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100%">')
        return '-'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)

@admin.register(NewsLinks)
class NewsLinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'whatsapp', 'telegram', 'instagram', 'facebook')
    list_display_links = ('id', 'news',)

# Register your models here.
