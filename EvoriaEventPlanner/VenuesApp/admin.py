# VenuesApp/admin.py
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Venue, Decor, VenueReservation


# ---------- Venue form: radio for decor + euro label on price ----------
class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"
        widgets = {
            "decor": forms.RadioSelect,                       # single-choice
            "prix": forms.NumberInput(attrs={"step": "0.01", "placeholder": "€"}),  # nicer input + hint
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: only show available decors (remove this line if you want all)
       
        # Show € in the label
        self.fields["prix"].label = "Prix (€)"


# ---------- Decor admin ----------
@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "price_euro", "available", "created_at")
    list_filter = ("available", "category")
    search_fields = ("name",)
    readonly_fields = ("preview",)

    @admin.display(description="Prix (€)", ordering="price")
    def price_euro(self, obj):
        return f"{obj.price:.2f} €" if obj.price is not None else "—"

    @admin.display(description="Image")
    def thumb(self, obj):
        return format_html(
            '<img src="{}" style="height:60px;width:auto;border-radius:6px;" />',
            obj.image.url
        ) if obj.image else "—"

    @admin.display(description="Aperçu")
    def preview(self, obj):
        return format_html(
            '<img src="{}" style="max-height:200px;width:auto;border-radius:8px;" />',
            obj.image.url
        ) if obj.image else "—"


# ---------- Venue admin ----------
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    list_display = ("thumb", "nom_v", "nb_place", "prix_euro", "email", "decor", "created_at")
    search_fields = ("nom_v", "adresse_v", "email", "type")
    list_filter = ("type",)
    readonly_fields = ("preview", "created_at", "updated_at")
    fieldsets = (
        ("Infos générales", {"fields": ("nom_v", "adresse_v", "nb_place", "type", "description")}),
        ("Média", {"fields": ("image", "preview")}),
        ("Décor", {"fields": ("decor",)}),     # single-choice radio
        ("Tarif & contact", {"fields": ("prix", "email")}),
        ("Suivi", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Prix (€)", ordering="prix")
    def prix_euro(self, obj):
        return f"{obj.prix:.2f} €" if obj.prix is not None else "—"

    @admin.display(description="Image")
    def thumb(self, obj):
        return format_html(
            '<img src="{}" style="height:60px;width:auto;border-radius:6px;" />',
            obj.image.url
        ) if obj.image else "—"

    @admin.display(description="Aperçu")
    def preview(self, obj):
        return format_html(
            '<img src="{}" style="max-height:200px;width:auto;border-radius:8px;" />',
            obj.image.url
        ) if obj.image else "—"

@admin.register(VenueReservation)
class VenueReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "venue", "event", "date_reservation", "start_time")
    search_fields = ("user__username", "venue__nom_v", "event__title")
    list_filter = ("date_reservation",)