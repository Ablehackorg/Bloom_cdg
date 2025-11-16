from django.views.generic import TemplateView
from projects.models import Project
from groups.models import Group

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Oxirgi 6 ta project
        ctx["projects"] = Project.objects.all().order_by("-created_at")[:6]

        # Groups bilan birga oxirgi xabarlarni olish
        groups = Group.objects.prefetch_related("messages").all().order_by("name")

        # Har bir group uchun oxirgi 2 ta xabarni olish
        for g in groups:
            g.latest_messages = g.messages.all().order_by("-created_at")[:2]

        ctx["groups"] = groups
        return ctx
