from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from inventory.models import InventoryItem

@receiver(post_save, sender=Product)
def create_inventory_item(sender, instance, created, **kwargs):
    """
    Signal receiver function to create an InventoryItem for every new Product.
    """
    if created:
        # Create an InventoryItem for the newly created Product
        InventoryItem.objects.create(product=instance)

@receiver(post_delete, sender=Product)
def delete_inventory_item(sender, instance, **kwargs):
    """
    Signal receiver function to delete the corresponding InventoryItem when a Product is deleted.
    """
    try:
        inventory_item = InventoryItem.objects.get(product=instance)
        inventory_item.delete()
    except InventoryItem.DoesNotExist:
        pass
