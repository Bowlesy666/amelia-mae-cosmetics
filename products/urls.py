"""
1. `product_list`:
   - URL pattern for displaying all products.
   - Maps to the `all_products` view.

2. `product_detail`:
   - URL pattern for displaying details of a specific product.
   - Uses a product ID parameter to identify the product.
   - Maps to the `product_detail` view.

3. `product_admin`:
   - URL pattern for accessing the product administration panel.
   - Maps to the `product_admin` view.

4. `add_product`:
   - URL pattern for adding a new product.
   - Maps to the `add_product` view.

5. `edit_product`:
   - URL pattern for editing an existing product.
   - Uses a product ID parameter to identify the product.
   - Maps to the `edit_product` view.

6. `delete_product`:
   - URL pattern for deleting an existing product.
   - Uses a product ID parameter to identify the product.
   - Maps to the `delete_product` view.

7. `admin_products_list`:
   - URL pattern for displaying a list of products in the admin panel.
   - Maps to the `admin_products_list` view.

8. `reviews_form`:
   - URL pattern for accessing the form for adding a review to a product.
   - Uses a product ID parameter to identify the product.
   - Maps to the `reviews_form` view.

9. `delete_review`:
   - URL pattern for deleting a review of a product.
   - Uses both product ID and review ID parameters to identify product/review.
   - Maps to the `delete_review` view.

10. `add_favourite`:
    - URL pattern for adding a product to favorites.
    - Uses a product ID parameter to identify the product.
    - Maps to the `add_favourite` view.

11. `delete_favourite`:
    - URL pattern for removing a product from favorites.
    - Uses a product ID parameter to identify the product.
    - Maps to the `delete_favourite` view.

12. `favourites_list`:
    - URL pattern for displaying a list of favorite products.
    - Maps to the `favourites_list` view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_admin/', views.product_admin, name='product_admin'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),
    path(
        'admin_products_list/',
        views.admin_products_list,
        name='admin_products_list'
    ),
    path(
        'reviews_form/<int:product_id>/',
        views.reviews_form,
        name='reviews_form'
    ),
    path(
        'delete_review/<int:product_id>/<int:review_id>/',
        views.delete_review,
        name='delete_review'
    ),
    path(
        'add_favourite/<int:product_id>/',
        views.add_favourite,
        name='add_favourite'
    ),
    path(
        'delete_favourite/<int:product_id>/',
        views.delete_favourite,
        name='delete_favourite'
    ),
    path(
        'favourites_list/',
        views.favourites_list,
        name='favourites_list'
    ),
]
