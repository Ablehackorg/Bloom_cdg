from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    sdg = models.CharField(max_length=32, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_groups")
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.user.username if self.user else "Anon"
        return f"{who}: {self.text[:30]}"

    def save(self, *args, **kwargs):
        # ✅ Xavfsizroq qilib tekshiramiz
        if self.group_id and self.group.is_closed:
            raise ValueError("This group is closed, you cannot send messages.")
        super().save(*args, **kwargs)

