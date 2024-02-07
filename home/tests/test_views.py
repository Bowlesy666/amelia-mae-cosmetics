from django.test import TestCase


class TestViews(TestCase):
    """ Test views for the Home app """
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
