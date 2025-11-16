from rest_framework import serializers
from .models import Group, Message

class GroupSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "slug",
            "sdg",
            "is_closed",
            "owner",
            "owner_username",
            "created_at",
        ]
        read_only_fields = ["owner", "slug", "is_closed", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "group", "user", "user_username", "text", "created_at"]
        read_only_fields = ["user", "group", "created_at"]