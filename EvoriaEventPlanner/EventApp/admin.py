from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id_evenement", "nom", "date_evenement", "created_at")
    list_filter = ("date_evenement",)
    search_fields = ("nom",)
    ordering = ("-date_evenement", "nom")
