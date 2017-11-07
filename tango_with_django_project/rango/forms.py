from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

class PageForm(forms.Form):
    title = forms.CharField(max_length=50, help_text='Please enter the page title.')
    url = forms.URLField(max_length=128,initial='http://', help_text='Enter the URL of the page.')
    category = forms.ModelChoiceField(queryset=None)

    def __init__(self, category_name_slug=None, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

        if category_name_slug and Category.objects.filter(slug=category_name_slug).count() > 0:
            self.fields['category'].initial = Category.objects.filter(slug=category_name_slug)[0]


    def clean_category(self):
        cat_name = self.cleaned_data['category']
        if Category.objects.filter(name=cat_name).count() < 1:
            raise ValidationError(('Invalid Category'), code='invalid')
        return self.cleaned_data['category']

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=50, help_text='Please enter the category name.')

    def clean_name(self):
        cat_name = self.cleaned_data['name']
        if Category.objects.filter(slug=slugify(cat_name)).count() > 0:
            raise ValidationError(('Category with similar name already present.'), code='invalid')
        return self.cleaned_data['name']


class UserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise ValidationError(('Email already registered.'), code='invalid')
        return self.cleaned_data['email']

class UserProfileForm(forms.Form):
    website = forms.URLField(max_length=128,initial='http://www.example.com',required=False)
    picture = forms.ImageField(required=False)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
