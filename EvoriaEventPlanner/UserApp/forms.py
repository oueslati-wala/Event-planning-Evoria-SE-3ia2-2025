from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

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
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())  # Ajoute le reCAPTCHA
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
class LoginForm(forms.Form):
    # email = forms.EmailField()
    # password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(
    widget=forms.EmailInput(attrs={
        "placeholder": "", 
        "autocomplete": "email",
        "class": "input-field"
    })
    )

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        "placeholder": "",
        "autocomplete": "current-password",
        "class": "input-field"
    })
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is None or not user.check_password(password):
                raise forms.ValidationError("Email ou mot de passe incorrect")

        return cleaned_data
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password")
        pw2 = cleaned_data.get("confirm_password")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return cleaned_data