"""
1. `articles_list`:
   - URL pattern for listing all articles.
   - Maps to the `articles_list` view.

2. `add_article`:
   - URL pattern for adding a new article.
   - Maps to the `add_article` view.

3. `article_detail`:
   - URL pattern for displaying details of a specific article.
   - Uses an integer parameter to identify the article.
   - Maps to the `article_detail` view.

4. `edit_article`:
   - URL pattern for editing an existing article.
   - Uses an integer parameter to identify the article.
   - Maps to the `edit_article` view.

5. `delete_article`:
   - URL pattern for deleting an existing article.
   - Uses an integer parameter to identify the article.
   - Maps to the `delete_article` view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_list, name='articles_list'),
    path('add_article/', views.add_article, name='add_article'),
    path(
        'article_detail/<int:article_id>/',
        views.article_detail, name='article_detail'
    ),
    path(
        'edit_article/<int:article_id>/',
        views.edit_article, name='edit_article'
    ),
    path(
        'delete_article/<int:article_id>/',
        views.delete_article, name='delete_article'
    ),
]
