from django import forms
from .models import Caterer, MenuItem


class CatererForm(forms.ModelForm):
    class Meta:
        model = Caterer
        fields = ['name', 'company_name', 'phone', 'email', 'address', 'website', 'notes', 'status']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'category', 'is_available', 'caterer']
