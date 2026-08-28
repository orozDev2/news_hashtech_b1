from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from main.models import News, Category, Tag
import datetime


def main_page(request):
    print('Wellcome to our news site')

    # return redirect('/news/')  # Direct link
    return redirect('list_news')  # Named link


def list_page(request):
    news = News.objects.all()

    search = request.GET.get('search')

    if search:
        news = news.filter(title__icontains=search)

    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 3)

    pagin = Paginator(news, page_size)
    news = pagin.get_page(page)

    categories = Category.objects.all()
    return render(request, 'index.html', {'news': news, 'categories': categories})



def detail_news(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return render(request, 'extra_pages/not_found_404.html')

    print(news)
    return render(request, 'detail_news.html', {'news': news})


def youtube(request):

    minute = datetime.datetime.now().minute
    if minute % 2 == 0:
        print('Opening youtube.....')
        return redirect('https://www.youtube.com/')

    return render(request, 'extra_pages/not_found_404.html')


def news_by_category(request, category_id):
    news = News.objects.filter(category__id=category_id)

    categories = Category.objects.all()
    return render(request, 'index.html', {'news': news, 'categories': categories})


def workspace(request):
    news = News.objects.all()

    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 3)

    pagin = Paginator(news, page_size)
    news = pagin.get_page(page)
    
    return render(request, 'workspace/index.html', {'news': news})



def create_news(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        author = request.POST.get('author')
        content = request.POST.get('content')
        category = Category.objects.get(id=int(request.POST.get('category')))
        tags_id = list(map(int, request.POST.getlist('tags')))
        tags = Tag.objects.filter(id__in=tags_id)
        
        news = News.objects.create(
            title=title,
            author=author,
            content=content,
            category=category,
        )
        
        if image:
            news.image.save(image.name, image)
        
        news.tags.add(*tags)
        
        news.save()
        
        return redirect('workspace')
        
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'workspace/create_news.html', {'categories': categories, 'tags': tags})


def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    return redirect('workspace')

# Create your views here.
