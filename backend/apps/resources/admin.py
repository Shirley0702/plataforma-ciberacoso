from django.contrib import admin

from .models import OrientationResource


@admin.register(OrientationResource)
class OrientationResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "phone", "emergency", "active")
    list_filter = ("country", "emergency", "active")
    list_editable = ("active",)
    search_fields = ("name", "description")
