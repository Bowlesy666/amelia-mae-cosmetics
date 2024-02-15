from django.test import TestCase

from products.models import Product, Category, Reviews, SkinType


class TestProductViews(TestCase):
    """ Test views for the Products app """
    def setUp(self):
        # Create a Product instance in the test database
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            image='image.png',
            is_best_seller=True,
            category=self.category
        )
        self.category_two = Category.objects.create(name='Test Category Two')
        self.product_two = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=50.00,
            image='image.png',
            is_best_seller=True,
            category=self.category_two
        )


    def test_search_with_query(self):
        response = self.client.get('/products/', {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products_list.html')
        # check search term is in context
        self.assertIn('search_term', response.context)
        # check it matches the query
        self.assertEqual(response.context['search_term'], 'Test')

    def test_search_with_is_best_seller(self):
        response = self.client.get('/products/', {'is_best_seller': True})
        # Check returns best seller is True
        self.assertIn(self.product, response.context['products'])

    def test_search_with_category(self):
        response = self.client.get('/products/', {'category': 'Test Category'})
        # Check returns best seller is True
        self.assertIn(self.product, response.context['products'])

    def test_sort(self):
        response = self.client.get('/products/?sort=price&direction=asc')
        # Check returns best seller is True
        self.assertQuerysetEqual(response.context['products'], Product.objects.all().order_by('price'),transform=lambda x: x)
        response_desc = self.client.get('/products/?sort=category&direction=desc')
        # Check returns best seller is True
        self.assertQuerysetEqual(response_desc.context['products'], Product.objects.all().order_by('-category'),transform=lambda x: x)

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
        # Delete the test instances from the test database
        self.product.delete()
