from django.test import TestCase


class TestBagViews(TestCase):
    """ Test views for the Bag app """
    def test_view_bag(self):
        response = self.client.get('/bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        item_id = 1
        data = {'quantity': 4, 'redirect_url': '/'}
        response = self.client.post(f'/bag/add/{item_id}/', data)
        self.assertRedirects(response, '/')
        response_now_bag_has_item = self.client.post(f'/bag/add/{item_id}/', data)
        self.assertRedirects(response_now_bag_has_item, '/')

    def test_quick_add_to_bag(self):
        item_id = 1
        data = {'quantity': 1, 'redirect_url': '/'}
        response = self.client.post(f'/bag/quick_add/{item_id}/', data)
        self.assertRedirects(response, '/')
        response_now_bag_has_item = self.client.post(f'/bag/quick_add/{item_id}/', data)
        self.assertRedirects(response_now_bag_has_item, '/')
