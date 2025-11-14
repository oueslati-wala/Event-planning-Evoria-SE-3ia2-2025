from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Animateur, ReservationAnim

@admin.register(Animateur)
class AnimateurAdmin(admin.ModelAdmin):
    list_display=("photo_thumb","nom","type_animation","prix_base","capacite_max","interieur_exterieur","disponible","created_at")
    list_filter=("interieur_exterieur","disponible","created_at")
    search_fields=("nom","type_animation","tags")
    ordering=("nom",)

    readonly_fields = ("photo_preview",)

    def photo_thumb(self, obj):
        if getattr(obj, "photo", None):
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />')
        return "—"
    photo_thumb.short_description = "Photo"

    def photo_preview(self, obj):
        if getattr(obj, "photo", None):
            return mark_safe(f'<img src="{obj.photo.url}" style="max-width:300px;height:auto;border-radius:6px;" />')
        return "Aucune image"
    photo_preview.short_description = "Aperçu"

@admin.register(ReservationAnim)
class ReservationAnimAdmin(admin.ModelAdmin):
    list_display=("id","animateur","date_debut","date_fin","lieu","statut","prix_total")
    list_filter=("statut","date_debut")
    search_fields=("lieu","id_evenement","animateur__nom")
    autocomplete_fields=("animateur",)
