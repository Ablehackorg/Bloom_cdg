from django.contrib import admin
from .models import Group, Message

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "sdg", "owner", "is_closed", "created_at")
    list_filter = ("is_closed", "created_at")
    search_fields = ("name", "slug", "sdg", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "user", "short_text", "created_at")
    list_filter = ("created_at", "group")
    search_fields = ("text", "user__username", "group__name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def short_text(self, obj):
        return (obj.text[:50] + "...") if len(obj.text) > 50 else obj.text
    short_text.short_description = "Text"