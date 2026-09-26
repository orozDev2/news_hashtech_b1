from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from main.forms import NewsForm
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
    page_size = request.GET.get('page_size', 12)

    pagin = Paginator(news, page_size)
    news = pagin.get_page(page)

    return render(request, 'index.html', {'news': news})



def detail_news(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return render(request, 'extra_pages/not_found_404.html')
    
    news.views += 1
    news.save()

    return render(request, 'detail_news.html', {'news': news})


def youtube(request):

    minute = datetime.datetime.now().minute
    if minute % 2 == 0:
        print('Opening youtube.....')
        return redirect('https://www.youtube.com/')

    return render(request, 'extra_pages/not_found_404.html')


def news_by_category(request, category_id):
    news = News.objects.filter(category__id=category_id)

    return render(request, 'index.html', {'news': news})


def workspace(request):
    news = News.objects.all()

    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 12)

    pagin = Paginator(news, page_size)
    news = pagin.get_page(page)
    
    return render(request, 'workspace/index.html', {'news': news})



def create_news(request):
    form = NewsForm()

    if request.method == 'POST':
        form = NewsForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            news = form.save()
            messages.success(request, f'Новость "{news.title}" успешно добавилось.')
            return redirect('workspace')
        
        messages.error(request, f'Исправьте ошибки.')

    return render(request, 'workspace/create_news.html', {'form': form})


def delete_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    messages.success(request, f'Новость "{news.title}" успешно удалена.')
    return redirect('workspace')


def update_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    form = NewsForm(instance=news)
    
    if request.method == 'POST':
        form = NewsForm(instance=news, data=request.POST, files=request.FILES)
        
        if form.is_valid():
            news = form.save()
            messages.success(request, f'Новость "{news.title}" успешно сохранена.')
            return redirect('workspace')
        
        messages.error(request, f'Исправьте ошибки.')
            
    return render(request, 'workspace/update_news.html', 
                  {'news': news, 'form': form})

# Create your views here.
