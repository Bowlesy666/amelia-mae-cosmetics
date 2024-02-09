from django.test import TestCase

from products.models import Product, Category, Reviews, SkinType


class ProductTests(TestCase):
    """ Tests for Product models """
    def setUp(self):
        """ Sets up the category model for test """
        category = Category(name='cleansers')
        category.save()

    def test_create_product_with_all_fields(self):
        """ Tests for product model creation """
        category = Category.objects.create(name='Test Category')
        skin_type = SkinType.objects.create(name='Test Skin Type')
        product = Product.objects.create(
            category=category,
            skin_type=skin_type,
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

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.sku, '12345')
        self.assertEqual(product.description, 'Test description')
        self.assertEqual(product.price, 10.00)
        self.assertEqual(product.rating, 4.5)
        self.assertEqual(product.image_url, 'https://example.com/image.jpg')
        self.assertEqual(product.image, 'path/to/image.jpg')
        self.assertEqual(product.quantity, 50)
        self.assertFalse(product.is_out_of_stock)
        self.assertFalse(product.is_discontinued)
        self.assertTrue(product.is_best_seller)
        self.assertEqual(product.category.name, 'Test Category')
        self.assertEqual(product.skin_type.name, 'Test Skin Type')

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
        category = Category.objects.get(pk=1)
        self.assertEqual(str(category), ('cleansers'))

    def test_products_str(self):
        """ Tests the string method on a product after its creation """
        test_name = Product(name='productA')
        self.assertEqual(str(test_name), ('productA'))

    def tearDown(self):
        # Delete the Category instance from the test database
        self.category.delete()
