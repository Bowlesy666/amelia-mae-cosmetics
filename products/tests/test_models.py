from django.test import TestCase
from django.contrib.auth.models import User

from products.models import Product, Category, Reviews, SkinType


class ProductTests(TestCase):
    """ Tests for Product models """
    def setUp(self):
        """ Sets up the category model for test """
        self.category = Category.objects.create(
            name='Test Category', friendly_name='Category Friendly')
        self.skin_type = SkinType.objects.create(
            name='Test Skin Type', friendly_name='Skin Type Friendly')
        self.product = Product.objects.create(
            category=self.category,
            skin_type=self.skin_type,
            sku='12345',
            name='Test Product',
            description='Test description',
            price=10.00,
            rating=4.5,
            image_url='https://example.com/image.jpg',
            image='path/to/image.jpg',
            quantity=50,
            is_out_of_stock=False,
            is_discontinued=False,
            is_best_seller=True
        )

    def test_create_product_with_all_fields(self):
        """ Tests for product model creation """
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.sku, '12345')
        self.assertEqual(self.product.description, 'Test description')
        self.assertEqual(self.product.price, 10.00)
        self.assertEqual(self.product.rating, 4.5)
        self.assertEqual(self.product.image_url, 'https://example.com/image.jpg')
        self.assertEqual(self.product.image, 'path/to/image.jpg')
        self.assertEqual(self.product.quantity, 50)
        self.assertFalse(self.product.is_out_of_stock)
        self.assertFalse(self.product.is_discontinued)
        self.assertTrue(self.product.is_best_seller)
        self.assertEqual(self.product.category.name, 'Test Category')
        self.assertEqual(self.product.skin_type.name, 'Test Skin Type')

    def test_update_out_of_stock_status(self):
        """ Tests if out of stock updates automatically """
        product_with_quantity = Product.objects.create(
            name='Test Product', quantity=10, price=10.00)
        product_with_quantity.update_out_of_stock_status()
        product_without_quantity = Product.objects.create(
            name='Test Product 2', quantity=0, price=10.00)
        product_without_quantity.update_out_of_stock_status()
        self.assertFalse(product_with_quantity.is_out_of_stock)
        self.assertTrue(product_without_quantity.is_out_of_stock)

    def test_categories_str(self):
        """ Tests the string method on the category """
        category = Category.objects.get(name='Test Category')
        self.assertEqual(str(category), 'Test Category')

    def test_skin_types_str(self):
        """ Tests the string method on the skin type """
        skin_type = SkinType.objects.get(name='Test Skin Type')
        self.assertEqual(str(skin_type), 'Test Skin Type')

    def test_reviews_str(self):
        """ Tests the string method on Reviews """
        user = User.objects.create_user(
            username='test user', password='password123')
        reviews = Reviews.objects.create(
            user=user, comment='Lorem ipsum, this is a test comment',
            rating=5, product_id=1)
        self.assertEqual(
            str(reviews),
            'Review by test user: Lorem ipsum, this is a test comment...')

    def test_categories_friendly_name(self):
        """ Tests the friendly_name method on the category """
        category = Category.objects.get(friendly_name='Category Friendly')
        friendly_name = category.get_friendly_name()
        self.assertEqual(str(friendly_name), 'Category Friendly')

    def test_skin_types_friendly_name(self):
        """ Tests the friendly_name method on the skin type """
        skin_type = SkinType.objects.get(friendly_name='Skin Type Friendly')
        friendly_name = skin_type.get_friendly_name()
        self.assertEqual(str(friendly_name), 'Skin Type Friendly')

    def test_products_str(self):
        """ Tests the string method on a product after its creation """
        self.assertEqual(str(self.product), ('Test Product'))

    def tearDown(self):
        # Delete the Category instance from the test database
        self.category.delete()
        self.skin_type.delete()
        self.product.delete()
