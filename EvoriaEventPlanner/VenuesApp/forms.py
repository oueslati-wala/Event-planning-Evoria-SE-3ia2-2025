# VenuesApp/forms.py
from django import forms
from .models import VenueReservation
from EventApp.models import Event
class ReservationForm(forms.ModelForm):
    start_time = forms.TimeField(
        input_formats=['%H:%M', '%H:%M:%S'],
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'step': '60'})
    )

    class Meta:
        model = VenueReservation
        fields = ['event', 'start_time', 'duration_minutes']
        widgets = {
            'duration_minutes': forms.NumberInput(attrs={'min': 15, 'step': 15})
        }

    def __init__(self, *args, **kwargs):
        # 👉 on récupère le user passé depuis la view
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None and user.is_authenticated:
            # 👉 ne montrer que les events créés par ce user
            self.fields['event'].queryset = Event.objects.filter(user=user).order_by('-created_at')
        else:
            # aucun event si user anonyme / non fourni
            self.fields['event'].queryset = Event.objects.none()
