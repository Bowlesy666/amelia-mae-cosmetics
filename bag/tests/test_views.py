from django.test import TestCase


class TestBagViews(TestCase):
    """ Test views for the Bag app """
    def test_home(self):
        response = self.client.get('/bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')
