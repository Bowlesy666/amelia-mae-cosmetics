from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_admin/', views.product_admin, name='product_admin'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin_products_list/', views.admin_products_list, name='admin_products_list'),
    path('reviews_form/<int:product_id>/', views.reviews_form, name='reviews_form'),
    path('delete_review/<int:product_id>/<int:review_id>/', views.delete_review, name='delete_review'),
    path('add_favourite/<int:product_id>/', views.add_favourite, name='add_favourite'),
    path('delete_favourite/<int:product_id>/', views.delete_favourite, name='delete_favourite'),
]
