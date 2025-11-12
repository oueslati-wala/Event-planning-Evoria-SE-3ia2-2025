from django import forms
from .models import Invitation, Guest

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['name', 'theme', 'location', 'description', 'start_date', 'end_date']
        labels = {
            'name': "Titre de l'évenement",
            'theme': "Thématique",
            'location': "Lieu",
            'description': "Description",
            'start_date': "Date de début",
            'end_date': "Date de fin",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Entrer un titre à l'évenement"}),
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Thématique de l'évenement"}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'title', 'first_name', 'last_name', 'email', 'phone', 
            'company', 'position', 'status', 'notes', 'plus_one', 
            'dietary_restrictions'
        ]
        labels = {
            'invitation': "Événement",
            'title': "Titre",
            'first_name': "Prénom",
            'last_name': "Nom",
            'email': "Email",
            'phone': "Téléphone",
            'company': "Entreprise",
            'position': "Poste",
            'status': "Statut",
            'notes': "Notes",
            'plus_one': "Accompagnateur",
            'dietary_restrictions': "Restrictions alimentaires",
        }
        widgets = {
            'invitation': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Entrer le prénom"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Entrer le nom"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "email@example.com"}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "+33 6 12 34 56 78"}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'entreprise"}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Poste occupé"}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "Notes supplémentaires..."}),
            'plus_one': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dietary_restrictions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': "Allergies, préférences alimentaires..."}),
        }