# VenuesApp/forms.py
from django import forms
from .models import VenueReservation

class ReservationForm(forms.ModelForm):
    start_time = forms.TimeField(
        input_formats=['%H:%M', '%H:%M:%S'],
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'step': '60'})
    )

    class Meta:
        model = VenueReservation
        # IMPORTANT: use the real field names from your model
        fields = ['event', 'start_time', 'duration_minutes']
        widgets = {
            'duration_minutes': forms.NumberInput(attrs={'min': 15, 'step': 15})
        }
