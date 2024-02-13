from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),
    path('cache_chekcout_data/', views.cache_chekcout_data, name='cache_chekcout_data'),
    path('wh/', webhook, name='webhook'),
]
