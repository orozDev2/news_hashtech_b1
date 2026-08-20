from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from main.models import News, Category
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



# Create your views here.
