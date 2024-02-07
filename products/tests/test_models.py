from django.test import TestCase

from products.models import Product, Category, Reviews, SkinType


class ProductTests(TestCase):
    """ Tests for Product models """
    def setUp(self):
        """ Sets up the category model for test """
        category = Category(name='cleansers')
        category.save()

    def test_categories_str(self):
        """ Tests the string method on the category """
        category = Category.objects.get(pk=1)
        self.assertEqual(str(category), ('cleansers'))

    def test_products_str(self):
        """ Tests the string method on a product after its creation """
        test_name = Product(name='productA')
        self.assertEqual(str(test_name), ('productA'))
