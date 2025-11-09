from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Invitation(models.Model):
    # id is implicit primary key
    name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)
    
    location = models.CharField(max_length=50)
    description = models.TextField(
        validators=[MaxLengthValidator(500, "La description ne doit pas dépasser 500 caractères.")]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name  

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("La date de fin ne peut pas être antérieure à la date de début.")
        
        if self.start_date and self.start_date < timezone.now().date():
            raise ValidationError("La date de début ne peut pas être dans le passé.")

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'


class Guest(models.Model):    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('declined', 'Décliné'),
        ('attended', 'Présent'),
        ('absent', 'Absent'),
    ]
    
    TITLE_CHOICES = [
        ('mr', 'M.'),
        ('mrs', 'Mme'),
        ('ms', 'Mlle'),
        ('dr', 'Dr'),
        ('prof', 'Prof'),
    ]
    
    invitation = models.ForeignKey(
        Invitation, 
        on_delete=models.CASCADE, 
        related_name='guests',
        verbose_name="Événement"
    )
    
    title = models.CharField(
        max_length=10, 
        choices=TITLE_CHOICES, 
        default='mr',
        verbose_name="Titre"
    )
    
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    
    email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name="Email"
    )
    
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Téléphone"
    )
    
    company = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Entreprise"
    )
    
    position = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Poste"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Statut"
    )
    
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Notes"
    )
    
    plus_one = models.BooleanField(
        default=False,
        verbose_name="Accompagnateur"
    )
    
    dietary_restrictions = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Restrictions alimentaires"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_title_display()} {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        """Return the full name of the guest"""
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Invité'
        verbose_name_plural = 'Invités'
        unique_together = ['invitation', 'email']  # Prevent duplicate emails per event