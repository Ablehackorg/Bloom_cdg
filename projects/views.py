from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import viewsets, permissions, decorators, response, status
from django.views.generic import DetailView, ListView
from .models import Project, Donation, VolunteerApplication
from .serializers import ProjectSerializer, DonationSerializer, VolunteerApplicationSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat project egasi yoki staff o‘zgartira oladi
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user or request.user.is_staff


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # 💰 Donate
    @decorators.action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def donate(self, request, pk=None):
        project = self.get_object()
        ser = DonationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        donation = ser.save(project=project, donor=request.user)
        project.collected_amount += donation.amount
        project.save(update_fields=["collected_amount"])
        return response.Response(
            {"ok": True, "collected_amount": project.collected_amount},
            status=status.HTTP_201_CREATED,
        )

    # 🙋 Volunteer application
    @decorators.action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        project = self.get_object()
        ser = VolunteerApplicationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(project=project, volunteer=request.user)
        return response.Response(ser.data, status=status.HTTP_201_CREATED)


# Template uchun
class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_details.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = self.get_object()
        user = self.request.user

        # Fix missing owner on-the-fly (temporary solution)
        if not project.created_by:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                project.created_by = admin_user
                project.save()

        # 👤 Foydalanuvchi volunteer bo‘lganmi?
        if user.is_authenticated:
            ctx["has_applied"] = VolunteerApplication.objects.filter(
                project=project, volunteer=user
            ).exists()
        else:
            ctx["has_applied"] = False

        # 💰 Donate mumkinmi (agar progress < 100 bo‘lsa)
        ctx["can_donate"] = project.progress < 100

        return ctx

def donate_success(request, project_id):
    project = Project.objects.get(id=project_id)
    messages.success(request, f"Thank you for donating to {project.title}!")
    return redirect("project-detail", pk=project_id)

class ProjectListView(ListView):
    model = Project
    template_name = "projects.html"  # <- поставь свой путь, если другой
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset().order_by("-created_at")
        category = self.request.GET.get("category")
        if category:
            # если category — CharField с choices ('health', 'education', ...)
            qs = qs.filter(category__iexact=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_category"] = self.request.GET.get("category", "")
        return ctx