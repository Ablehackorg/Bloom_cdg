from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Donation, VolunteerApplication


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    readonly_fields = ("donor", "amount", "created_at")
    can_delete = False


class VolunteerApplicationInline(admin.TabularInline):
    model = VolunteerApplication
    extra = 0
    readonly_fields = ("volunteer", "note", "status", "created_at")
    can_delete = False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category_display",   # ✅ SDG deb chiqadi
        "goal_amount",
        "collected_amount",
        "progress_bar",
        "donors_count",
        "volunteers_count",
        "created_by",
        "created_at",
    )
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "region")
    readonly_fields = ("created_at", "progress_bar")
    inlines = [DonationInline, VolunteerApplicationInline]

    def category_display(self, obj):
        return obj.get_category_display()   # choices’dan “Health”/“Education” ni oladi
    category_display.short_description = "SDG"

    def progress_bar(self, obj):
        percent = obj.progress
        color = "green" if percent >= 100 else "orange" if percent >= 50 else "red"
        return format_html(
            '<div style="width:100px; background:#eee; border-radius:4px;">'
            '<div style="width:{}%; background:{}; color:white; text-align:center; font-size:10px; border-radius:4px;">'
            '{}%</div></div>',
            int(percent),
            color,
            int(percent),
        )
    progress_bar.short_description = "Progress"

    def donors_count(self, obj):
        return obj.donations.count()
    donors_count.short_description = "Donors"

    def volunteers_count(self, obj):
        return obj.volunteer_applications.count()
    volunteers_count.short_description = "Volunteers"


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "donor", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("project__title", "donor__username")


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "volunteer", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("project__title", "volunteer__username")