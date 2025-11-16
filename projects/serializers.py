from rest_framework import serializers
from .models import Project, Donation, VolunteerApplication

class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "goal_amount", "collected_amount",
            "image", "category", "region",
            "created_by", "created_by_username",
            "created_at", "progress",
        ]
        read_only_fields = ["created_by", "collected_amount", "created_at", "progress"]

    def get_progress(self, obj):
        return obj.progress



class DonationSerializer(serializers.ModelSerializer):
    donor_username = serializers.CharField(source="donor.username", read_only=True)

    class Meta:
        model = Donation
        fields = ["id", "project", "donor", "donor_username", "amount", "created_at"]
        read_only_fields = ["project", "donor", "created_at"]


class VolunteerApplicationSerializer(serializers.ModelSerializer):
    volunteer_username = serializers.CharField(source="volunteer.username", read_only=True)

    class Meta:
        model = VolunteerApplication
        fields = ["id", "project", "volunteer", "volunteer_username", "note", "status", "created_at"]
        read_only_fields = ["project", "volunteer", "status", "created_at"]