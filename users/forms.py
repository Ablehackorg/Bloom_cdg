from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "bio", "skills", "language"]  # kerakli fieldlar
        widgets = {
            "username": forms.TextInput(attrs={"class": "w-full px-3 py-2 border rounded-lg"}),
            "email": forms.EmailInput(attrs={"class": "w-full px-3 py-2 border rounded-lg"}),
            "bio": forms.Textarea(attrs={"class": "w-full px-3 py-2 border rounded-lg", "rows": 3}),
            "skills": forms.Textarea(attrs={"class": "w-full px-3 py-2 border rounded-lg", "rows": 2}),
            "language": forms.Select(attrs={"class": "w-full px-3 py-2 border rounded-lg"}),
        }