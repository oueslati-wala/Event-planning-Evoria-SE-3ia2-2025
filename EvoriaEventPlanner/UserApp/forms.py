from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "nationality", "theme", "adresse", "num_tel"]
        # widgets = {
        #     "username": forms.TextInput(attrs={"class": "form-control"}),
        #     "email": forms.EmailInput(attrs={"class": "form-control"}),
        #     "nationality": forms.TextInput(attrs={"class": "form-control"}),
        #     "theme": forms.Select(attrs={"class": "form-select" }),
        #     "adresse": forms.TextInput(attrs={"class": "form-control"}),
        #     "num_tel": forms.TextInput(attrs={"class": "form-control"}),
        # }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "nationality": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nationalité"}
            ),
            "theme": forms.Select(attrs={"class": "nice-select wide"}),
            "adresse": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Adresse"}
            ),
            "num_tel": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}
            ),
        }
