from django.contrib import admin
from .models import Caterer, MenuItem


@admin.register(Caterer)
class CatererAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'status', 'phone', 'email')
    search_fields = ('name', 'company_name', 'email')
    list_filter = ('status',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available', 'caterer')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')
