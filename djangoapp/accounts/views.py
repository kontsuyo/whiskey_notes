from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from accounts.models import TastingNoteUser
from accounts.serializers import CustomUserSerializer


class UserList(generics.ListAPIView):
    queryset = TastingNoteUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    queryset = TastingNoteUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class CreateUser(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = CustomUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
