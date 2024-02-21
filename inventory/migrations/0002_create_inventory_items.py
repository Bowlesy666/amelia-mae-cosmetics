from django.db import migrations
from products.models import Product
from inventory.models import InventoryItem

def create_inventory_items(apps, schema_editor):
    for product in Product.objects.all():
        InventoryItem.objects.create(product=product)

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_inventory_items),
    ]
