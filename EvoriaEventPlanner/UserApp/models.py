from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# Create your models here.
import uuid


def generate_user_id():
    return "USER" + uuid.uuid4().hex[:4].upper()


name_validator = RegexValidator(
    regex=r"^[a-zA-Z]+$", message="This field must contain only alphabetic characters."
)


def verify_email(email):
    allowed_domains = [
        "gmail.com",
        "yahoo.fr",
        "esprit.tn",
        "hotmail.com",
        "outlook.com",
        "yahoo.com",
    ]
    domain = email.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(
            f"L'email doit être sur un domaine autorisé : {', '.join(allowed_domains)}"
        )


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.role_id} - {self.name}"


class User(AbstractUser):
    user_id = models.CharField(
        max_length=8, primary_key=True, default=generate_user_id, editable=False
    )
    firstname = models.CharField(max_length=30, validators=[name_validator])
    lastname = models.CharField(max_length=30, validators=[name_validator])
    email = models.EmailField(unique=True, validators=[verify_email])
    nationality = models.CharField(max_length=50, null=True)
    num_tel = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    file_validator = FileExtensionValidator(
        allowed_extensions=["png", "jpg"],
        message="Le fichier doit être au format PNG ou JPG.",
    )
    # photo = models.ImageField(upload_to='users_photos/', blank=True, null=True, validators=[file_validator])
    Themes = [
        ("light", "Light"),
        ("dark", "Dark"),
    ]
    theme = models.CharField(max_length=50, choices=Themes, default="light")
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, related_name="users", default=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            newid = generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid = generate_user_id()
            self.user_id = newid
        super().save(*args, **kwargs)
