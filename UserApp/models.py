from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
class User(models.Model):
    # id auto par Django (pas besoin de le déclarer)
    nom = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "User (app)"
        verbose_name_plural = "Users (app)"  # pour éviter la confusion avec l'auth Django

    def __str__(self):
        return self.nom
