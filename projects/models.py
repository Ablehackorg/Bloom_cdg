from django.db import models
from django.conf import settings


REGION_CHOICES = [
    ("andijan", "Andijan"),
    ("bukhara", "Bukhara"),
    ("fergana", "Fergana"),
    ("jizzakh", "Jizzakh"),
    ("namangan", "Namangan"),
    ("navoiy", "Navoiy"),
    ("kashkadarya", "Kashkadarya"),
    ("samarkand", "Samarkand"),
    ("sirdarya", "Sirdarya"),
    ("surkhandarya", "Surkhandarya"),
    ("tashkent", "Tashkent"),
    ("karakalpakstan", "Karakalpakstan"),
    ("khorezm", "Khorezm"),
]


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("health", "Health"),
        ("education", "Education"),
        ("environment", "Environment"),
        ("innovation", "Innovation"),
        ("equality", "Equality"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    collected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)  # ✅ media/projects ichiga
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="health",
        verbose_name="SDG"
    )
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES,
        default="tashkent",
        verbose_name="Region"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def progress(self):
        goal = self.goal_amount or 0
        collected = self.collected_amount or 0
        if goal > 0:
            return min((collected / goal) * 100, 100)
        return 0



class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="donations")
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor} → {self.project} (${self.amount})"


class VolunteerApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="volunteer_applications")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer} → {self.project} ({self.status})"