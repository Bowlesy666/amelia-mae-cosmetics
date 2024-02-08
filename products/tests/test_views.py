from django.test import TestCase

from products.models import Product, Category, Reviews, SkinType


class TestProductViews(TestCase):
    """ Test views for the Products app """
    def test_products_list_render(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products_list.html')

    def test_product_detail_render(self):
        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
