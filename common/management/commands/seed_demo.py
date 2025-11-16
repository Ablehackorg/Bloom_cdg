from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import Project
from blog.models import Post
from groups.models import Group, Message

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo data for hackathon MVP"

    def handle(self, *args, **options):
        # --- Users ---
        owner, _ = User.objects.get_or_create(
            username="owner",
            defaults={"email": "owner@test.com", "role": "owner"}
        )
        owner.set_password("1234")
        owner.save()

        volunteer, _ = User.objects.get_or_create(
            username="volunteer",
            defaults={"email": "vol@test.com", "role": "volunteer"}
        )
        volunteer.set_password("1234")
        volunteer.save()

        investor, _ = User.objects.get_or_create(
            username="investor",
            defaults={"email": "inv@test.com", "role": "investor"}
        )
        investor.set_password("1234")
        investor.save()

        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@test.com", "role": "admin", "is_staff": True, "is_superuser": True}
        )
        admin.set_password("1234")
        admin.save()

        self.stdout.write(self.style.SUCCESS(
            "Demo users created: owner / volunteer / investor / admin (password: 1234)"
        ))

        # --- Projects ---
        if not Project.objects.exists():
            Project.objects.create(
                title="Clean Water for All",
                description="Building wells and providing clean water access.",
                goal_amount=5000,
                collected_amount=1200,
                category="health",
                region="africa",
                owner=owner,
            )
            Project.objects.create(
                title="Tech for Schools",
                description="Providing laptops and coding lessons for children.",
                goal_amount=8000,
                collected_amount=3500,
                category="education",
                region="asia",
                owner=investor,
            )
            self.stdout.write(self.style.SUCCESS("Demo projects created."))

        # --- Blog ---
        if not Post.objects.exists():
            Post.objects.create(
                title="Why Volunteering Matters",
                content="Volunteering changes lives.",
                author=owner,
            )
            Post.objects.create(
                title="Future of Social Impact",
                content="Technology + humanity = impact.",
                author=investor,
            )
            self.stdout.write(self.style.SUCCESS("Demo blog posts created."))

        # --- Groups ---
        if not Group.objects.exists():
            g1 = Group.objects.create(name="Health Volunteers", owner=owner)
            g2 = Group.objects.create(name="Tech Innovators", owner=investor)
            self.stdout.write(self.style.SUCCESS("Demo groups created."))

            # Messages for groups
            Message.objects.create(group=g1, user=owner, text="Welcome to Health Volunteers group!")
            Message.objects.create(group=g1, user=volunteer, text="Happy to join and help!")
            Message.objects.create(group=g2, user=investor, text="Tech can change education!")
            Message.objects.create(group=g2, user=owner, text="Absolutely, let’s brainstorm ideas.")
            self.stdout.write(self.style.SUCCESS("Demo messages created."))

        self.stdout.write(self.style.SUCCESS("✅ Demo data successfully seeded."))