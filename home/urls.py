"""
1. `home`:
   - URL pattern for the home page.
   - Maps to the `index` view.

2. `privacy_policy`:
   - URL pattern for the privacy policy page.
   - Maps to the `privacy_policy` view.

3. `shipping_policy`:
   - URL pattern for the shipping policy page.
   - Maps to the `shipping_policy` view.

4. `cookie_policy`:
   - URL pattern for the cookie policy page.
   - Maps to the `cookie_policy` view.

5. `disclaimer`:
   - URL pattern for the disclaimer page.
   - Maps to the `disclaimer` view.

6. `terms_and_conditions`:
   - URL pattern for the terms and conditions page.
   - Maps to the `terms_and_conditions` view.

7. `return_and_refund_policy`:
   - URL pattern for the return and refund policy page.
   - Maps to the `return_and_refund_policy` view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('shipping_policy/', views.shipping_policy, name='shipping_policy'),
    path('cookie_policy/', views.cookie_policy, name='cookie_policy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path(
        'terms_and_conditions/',
        views.terms_and_conditions,
        name='terms_and_conditions'),
    path(
        'return_and_refund_policy/',
        views.return_and_refund_policy,
        name='return_and_refund_policy'),
]
