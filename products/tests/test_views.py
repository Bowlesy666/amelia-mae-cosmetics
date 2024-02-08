from django.test import TestCase

from products.models import Product, Category, Reviews, SkinType


class TestProductViews(TestCase):
    """ Test views for the Products app """
    def setUp(self):
        # Create a Product instance in the test database
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            image='image.png'
        )

    def test_products_list_render(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products_list.html')

    def test_product_detail_render(self):
        product = Product()
        response = self.client.get(f'/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def tearDown(self):
        # Delete the Product instance from the test database
        self.product.delete()
