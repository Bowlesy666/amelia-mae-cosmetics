from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """ Form for creating and updating products """
    class Meta:
        model = Product
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            categories = Category.objects.all()
            # list comprehension
            friendly_names = [(
                c.id, c.get_friendly_name()) for c in categories]

            self.fields['category'].choices = friendly_names
            # match theme of the rest of the store
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'border-black shadow rounded-0'


class ReviewsForm(forms.Form):
    """ Form for creating reviews """
    rating = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'rating-value'})
    )
    comment = forms.CharField(label='Comment', widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('comment')
        rating = cleaned_data.get('rating')

        if not comment:
            raise forms.ValidationError("Remember to add your comment here!")
        if rating < 1:
            raise forms.ValidationError("Remember to add your stars!")

        return cleaned_data
