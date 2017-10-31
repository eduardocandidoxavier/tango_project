from django import forms
from rango.models import Page, Category
from django.core.exceptions import ValidationError

class PageForm(forms.Form):
    title = forms.CharField(max_length=50, help_text='Please enter the page title.')
    url = forms.URLField(max_length=128,initial='http://', help_text='Enter the URL of the page.')
    category = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    def clean_category(self):
        cat_name = self.cleaned_data['category']
        if Category.objects.filter(name=cat_name).count() < 1:
            raise ValidationError(_('Invalid Category'), code='invalid')
        return self.cleaned_data['category']

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=50, help_text='Please enter the category name.')


