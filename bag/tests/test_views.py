from django.test import TestCase
from django.shortcuts import reverse

from products.models import Product


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

    def test_remove_from_bag(self):
        item = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            image='image.png',
            is_best_seller=True,
        )

        session = self.client.session
        session['bag'] = {item.id: 1}
        session.save()

        response = self.client.get(reverse('remove_from_bag', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(item.id, self.client.session['bag'])
