from django import forms
from .models import Caterer, MenuItem, CateringReservation


class CatererForm(forms.ModelForm):
    class Meta:
        model = Caterer
        fields = ['name', 'company_name', 'phone', 'email', 'address', 'website', 'notes', 'status']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'category', 'is_available', 'caterer']


class CateringReservationForm(forms.ModelForm):
    start_time = forms.TimeField(
        input_formats=['%H:%M', '%H:%M:%S'],
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'step': '60'})
    )

    class Meta:
        model = CateringReservation
        fields = ['event', 'start_time', 'duration_minutes']
        widgets = {
            'duration_minutes': forms.NumberInput(attrs={'min': 15, 'step': 15})
        }
