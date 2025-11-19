from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time

# Valideur de nom : uniquement lettres, espaces et tirets
name_letters_validator = RegexValidator(
    r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$',
    "Le nom doit contenir uniquement des lettres, espaces ou tirets."
)

# Valideur pour les formats d'images
def validate_image_format(image):
    valid_extensions = ["jpg", "jpeg", "png", "webp"]
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Format d'image non valide. Formats acceptés : JPG, JPEG, PNG, WEBP.")

class Decor(models.Model):
    DECOR_CATEGORIES = [
        ("floral", "Décor Floral"),
        ("table", "Décor de Table"),
        ("lighting", "Éclairage"),
        ("stage", "Scène / Podium"),
        ("entrance", "Entrée / Accueil"),
        ("traditional", "Traditionnel"),
        ("modern", "Moderne"),
    ]

    name = models.CharField(
        max_length=200,
        validators=[name_letters_validator],
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "Le nom du décor est obligatoire."}
    )
    category = models.CharField(
        max_length=120,
        choices=DECOR_CATEGORIES,
        blank=False,
        null=False,
        error_messages={"blank": "La catégorie est obligatoire."}
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
        error_messages={"blank": "Le prix est obligatoire."}
    )
    available = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to="decors/",
        blank=False,  # obligatoire
        null=True,
        validators=[validate_image_format],
        error_messages={"blank": "L'image du décor est obligatoire."}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Venue(models.Model):
    VENUE_TYPES = [
        ("wedding_hall", "Salle de mariage"),
        ("luxury_hotel", "Hôtel de luxe"),
        ("outdoor", "Espace extérieur"),
        ("garden", "Jardin"),
        ("castle", "Château"),
        ("ballroom", "Salle de réception"),
        ("restaurant", "Restaurant"),
    ]

    nom_v = models.CharField(
        max_length=200,
        validators=[name_letters_validator],
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "Le nom du venue est obligatoire."}
    )
    adresse_v = models.CharField(
        max_length=300,
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "L'adresse du venue est obligatoire."}
    )
    nb_place = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "Le nombre de places est obligatoire."}
    )
    image = models.ImageField(
        upload_to="venues/",
        blank=False,  # obligatoire
        null=True,
        validators=[validate_image_format],
        error_messages={"blank": "L'image du venue est obligatoire."}
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(50)],
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "Le prix du venue est obligatoire."}
    )
    email = models.EmailField(
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "L'email du venue est obligatoire."}
    )
    type = models.CharField(
        max_length=120,
        choices=VENUE_TYPES,
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "Le type de venue est obligatoire."}
    )
    description = models.TextField(
        validators=[MinLengthValidator(31)],
        blank=False,  # obligatoire
        null=False,
        error_messages={"blank": "La description du venue est obligatoire."}
    )

    decor = models.ForeignKey(
        Decor,
        on_delete=models.PROTECT,  # empêche la suppression d'un décor lié à un venue
        related_name="venues",
        null=False,
        blank=False,
        error_messages={"blank": "Le décor est obligatoire."}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_v


# --- Association: réservation d'un venue par un user, liée à un event ---
# ... keep your imports and existing models ...
# VenuesApp/models.py
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class VenueReservation(models.Model):
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='venue_reservations')
    venue = models.ForeignKey('VenuesApp.Venue', on_delete=models.CASCADE, related_name='reservations')
    event = models.OneToOneField('EventApp.Event', on_delete=models.CASCADE, related_name='reservation')

    date_reservation = models.DateField()
    start_time = models.TimeField(null=True, blank=True, default=time(12, 0))
    duration_minutes = models.PositiveIntegerField(default=60)

    nom_reservation = models.CharField(max_length=200)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def end_time(self):
        if not self.start_time:
            return None
        dt = datetime.combine(self.date_reservation, self.start_time)
        return (dt + timedelta(minutes=self.duration_minutes)).time()

    def clean(self):
        # Guard: skip until all needed fields exist
        if not self.venue or not self.date_reservation or not self.start_time or not self.duration_minutes:
            return

        qs = VenueReservation.objects.filter(
            venue=self.venue, date_reservation=self.date_reservation
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        # Ensure start_time is a datetime.time object
        if isinstance(self.start_time, datetime):
            start_time = self.start_time.time()
        else:
            start_time = self.start_time

        new_start = datetime.combine(self.date_reservation, start_time)
        new_end = new_start + timedelta(minutes=self.duration_minutes)

        for r in qs:
            if not r.start_time:
                continue
            rs = datetime.combine(r.date_reservation, r.start_time)
            re = rs + timedelta(minutes=r.duration_minutes)
            if new_start < re and new_end > rs:
                raise ValidationError("Ce créneau horaire est déjà pris pour ce venue.")

    def __str__(self):
        st = self.start_time.strftime('%H:%M') if self.start_time else '--:--'
        return f"{self.nom_reservation} – {self.user} @ {self.venue} ({self.date_reservation} {st})"
