from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


# ✅ Custom filter: role bo‘yicha rangli buttonlar
class RoleListFilter(admin.SimpleListFilter):
    title = "Role"
    parameter_name = "role"

    def lookups(self, request, model_admin):
        return [
            ("owner", "🟠 Owner"),
            ("volunteer", "🟢 Volunteer"),
            ("investor", "🔵 Investor"),
            ("admin", "⚫ Admin"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(role=self.value())
        return queryset


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "role_badge",   # ✅ rangli badge
        "language",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = (RoleListFilter, "language", "is_staff", "is_active")  # ✅ custom filter ishlaydi
    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "role", "bio", "skills", "language")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "role",
                    "bio",
                    "skills",
                    "language",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    readonly_fields = ("date_joined", "last_login")

    # ✅ Role badge
    def role_badge(self, obj):
        colors = {
            "owner": "orange",
            "volunteer": "green",
            "investor": "blue",
            "admin": "black",
        }
        color = colors.get(obj.role, "gray")
        return format_html(
            '<span style="background:{}; color:white; padding:3px 8px; border-radius:8px; font-size:12px;">{}</span>',
            color,
            obj.get_role_display(),
        )

    role_badge.short_description = "Role"