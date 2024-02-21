from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_inventory, name='view_inventory'),
    path('edit_inventory/<int:inventory_item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
]
