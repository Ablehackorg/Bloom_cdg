from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.text import slugify
from django.views.generic import TemplateView
from .models import Group, Message
from .serializers import GroupSerializer, MessageSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            slug=slugify(serializer.validated_data["name"])
        )

    # 🔒 Guruhni yopish
    @action(detail=True, methods=["post"], permission_classes=[IsOwnerOrAdmin])
    def close(self, request, pk=None):
        group = self.get_object()
        group.is_closed = True
        group.save(update_fields=["is_closed"])
        return Response({"status": "closed"}, status=status.HTTP_200_OK)

    # 🔓 Qayta ochish
    @action(detail=True, methods=["post"], permission_classes=[IsOwnerOrAdmin])
    def reopen(self, request, pk=None):
        group = self.get_object()
        group.is_closed = False
        group.save(update_fields=["is_closed"])
        return Response({"status": "reopened"}, status=status.HTTP_200_OK)

    # ❌ O‘chirish
    @action(detail=True, methods=["delete"], permission_classes=[IsOwnerOrAdmin])
    def remove(self, request, pk=None):
        group = self.get_object()
        group.delete()
        return Response({"status": "deleted"}, status=status.HTTP_204_NO_CONTENT)

    # ✉️ Xabar yuborish
    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        group = self.get_object()
        serializer = MessageSerializer(data={"text": request.data.get("text")})
        if serializer.is_valid():
            # 👇 bu yerda group va userni qo‘shib saqlaymiz
            message = Message.objects.create(
                group=group,
                user=request.user,
                text=serializer.validated_data["text"]
            )
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 📩 Xabarlarni olish
    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        group = self.get_object()
        messages = group.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class GroupsPage(TemplateView):
    template_name = "groups/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        groups = Group.objects.all().order_by("name")

        gid = self.request.GET.get("group")
        current_group = None
        msgs = []
        is_owner_or_admin = False

        if gid:
            try:
                current_group = Group.objects.get(id=gid)
                msgs = Message.objects.filter(group=current_group).order_by("created_at")

                # 👇 Admin yoki o‘sha group egasi bo‘lsa flag True
                if self.request.user.is_authenticated:
                    if self.request.user.is_staff or self.request.user.id == current_group.owner_id:
                        is_owner_or_admin = True
            except Group.DoesNotExist:
                current_group = None

        ctx.update({
            "groups": groups,
            "messages": msgs,
            "current_group": current_group,
            "is_owner_or_admin": is_owner_or_admin,
        })
        return ctx