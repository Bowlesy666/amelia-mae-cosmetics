from django.test import TestCase

from checkout.models import Order


class CheckoutTests(TestCase):
    def setUp(self):
        """ Sets up the category model for test """
        self.order = Order.objects.create(
            order_number = 'AMC123456',
            full_name = 'test user',
            email = 'test email',
            phone_number = '01257442777',
            country = 'United Kingdom',
            postcode = 'PR11PR',
            town_or_city = 'test town',
            street_address1 = 'address1',
            street_address2 = 'address1',
            county = 'Lancashire',
            delivery_cost = '3.50',
            order_total = '35',
            grand_total = '38.5'
        )

    def tearDown(self):
        self.order.delete()