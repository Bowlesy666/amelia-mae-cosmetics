from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_admin/', views.product_admin, name='product_admin'),
    path('add/', views.add_product, name='add_product'),
]
