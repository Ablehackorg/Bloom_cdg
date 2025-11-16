from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView  # <- ДОБАВЬ ЭТО
from users.views import custom_login, custom_logout, custom_signup, profile_view
from common.views import HomeView
from projects.views import ProjectDetailView, ProjectListView
from groups.views import GroupsPage
from rest_framework.routers import DefaultRouter
from projects.views import ProjectViewSet
from groups.views import GroupViewSet

# API router faqat /api/ ostida ishlaydi
router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project-api")  # 🔥 nomi boshqa
router.register("groups", GroupViewSet, basename="group-api")

urlpatterns = [
    path("admin/", admin.site.urls),

    # Templates
    path("", HomeView.as_view(), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("groups/", GroupsPage.as_view(), name="groups"),
    path("blogs/", include("blog.urls")),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),

    # Auth (custom views)
    path("profile/", profile_view, name="profile"),
    path("login/", custom_login, name="login"),
    path("logout/", custom_logout, name="logout"),
    path("signup/", custom_signup, name="signup"),
    # API
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)