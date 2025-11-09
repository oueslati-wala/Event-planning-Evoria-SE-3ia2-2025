from django.contrib import admin
from .models import Invitation, Guest


admin.site.site_title = "Evoria"
admin.site.site_header = "Gestion des invitations et invités"
admin.site.index_title = "Django App Invitations"


@admin.register(Invitation)
class AdminInvitationModel(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name", "theme", "location")


@admin.register(Guest)
class AdminGuestModel(admin.ModelAdmin):
    list_display = ("__str__", "email", "phone", "company", "position", "status", "invitation")
    search_fields = ("first_name", "last_name", "email", "company")
    list_filter = ("status", "title", "invitation", "plus_one")
    list_select_related = ("invitation",)
    raw_id_fields = ("invitation",)
    list_per_page = 50