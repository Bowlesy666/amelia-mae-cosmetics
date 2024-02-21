from django.db import migrations, models

def set_default_supplier_values(apps, schema_editor):
    InventoryItem = apps.get_model('inventory', 'InventoryItem')
    InventoryItem.objects.filter(supplier_name='').update(supplier_name='Bowles Beauty Supplys')
    InventoryItem.objects.filter(supplier_email='').update(supplier_email='bowlesdevelopment906@gmail.com')

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_create_inventory_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='supplier_email',
            field=models.EmailField(default='bowlesdevelopment906@gmail.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='supplier_name',
            field=models.CharField(default='Bowles Beauty Supplys', max_length=100),
        ),
        migrations.RunPython(set_default_supplier_values)
    ]
