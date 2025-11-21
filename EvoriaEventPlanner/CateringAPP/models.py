from django.db import models
from datetime import datetime, timedelta, time
from django.core.exceptions import ValidationError


class Caterer(models.Model):
    name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=(('active', 'Actif'), ('inactive', 'Inactif')),
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name or self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    category = models.CharField(
        max_length=40,
        choices=(
            ('entree', 'Entrée'),
            ('main', 'Plat'),
            ('dessert', 'Dessert'),
            ('drink', 'Boisson'),
        ),
        default='main'
    )
    is_available = models.BooleanField(default=True)
    caterer = models.ForeignKey(Caterer, null=True, blank=True, on_delete=models.SET_NULL, related_name='menu_items')

    def __str__(self):
        return self.title


class CateringReservation(models.Model):
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='catering_reservations')
    caterer = models.ForeignKey('CateringAPP.Caterer', on_delete=models.CASCADE, related_name='reservations')
    event = models.OneToOneField('EventApp.Event', on_delete=models.CASCADE, related_name='reservation_catering')

    date_reservation = models.DateField()
    start_time = models.TimeField(null=True, blank=True, default=time(12, 0))
    duration_minutes = models.PositiveIntegerField(default=60)

    nom_reservation = models.CharField(max_length=200)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if not self.caterer or not self.date_reservation or not self.start_time or not self.duration_minutes:
            return
        qs = CateringReservation.objects.filter(caterer=self.caterer, date_reservation=self.date_reservation)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        new_start = datetime.combine(self.date_reservation, self.start_time)
        new_end = new_start + timedelta(minutes=self.duration_minutes)
        for r in qs:
            if not r.start_time:
                continue
            rs = datetime.combine(r.date_reservation, r.start_time)
            re = rs + timedelta(minutes=r.duration_minutes)
            if new_start < re and new_end > rs:
                raise ValidationError("Ce créneau horaire est déjà pris pour ce traiteur.")

    def __str__(self):
        st = self.start_time.strftime('%H:%M') if self.start_time else '--:--'
        return f"{self.nom_reservation} – {self.user} @ {self.caterer} ({self.date_reservation} {st})"
