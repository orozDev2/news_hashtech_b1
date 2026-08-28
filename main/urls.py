from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.list_page, name='list_news'),
    path('news/<int:news_id>/', views.detail_news, name='detail_news'),
    path('news/category/<int:category_id>/', views.news_by_category, name='news_by_category'),
    path('youtube/', views.youtube, name='youtube'),
    path('workspace/', views.workspace, name='workspace'),
    path('workspace/create-news/', views.create_news, name='create_news'),
    path('workspace/delete-news/<int:news_id>/', views.delete_news, name='delete_news'),
    path('', views.main_page, name='main_page'),
]