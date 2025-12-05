
from django.contrib import admin
from .models import User, Role
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
# import pyotp
# import qrcode
# from io import BytesIO
# import base64
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_id", "name", "description")
    search_fields = ("name",)
    ordering = ("role_id",)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # CHAMPS AFFICHÉS DANS LE TABLEAU
    list_display = (
        "user_id",
        "firstname",
        "lastname",
        "email",
        "role",
        "nationality",
        "num_tel",
        "theme",
        "active_badge",
        "created_at",
    )

    # Colonnes cliquables
    list_display_links = ("user_id", "firstname", "lastname")

    # Recherche
    search_fields = (
        "user_id",
        "firstname",
        "lastname",
        "email",
        "role__name",
        "nationality",
    )

    # Filtres
    list_filter = ("role", "theme", "is_active", "created_at")

    # Tri par défaut
    ordering = ("-created_at",)

    # Pagination
    list_per_page = 20

    # Champs en lecture seule
    readonly_fields = ("user_id", "created_at", "updated_at", "last_login")

    # Organisation du formulaire en sections
    fieldsets = (
        ("Informations personnelles", {
            "fields": ("user_id", "firstname", "lastname", "email", "password")
        }),
        ("Profil", {
            "fields": ("nationality", "num_tel", "adresse", "bio")
        }),
        ("Paramètres du compte", {
            "fields": ("role", "theme", "is_active",),
            "classes": ("collapse",)
        }),
        ("Permissions avancées", {
            "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",)
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at","last_login",)
        }),
    )

    # Champs affichés dans le formulaire d'ajout
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "firstname", "lastname", "email", "username",
                "password1", "password2",
                "nationality", "num_tel", "adresse",
                "role", "theme",
            ),
        }),
    )

    # Actions personnalisées
    actions = ["activate_users", "deactivate_users"]

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilisateur(s) activé(s).")

    activate_users.short_description = "Activer les comptes sélectionnés"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilisateur(s) désactivé(s).")

    deactivate_users.short_description = "Désactiver les comptes sélectionnés"
    def active_badge(self, obj):
        color = "green" if obj.is_active else "orange"
        status = "Activated" if obj.is_active else "Pending"
        return format_html(
            '<span style="color:white;background-color:{};padding:3px 7px;border-radius:5px;">{}</span>',
            color,
            status,
        )

    active_badge.short_description = "Status"
    # def totp_qr(self, obj):
    #     if obj.totp_secret:

    #         totp = pyotp.TOTP(obj.totp_secret)
    #         uri = totp.provisioning_uri(name=obj.email, issuer_name="MyApp")

    #         # Générer QR code
    #         qr = qrcode.make(uri)
    #         buffer = BytesIO()
    #         qr.save(buffer, format="PNG")
    #         img_str = base64.b64encode(buffer.getvalue()).decode()
    #         return format_html('<img src="data:image/png;base64,{}" width="100" />', img_str)
    #     return "No TOTP setup"

    # totp_qr.short_description = "QR Code 2FA"
    # import csv

    actions += ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=users.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exporter la sélection en CSV"
    list_filter = (
        ("role", admin.RelatedOnlyFieldListFilter),
        ("theme", admin.ChoicesFieldListFilter),
        ("is_active", admin.BooleanFieldListFilter),
        ("created_at", admin.DateFieldListFilter),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        # Tu peux injecter du CSS pour colorer les lignes si nécessaire
        return response

# Dans ton admin.py, tu peux ajouter un Media pour custom CSS
class Media:
    css = {
        "all": ("css/admin_custom.css",)
    }






