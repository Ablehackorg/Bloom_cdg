from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [("owner","Owner"), ("volunteer","Volunteer"),
                    ("investor","Investor"), ("admin","Admin")]
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="owner")
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    language = models.CharField(max_length=8, default="en")