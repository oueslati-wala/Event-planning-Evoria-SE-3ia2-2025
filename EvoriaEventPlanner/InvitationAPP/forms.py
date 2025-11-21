from django import forms
from .models import Invitation, Guest
from EventApp.models import Event

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['event', 'name', 'theme', 'start_time', 'dress_code', 'description', 'start_date', 'end_date']
        labels = {
            'event': "Événement",
            'name': "Titre de l'évenement",
            'theme': "Thématique",
            'start_time': "Heure de début",
            'dress_code': "Code vestimentaire",
            'description': "Description",
            'start_date': "Date de début",
            'end_date': "Date de fin",
        }
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Entrer un titre à l'évenement"}),
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Thématique de l'évenement"}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '60'}),
            'dress_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ex: Tenue de soirée"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['event'].queryset = Event.objects.filter(user=user)
        self.fields['event'].required = True
        self.fields['start_date'].required = False
        self.fields['start_time'].required = False
        self.fields['start_date'].widget.attrs['readonly'] = True
        self.fields['start_date'].widget.attrs['disabled'] = True
        self.fields['start_time'].widget.attrs['readonly'] = True
        self.fields['start_time'].widget.attrs['disabled'] = True
        ev_id = (self.data.get('event') if hasattr(self, 'data') else None) or (self.instance.event_id if getattr(self.instance, 'event_id', None) else None)
        if ev_id:
            pass

    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        if event:
            if not cleaned_data.get('start_date') and event.date_evenement:
                cleaned_data['start_date'] = event.date_evenement
            try:
                res = event.reservation
                if res and res.venue and not cleaned_data.get('start_time') and res.start_time:
                    cleaned_data['start_time'] = res.start_time
            except AttributeError:
                pass
        return cleaned_data

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