from django.contrib import admin
from .models import User  # <-- ton modèle User de UserApp

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "created_at")
    search_fields = ("nom",)
    ordering = ("nom",)
    readonly_fields = ("created_at", "updated_at")
    fields = ("nom", "created_at", "updated_at")
