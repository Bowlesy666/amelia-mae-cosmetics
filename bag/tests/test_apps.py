from django.apps import apps
from django.test import TestCase
from bag.apps import BagConfig


class TestBagConfig(TestCase):
    """Tests the Django app config."""
    def test_app(self):
        self.assertEqual('bag', BagConfig.name)
        self.assertEqual('bag', apps.get_app_config('bag').name)
