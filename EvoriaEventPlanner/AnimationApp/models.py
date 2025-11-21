from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

class Animateur(models.Model):
    IN_OUT = [("interieur","Intérieur"),("exterieur","Extérieur"),("mixte","Mixte")]
    nom = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    type_animation = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    description = models.TextField(blank=True)
    prix_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])           # DT
    capacite_max = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100000)])
    interieur_exterieur = models.CharField(max_length=20, choices=IN_OUT, default="mixte")
    disponible = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="animateurs/", blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)       # ex: "enfants, magie, clown"
    tags_auto = models.CharField(max_length=255, blank=True)  # réservé IA
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.nom} – {self.type_animation}"

class ReservationAnim(models.Model):
    STATUT = [("brouillon","Brouillon"),("confirme","Confirmé"),("annule","Annulé")]
    animateur = models.ForeignKey(Animateur, on_delete=models.CASCADE, related_name="reservations")
    id_evenement = models.ForeignKey('EventApp.Event', on_delete=models.CASCADE, related_name='reservations_animation')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=140, validators=[MinLengthValidator(2)])
    statut = models.CharField(max_length=12, choices=STATUT, default="brouillon")
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.date_fin and self.date_debut and self.date_fin <= self.date_debut:
            raise ValidationError("La date de fin doit être après la date de début.")
        if self.date_debut and self.date_debut < timezone.now() and self.statut=="confirme":
            raise ValidationError("Impossible de confirmer une réservation dans le passé.")
        # Conflit de créneau pour le même animateur
        if self.animateur_id and self.date_debut and self.date_fin:
            qs = ReservationAnim.objects.filter(
                animateur_id=self.animateur_id,
                date_debut__lt=self.date_fin,
                date_fin__gt=self.date_debut,
            )
            if self.pk: qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Créneau déjà réservé pour cet animateur.")

    def __str__(self): return f"Res#{self.pk} – {self.animateur.nom}"
