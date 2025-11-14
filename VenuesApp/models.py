from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time

name_letters_validator = RegexValidator(
    r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$',
    "Name must contain only letters, spaces or hyphens."
)

class Decor(models.Model):
    name = models.CharField(max_length=200, validators=[name_letters_validator])
    category = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="decors/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    nom_v = models.CharField(max_length=200, validators=[name_letters_validator])
    adresse_v = models.CharField(max_length=300)
    nb_place = models.PositiveIntegerField()
    image = models.ImageField(upload_to="venues/", blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    email = models.EmailField()
    type = models.CharField(max_length=120)
    description = models.TextField(validators=[MinLengthValidator(31)])

    # ✅ exactly ONE decor per venue (FK)
    decor = models.ForeignKey(
        Decor,
        on_delete=models.PROTECT,   # prevents deleting a decor that is used by a venue
        related_name="venues",
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_v

# --- Association: réservation d'un venue par un user, liée à un event ---
# ... keep your imports and existing models ...
# VenuesApp/models.py
class VenueReservation(models.Model):
    user  = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='venue_reservations')
    venue = models.ForeignKey('VenuesApp.Venue', on_delete=models.CASCADE, related_name='reservations')
    event = models.OneToOneField('EventApp.Event', on_delete=models.PROTECT, related_name='reservation')

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

        new_start = datetime.combine(self.date_reservation, self.start_time)
        new_end   = new_start + timedelta(minutes=self.duration_minutes)

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
