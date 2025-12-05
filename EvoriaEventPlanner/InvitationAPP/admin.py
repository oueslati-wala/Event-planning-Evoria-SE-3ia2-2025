from django.contrib import admin
from django.db.models import Count
from .models import Invitation, Guest


admin.site.site_title = "Evoria"
admin.site.site_header = "Evoria Administration"
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
    change_list_template = "admin/InvitationAPP/guest/change_list.html"

    def changelist_view(self, request, extra_context=None):
        qs = Guest.objects.all()
        total = qs.count()
        by_status = dict(qs.values_list("status").annotate(total=Count("id")))
        labels = {
            "pending": "En attente",
            "confirmed": "Confirmé",
            "declined": "Décliné",
            "attended": "Présent",
            "absent": "Absent",
        }
        stats = []
        for key, label in labels.items():
            count = by_status.get(key, 0)
            percent = int((count * 100) / total) if total else 0
            stats.append({"key": key, "label": label, "count": count, "percent": percent})
        extra_context = extra_context or {}
        extra_context["status_stats"] = stats
        extra_context["total_guests"] = total
        return super().changelist_view(request, extra_context=extra_context)
