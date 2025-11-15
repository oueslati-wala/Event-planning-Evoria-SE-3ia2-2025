from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "firstname",
            "lastname",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your username",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your password",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Confirm your password",
                }
            ),
        }


def save(self, commit=True):
    # Crée l'utilisateur sans l'enregistrer tout de suite
    user = super().save(commit=False)

    # Assigner le rôle par défaut "organizer"
    user.role = "organizer"

    # Enregistre l'utilisateur si commit=True
    if commit:
        user.save()
    return user
