from django import forms
from .models import InventoryItem


class InventoryItemForm(forms.ModelForm):

    class Meta:
        model = InventoryItem
        fields = [
            'min_threshold',
            'min_order_quantity',
            'supplier_name',
            'supplier_email',
            'cost_per_product',
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'border-black shadow rounded-0'
