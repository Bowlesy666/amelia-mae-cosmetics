# Generated by Django 3.2.23 on 2024-02-06 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='rating',
            new_name='overall_rating',
        ),
    ]
