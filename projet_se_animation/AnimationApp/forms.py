from django import forms
from .models import Animateur, ReservationAnim

class AnimateurForm(forms.ModelForm):
    class Meta:
        model = Animateur
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows":3}),
            "tags": forms.TextInput(attrs={"placeholder": "ex: enfants, magie"}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = ReservationAnim
        fields = "__all__"
        widgets = {
            "date_debut": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "date_fin": forms.DateTimeInput(attrs={"type":"datetime-local"}),
        }
