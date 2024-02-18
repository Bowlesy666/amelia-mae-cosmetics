from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_list, name='articles_list'),
    path('add_article/', views.add_article, name='add_article'),
    path('article_detail/<int:article_id>/', views.article_detail, name='article_detail'),
    path('edit_article/<int:article_id>/', views.edit_article, name='edit_article'),
]