from django import forms
from .models import Article
from products.models import Category


class ArticleForm(forms.ModelForm):
    """ Form to create and edit articles """
    class Meta:
        model = Article
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
