from django.contrib import admin
from main.models import News, Category, NewsImage, Tag, NewsLinks
from django.utils.safestring import mark_safe


class NewsImageInline(admin.TabularInline):
    model = NewsImage  
    extra = 0  
    readonly_fields = ('created_at', 'get_image')
    
    @admin.display(description='изображение')
    def get_image(self, obj: NewsImage):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" width="150px">')
        return '-'
    

class NewsLinksInline(admin.StackedInline):
    model = NewsLinks
    extra = 0


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'date', 'author', 'get_image')
    list_display_links = ('id', 'title')
    readonly_fields = ('get_full_image', 'views', 'date', 'updated_at')
    list_filter = ('category', 'tags', 'date', 'updated_at')
    search_fields = ('title', 'content', 'author')
    filter_horizontal = ('tags',)
    inlines = (NewsImageInline, NewsLinksInline)

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
    search_fields = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name')


@admin.register(NewsLinks)
class NewsLinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'whatsapp', 'telegram', 'instagram', 'facebook')
    list_display_links = ('id', 'news',)
    search_fields = ('id', 'whatsapp', 'telegram', 'instagram', 'facebook')
# Register your models here.
